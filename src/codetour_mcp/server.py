"""MCP Server for CodeTour file generation."""

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("codetour-mcp")


def get_tours_directory(workspace_path: str = ".") -> Path:
    """Get or create the .tours directory."""
    tours_dir = Path(workspace_path) / ".tours"
    tours_dir.mkdir(exist_ok=True)
    return tours_dir


def load_tour(tour_file: Path) -> dict[str, Any]:
    """Load a tour from a JSON file."""
    with open(tour_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tour(tour_file: Path, tour_data: dict[str, Any]) -> None:
    """Save a tour to a JSON file."""
    with open(tour_file, "w", encoding="utf-8") as f:
        json.dump(tour_data, f, indent=2, ensure_ascii=False)


@mcp.tool()
def create_tour(title: str, description: str = "", workspace_path: str = ".") -> str:
    """Create a new CodeTour. A CodeTour is a guided walkthrough of a codebase stored in .tours/ directory.
    
    Args:
        title: Title of the tour
        description: Description of what the tour covers
        workspace_path: Path to the workspace (default: current directory)
    
    Returns:
        Success message with the location of the created tour
    """
    tours_dir = get_tours_directory(workspace_path)
    
    # Create tour filename from title
    filename = title.lower().replace(" ", "-").replace("/", "-") + ".tour"
    tour_file = tours_dir / filename
    
    if tour_file.exists():
        return f"Error: Tour '{title}' already exists at {tour_file}"
    
    tour_data = {
        "$schema": "https://aka.ms/codetour-schema",
        "title": title,
        "steps": []
    }
    
    if description:
        tour_data["description"] = description
    
    save_tour(tour_file, tour_data)
    
    return f"Successfully created tour '{title}' at {tour_file}"


@mcp.tool()
def add_step(
    tour_title: str,
    file: str,
    description: str,
    line: int | None = None,
    title: str | None = None,
    workspace_path: str = "."
) -> str:
    """Add a step to an existing CodeTour. Each step points to a specific file and line, with explanatory text.
    
    Args:
        tour_title: Title of the tour to add the step to
        file: Relative path to the file for this step
        description: Explanation text for this step
        line: Line number in the file (1-indexed)
        title: Optional title for this step
        workspace_path: Path to the workspace (default: current directory)
    
    Returns:
        Success message confirming the step was added
    """
    tours_dir = get_tours_directory(workspace_path)
    
    filename = tour_title.lower().replace(" ", "-").replace("/", "-") + ".tour"
    tour_file = tours_dir / filename
    
    if not tour_file.exists():
        return f"Error: Tour '{tour_title}' not found at {tour_file}"
    
    tour_data = load_tour(tour_file)
    
    step = {
        "file": file,
        "description": description,
    }
    
    if line is not None:
        step["line"] = line
    
    if title is not None:
        step["title"] = title
    
    tour_data["steps"].append(step)
    save_tour(tour_file, tour_data)
    
    step_num = len(tour_data["steps"])
    return f"Successfully added step {step_num} to tour '{tour_title}'"


@mcp.tool()
def list_tours(workspace_path: str = ".") -> str:
    """List all CodeTour files in the workspace .tours directory.
    
    Args:
        workspace_path: Path to the workspace (default: current directory)
    
    Returns:
        List of tours with their step counts
    """
    tours_dir = get_tours_directory(workspace_path)
    
    tour_files = list(tours_dir.glob("*.tour"))
    
    if not tour_files:
        return f"No tours found in {tours_dir}"
    
    tours_info = []
    for tour_file in sorted(tour_files):
        tour_data = load_tour(tour_file)
        step_count = len(tour_data.get("steps", []))
        title = tour_data.get("title", tour_file.stem)
        description = tour_data.get("description", "")
        
        info = f"- {title} ({step_count} steps)"
        if description:
            info += f": {description}"
        tours_info.append(info)
    
    return f"Tours in {tours_dir}:\n" + "\n".join(tours_info)


@mcp.tool()
def get_tour(tour_title: str, workspace_path: str = ".") -> str:
    """Get the full content of a specific CodeTour including all steps.
    
    Args:
        tour_title: Title of the tour to retrieve
        workspace_path: Path to the workspace (default: current directory)
    
    Returns:
        JSON representation of the tour
    """
    tours_dir = get_tours_directory(workspace_path)
    
    filename = tour_title.lower().replace(" ", "-").replace("/", "-") + ".tour"
    tour_file = tours_dir / filename
    
    if not tour_file.exists():
        return f"Error: Tour '{tour_title}' not found at {tour_file}"
    
    tour_data = load_tour(tour_file)
    
    return json.dumps(tour_data, indent=2)


def main():
    """Main entry point."""
    mcp.run()


if __name__ == "__main__":
    main()
