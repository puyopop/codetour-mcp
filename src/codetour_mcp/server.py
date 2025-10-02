"""CodeTour MCP Server - Main implementation."""

import json
from pathlib import Path
from typing import Any

import mcp.server.stdio
from mcp.server import Server
from mcp.types import TextContent, Tool

from .core import load_tour, save_tour

app = Server("codetour-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="create_tour",
            description="Create a new CodeTour file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the tour file (e.g., '.tours/my-tour.tour')"},
                    "title": {"type": "string", "description": "Title of the tour"},
                    "description": {"type": "string", "description": "Optional description of the tour"},
                },
                "required": ["path", "title"],
            },
        ),
        Tool(
            name="read_tour",
            description="Read a complete tour object from a file",
            inputSchema={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path to the tour file"}},
                "required": ["path"],
            },
        ),
        Tool(
            name="list_tours",
            description="List all tours in a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "dir": {"type": "string", "description": "Directory to search for tours (default: '.tours')"}
                },
            },
        ),
        Tool(
            name="list_steps",
            description="List all steps in a tour",
            inputSchema={
                "type": "object",
                "properties": {"tour_path": {"type": "string", "description": "Path to the tour file"}},
                "required": ["tour_path"],
            },
        ),
        Tool(
            name="get_step",
            description="Get a specific step from a tour",
            inputSchema={
                "type": "object",
                "properties": {
                    "tour_path": {"type": "string", "description": "Path to the tour file"},
                    "index": {"type": "number", "description": "Step index (0-based)"},
                },
                "required": ["tour_path", "index"],
            },
        ),
        Tool(
            name="insert_step",
            description="Insert a step into a tour using pattern regex",
            inputSchema={
                "type": "object",
                "properties": {
                    "tour_path": {"type": "string", "description": "Path to the tour file"},
                    "index": {"type": "number", "description": "Position to insert the step (omit to append)"},
                    "file": {"type": "string", "description": "File path relative to workspace root"},
                    "pattern_regex": {"type": "string", "description": "Regular expression to match in the file"},
                    "description": {"type": "string", "description": "Description of the step"},
                    "title": {"type": "string", "description": "Optional title for the step"},
                },
                "required": ["tour_path", "file", "pattern_regex", "description"],
            },
        ),
        Tool(
            name="insert_step_by_directory",
            description="Insert a step into a tour using directory location",
            inputSchema={
                "type": "object",
                "properties": {
                    "tour_path": {"type": "string", "description": "Path to the tour file"},
                    "index": {"type": "number", "description": "Position to insert the step (omit to append)"},
                    "file": {"type": "string", "description": "File path relative to workspace root"},
                    "directory": {"type": "string", "description": "Directory path relative to workspace root"},
                    "description": {"type": "string", "description": "Description of the step"},
                    "title": {"type": "string", "description": "Optional title for the step"},
                },
                "required": ["tour_path", "file", "directory", "description"],
            },
        ),
        Tool(
            name="update_step",
            description="Update an existing step's description or title",
            inputSchema={
                "type": "object",
                "properties": {
                    "tour_path": {"type": "string", "description": "Path to the tour file"},
                    "index": {"type": "number", "description": "Step index (0-based)"},
                    "description": {"type": "string", "description": "New description"},
                    "title": {"type": "string", "description": "New title"},
                },
                "required": ["tour_path", "index"],
            },
        ),
        Tool(
            name="remove_step",
            description="Remove a step from a tour",
            inputSchema={
                "type": "object",
                "properties": {
                    "tour_path": {"type": "string", "description": "Path to the tour file"},
                    "index": {"type": "number", "description": "Step index (0-based)"},
                },
                "required": ["tour_path", "index"],
            },
        ),
    ]


def truncate_description(description: str, max_length: int = 50) -> str:
    """
    Truncate a description to a maximum length.

    >>> truncate_description("Short")
    'Short'
    >>> truncate_description("This is a very long description that needs truncation")
    'This is a very long description that needs ...'
    >>> truncate_description("Exactly fifty characters long description here!!")
    'Exactly fifty characters long description here!!'
    >>> truncate_description("Just over fifty characters in this description!!!")
    'Just over fifty characters in this descripti...'
    """
    if len(description) > max_length:
        return description[: max_length - 3] + "..."
    return description


def validate_step_index(index: int, steps: list[dict[str, Any]]) -> None:
    """
    Validate that a step index is within valid range.

    >>> validate_step_index(0, [{"desc": "step1"}])
    >>> validate_step_index(2, [{"desc": "step1"}, {"desc": "step2"}, {"desc": "step3"}])
    >>> validate_step_index(-1, [{"desc": "step1"}])
    Traceback (most recent call last):
        ...
    IndexError: Step index -1 out of range (0-0)
    >>> validate_step_index(3, [{"desc": "step1"}])
    Traceback (most recent call last):
        ...
    IndexError: Step index 3 out of range (0-0)
    """
    if index < 0 or index >= len(steps):
        raise IndexError(f"Step index {index} out of range (0-{len(steps) - 1})")


def create_step_info(index: int, step: dict[str, Any]) -> dict[str, Any]:
    """
    Create step info dictionary from a step.

    >>> create_step_info(0, {"description": "Test", "file": "test.py"})
    {'index': 0, 'description': 'Test', 'file': 'test.py'}
    >>> create_step_info(
    ...     1,
    ...     {"description": "A very long description that exceeds the maximum length", "title": "Title"}
    ... )
    {'index': 1, 'description': 'A very long description that exceeds the max...', 'title': 'Title'}
    >>> create_step_info(0, {"description": "Test", "pattern": "test.*"})
    {'index': 0, 'description': 'Test', 'pattern_regex': 'test.*'}
    """
    description = truncate_description(step.get("description", ""))
    step_info = {"index": index, "description": description}

    for key in ("title", "file", "directory"):
        if key in step:
            step_info[key] = step[key]

    if "pattern" in step:
        step_info["pattern_regex"] = step["pattern"]

    return step_info


