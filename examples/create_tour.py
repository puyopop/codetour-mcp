#!/usr/bin/env python3
"""Example of using the CodeTour MCP tools programmatically."""

import asyncio
from codetour_mcp.server import mcp


async def create_example_tour():
    """Create an example tour."""
    
    # Create a tour
    print("Creating tour...")
    result = await mcp.call_tool("create_tour", {
        "title": "Getting Started",
        "description": "Learn about the main components of this project",
        "workspace_path": "."
    })
    print(result[0][0].text)
    
    # Add steps to the tour
    print("\nAdding steps...")
    
    # Step 1: Main entry point
    result = await mcp.call_tool("add_step", {
        "tour_title": "Getting Started",
        "file": "src/main.py",
        "line": 10,
        "description": "This is where the application starts. The main function initializes and runs the program.",
        "title": "Application Entry Point",
        "workspace_path": "."
    })
    print(result[0][0].text)
    
    # Step 2: Configuration
    result = await mcp.call_tool("add_step", {
        "tour_title": "Getting Started",
        "file": "src/config.py",
        "description": "Configuration settings are loaded from this module. You can customize behavior here.",
        "workspace_path": "."
    })
    print(result[0][0].text)
    
    # List all tours
    print("\nAll tours in workspace:")
    result = await mcp.call_tool("list_tours", {"workspace_path": "."})
    print(result[0][0].text)
    
    print("\n✓ Tour created! Open VS Code with CodeTour extension to view it.")


if __name__ == "__main__":
    asyncio.run(create_example_tour())
