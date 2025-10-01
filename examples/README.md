# CodeTour MCP Examples

This directory contains examples demonstrating how to use the CodeTour MCP server.

## Files

### demo.py

A Python script that demonstrates the core functionality of the codetour_mcp module. Run it with:

```bash
python examples/demo.py
```

This script demonstrates:
- Creating a new tour
- Adding steps (pattern-based, line-based, and directory-based)
- Listing steps in a tour
- Updating step descriptions
- Removing steps
- Reading the final tour JSON

### .tours/example-tour.tour

An example CodeTour file that provides a tour of the CodeTour MCP server itself. This tour can be opened in VS Code with the CodeTour extension to see how the server is structured.

## Running the Demo

```bash
cd /path/to/codetour-mcp
python examples/demo.py
```

The demo will:
1. Create a new tour file in `.tours/demo-tour.tour`
2. Add various types of steps
3. Show how to list and manipulate steps
4. Display the final tour content

## Using with VS Code

After running the demo, you can:

1. Open this project in VS Code
2. Install the [CodeTour extension](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour)
3. Open the tour by clicking on the CodeTour icon in the sidebar
4. Follow the tour to learn about the project structure

## Integration with MCP

When used as an MCP server (through Claude Desktop or similar), these operations would be called through the MCP tool interface instead of directly in Python. The MCP server provides the following tools:

- `create_tour` - Create a new tour file
- `read_tour` - Read an existing tour
- `list_tours` - List all tours in a directory
- `list_steps` - List steps in a tour
- `get_step` - Get a specific step
- `insert_step` - Add a new step with pattern regex
- `insert_step_by_directory` - Add a new step with directory location
- `update_step` - Update a step's description or title
- `remove_step` - Remove a step from a tour

See the main [README.md](../README.md) for more details on using the MCP server.
