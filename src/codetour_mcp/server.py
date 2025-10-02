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


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    if name == "create_tour":
        path = arguments["path"]
        title = arguments["title"]
        description = arguments.get("description", "")

        tour_data = {"title": title, "steps": []}
        if description:
            tour_data["description"] = description

        save_tour(path, tour_data)

        return [TextContent(type="text", text=f"Created tour '{title}' at {path}")]

    elif name == "read_tour":
        path = arguments["path"]
        tour_data = load_tour(path)

        return [TextContent(type="text", text=json.dumps(tour_data, indent=2))]

    elif name == "list_tours":
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

    elif name == "list_steps":
        tour_path = arguments["tour_path"]
        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        step_list = []
        for i, step in enumerate(steps):
            description = step.get("description", "")
            # Truncate to ~50 characters
            if len(description) > 50:
                description = description[:47] + "..."

            step_info = {"index": i, "description": description}

            if "title" in step:
                step_info["title"] = step["title"]
            if "file" in step:
                step_info["file"] = step["file"]
            if "directory" in step:
                step_info["directory"] = step["directory"]
            if "pattern" in step:
                step_info["pattern_regex"] = step["pattern"]

            step_list.append(step_info)

        return [TextContent(type="text", text=json.dumps(step_list, indent=2))]

    elif name == "get_step":
        tour_path = arguments["tour_path"]
        index = int(arguments["index"])

        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        if index < 0 or index >= len(steps):
            raise IndexError(f"Step index {index} out of range (0-{len(steps) - 1})")

        return [TextContent(type="text", text=json.dumps(steps[index], indent=2))]

    elif name == "insert_step":
        tour_path = arguments["tour_path"]
        file = arguments["file"]
        pattern_regex = arguments["pattern_regex"]
        description = arguments["description"]
        title = arguments.get("title")
        index = arguments.get("index")

        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        step = {"file": file, "pattern": pattern_regex, "description": description}
        if title:
            step["title"] = title

        if index is not None:
            steps.insert(int(index), step)
        else:
            steps.append(step)

        tour_data["steps"] = steps
        save_tour(tour_path, tour_data)

        actual_index = int(index) if index is not None else len(steps) - 1
        return [TextContent(type="text", text=f"Inserted step at index {actual_index}")]

    elif name == "insert_step_by_directory":
        tour_path = arguments["tour_path"]
        file = arguments["file"]
        directory = arguments["directory"]
        description = arguments["description"]
        title = arguments.get("title")
        index = arguments.get("index")

        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        step = {"file": file, "directory": directory, "description": description}
        if title:
            step["title"] = title

        if index is not None:
            steps.insert(int(index), step)
        else:
            steps.append(step)

        tour_data["steps"] = steps
        save_tour(tour_path, tour_data)

        actual_index = int(index) if index is not None else len(steps) - 1
        return [TextContent(type="text", text=f"Inserted step at index {actual_index}")]

    elif name == "update_step":
        tour_path = arguments["tour_path"]
        index = int(arguments["index"])
        description = arguments.get("description")
        title = arguments.get("title")

        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        if index < 0 or index >= len(steps):
            raise IndexError(f"Step index {index} out of range (0-{len(steps) - 1})")

        if description is not None:
            steps[index]["description"] = description
        if title is not None:
            steps[index]["title"] = title

        tour_data["steps"] = steps
        save_tour(tour_path, tour_data)

        return [TextContent(type="text", text=f"Updated step at index {index}")]

    elif name == "remove_step":
        tour_path = arguments["tour_path"]
        index = int(arguments["index"])

        tour_data = load_tour(tour_path)
        steps = tour_data.get("steps", [])

        if index < 0 or index >= len(steps):
            raise IndexError(f"Step index {index} out of range (0-{len(steps) - 1})")

        steps.pop(index)

        tour_data["steps"] = steps
        save_tour(tour_path, tour_data)

        return [TextContent(type="text", text=f"Removed step at index {index}")]

    else:
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