def build_step(
    file: str, description: str, title: str | None = None, pattern: str | None = None, directory: str | None = None
) -> dict[str, Any]:
    """
    Build a step dictionary with optional fields.

    >>> build_step("test.py", "Test step")
    {'file': 'test.py', 'description': 'Test step'}
    >>> build_step("test.py", "Test", title="Title", pattern="test.*")
    {'file': 'test.py', 'pattern': 'test.*', 'description': 'Test', 'title': 'Title'}
    >>> build_step("test.py", "Test", directory="src/")
    {'file': 'test.py', 'directory': 'src/', 'description': 'Test'}
    """
    step = {"file": file}

    if pattern:
        step["pattern"] = pattern
    if directory:
        step["directory"] = directory

    step["description"] = description

    if title:
        step["title"] = title

    return step


def insert_step_at_index(steps: list[dict[str, Any]], step: dict[str, Any], index: int | None = None) -> int:
    """
    Insert a step at the specified index or append if None.

    >>> steps = [{"desc": "step1"}]
    >>> insert_step_at_index(steps, {"desc": "new"}, 0)
    0
    >>> steps
    [{'desc': 'new'}, {'desc': 'step1'}]
    >>> steps = [{"desc": "step1"}]
    >>> insert_step_at_index(steps, {"desc": "new"}, None)
    1
    >>> steps
    [{'desc': 'step1'}, {'desc': 'new'}]
    """
    if index is not None:
        steps.insert(index, step)
        return index
    else:
        steps.append(step)
        return len(steps) - 1


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls using pattern matching."""
    match name:
        case "create_tour":
            path = arguments["path"]
            title = arguments["title"]
            description = arguments.get("description", "")

            tour_data = {"title": title, "steps": []}
            if description:
                tour_data["description"] = description

            save_tour(path, tour_data)
            return [TextContent(type="text", text=f"Created tour '{title}' at {path}")]

        case "read_tour":
            path = arguments["path"]
            tour_data = load_tour(path)
            return [TextContent(type="text", text=json.dumps(tour_data, indent=2))]

        case "list_tours":
            dir_path = arguments.get("dir", ".tours")
            tours_dir = Path(dir_path)

            if not tours_dir.exists():
                return [TextContent(type="text", text=json.dumps([]))]

            tours = []
            for tour_file in tours_dir.glob("*.tour"):
                try:
                    tour_data = load_tour(str(tour_file))
                    tours.append(
                        {
                            "path": str(tour_file),
                            "title": tour_data.get("title", ""),
                            "description": tour_data.get("description", ""),
                            "stepCount": len(tour_data.get("steps", [])),
                        }
                    )
                except Exception:
                    continue

            return [TextContent(type="text", text=json.dumps(tours, indent=2))]

        case "list_steps":
            tour_path = arguments["tour_path"]
            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            step_list = [create_step_info(i, step) for i, step in enumerate(steps)]
            return [TextContent(type="text", text=json.dumps(step_list, indent=2))]

        case "get_step":
            tour_path = arguments["tour_path"]
            index = int(arguments["index"])

            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            validate_step_index(index, steps)
            return [TextContent(type="text", text=json.dumps(steps[index], indent=2))]

        case "insert_step":
            tour_path = arguments["tour_path"]
            file = arguments["file"]
            pattern_regex = arguments["pattern_regex"]
            description = arguments["description"]
            title = arguments.get("title")
            index = arguments.get("index")

            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            step = build_step(file, description, title=title, pattern=pattern_regex)
            actual_index = insert_step_at_index(steps, step, int(index) if index is not None else None)

            tour_data["steps"] = steps
            save_tour(tour_path, tour_data)

            return [TextContent(type="text", text=f"Inserted step at index {actual_index}")]

        case "insert_step_by_directory":
            tour_path = arguments["tour_path"]
            file = arguments["file"]
            directory = arguments["directory"]
            description = arguments["description"]
            title = arguments.get("title")
            index = arguments.get("index")

            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            step = build_step(file, description, title=title, directory=directory)
            actual_index = insert_step_at_index(steps, step, int(index) if index is not None else None)

            tour_data["steps"] = steps
            save_tour(tour_path, tour_data)

            return [TextContent(type="text", text=f"Inserted step at index {actual_index}")]

        case "update_step":
            tour_path = arguments["tour_path"]
            index = int(arguments["index"])
            description = arguments.get("description")
            title = arguments.get("title")

            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            validate_step_index(index, steps)

            if description is not None:
                steps[index]["description"] = description
            if title is not None:
                steps[index]["title"] = title

            tour_data["steps"] = steps
            save_tour(tour_path, tour_data)

            return [TextContent(type="text", text=f"Updated step at index {index}")]

        case "remove_step":
            tour_path = arguments["tour_path"]
            index = int(arguments["index"])

            tour_data = load_tour(tour_path)
            steps = tour_data.get("steps", [])

            validate_step_index(index, steps)
            steps.pop(index)

            tour_data["steps"] = steps
            save_tour(tour_path, tour_data)

            return [TextContent(type="text", text=f"Removed step at index {index}")]

        case _:
            raise ValueError(f"Unknown tool: {name}")


def main():
    """Main entry point for the server."""
    import asyncio

    async def run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
