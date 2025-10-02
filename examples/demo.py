#!/usr/bin/env python3
"""
Demo script showing how to use the codetour_mcp.core module directly.

This demonstrates the core functionality without the MCP server layer.
When using as an MCP server, these operations would be called through
the MCP tool interface.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import codetour_mcp
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from codetour_mcp.core import load_tour, save_tour


def demo_create_tour():
    """Demonstrate creating a new tour."""
    print("=" * 60)
    print("Demo: Creating a new tour")
    print("=" * 60)

    tour_path = ".tours/demo-tour.tour"
    tour_data = {"title": "Demo Tour", "description": "This tour demonstrates the project structure", "steps": []}

    save_tour(tour_path, tour_data)
    print(f"✓ Created tour: {tour_path}")
    return tour_path


def demo_add_steps(tour_path):
    """Demonstrate adding steps to a tour."""
    print("\n" + "=" * 60)
    print("Demo: Adding steps to the tour")
    print("=" * 60)

    tour_data = load_tour(tour_path)

    # Add step with pattern
    tour_data["steps"].append(
        {
            "file": "src/codetour_mcp/server.py",
            "pattern": "@app.list_tools",
            "title": "Tool Registration",
            "description": "This decorator registers all available MCP tools with the server.",
        }
    )
    print("✓ Added step 1 (pattern-based)")

    # Add step with line number (alternative to pattern)
    tour_data["steps"].append(
        {
            "file": "src/codetour_mcp/core.py",
            "line": 10,
            "title": "Load Function",
            "description": "This function loads a tour file from disk and parses the JSON.",
        }
    )
    print("✓ Added step 2 (line-based)")

    # Add step with directory
    tour_data["steps"].append(
        {
            "directory": "examples",
            "file": "examples/demo.py",
            "title": "Demo Script",
            "description": "This example script shows how to use the core functionality directly.",
        }
    )
    print("✓ Added step 3 (directory-based)")

    save_tour(tour_path, tour_data)
    print(f"\nTour now has {len(tour_data['steps'])} steps")


def demo_list_steps(tour_path):
    """Demonstrate listing steps in a tour."""
    print("\n" + "=" * 60)
    print("Demo: Listing all steps")
    print("=" * 60)

    tour_data = load_tour(tour_path)

    print(f"Tour: {tour_data['title']}")
    print(f"Description: {tour_data.get('description', 'N/A')}")
    print(f"\nSteps ({len(tour_data['steps'])}):")

    for i, step in enumerate(tour_data["steps"]):
        title = step.get("title", "Untitled")
        file = step.get("file", "N/A")

        location = ""
        if "pattern" in step:
            location = f"pattern: {step['pattern']}"
        elif "line" in step:
            location = f"line: {step['line']}"
        elif "directory" in step:
            location = f"directory: {step['directory']}"

        print(f"  {i}. {title}")
        print(f"     File: {file}")
        if location:
            print(f"     Location: {location}")
        print(f"     Description: {step['description'][:60]}...")
        print()


def demo_update_step(tour_path):
    """Demonstrate updating a step."""
    print("=" * 60)
    print("Demo: Updating a step")
    print("=" * 60)

    tour_data = load_tour(tour_path)

    # Update the first step
    tour_data["steps"][0]["description"] = "UPDATED: This decorator is the key to exposing tools to MCP clients."

    save_tour(tour_path, tour_data)
    print("✓ Updated step 0's description")


def demo_remove_step(tour_path):
    """Demonstrate removing a step."""
    print("\n" + "=" * 60)
    print("Demo: Removing a step")
    print("=" * 60)

    tour_data = load_tour(tour_path)
    initial_count = len(tour_data["steps"])

    # Remove the second step
    tour_data["steps"].pop(1)

    save_tour(tour_path, tour_data)
    print(f"✓ Removed step 1 (tour now has {len(tour_data['steps'])} steps instead of {initial_count})")


def demo_final_result(tour_path):
    """Show the final tour content."""
    print("\n" + "=" * 60)
    print("Demo: Final tour content")
    print("=" * 60)

    with open(tour_path) as f:
        print(f.read())


def main():
    """Run the complete demo."""
    print("\n" + "=" * 60)
    print("CodeTour MCP - Core Functionality Demo")
    print("=" * 60)
    print()

    tour_path = demo_create_tour()
    demo_add_steps(tour_path)
    demo_list_steps(tour_path)
    demo_update_step(tour_path)
    demo_remove_step(tour_path)
    demo_list_steps(tour_path)
    demo_final_result(tour_path)

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
    print(f"\nCreated tour file: {tour_path}")
    print("You can open this in VS Code with the CodeTour extension.")


if __name__ == "__main__":
    main()
