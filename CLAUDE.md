# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that manages VS Code CodeTour extension files. It provides tools to programmatically create and manage interactive code tours through AI assistants.

## Development Commands

### Installation and Setup
```bash
# Install in development mode
pip install -e .

# Run the MCP server
codetour-mcp
```

### Testing
```bash
# Run the demonstration script to test functionality
python examples/demo.py

# Validate Python syntax
python -m py_compile src/codetour_mcp/*.py

# Validate generated tour JSON
python -m json.tool .tours/demo-tour.tour
```

## Architecture

### Core Components

**src/codetour_mcp/core.py**
- Pure Python functions for tour file management
- No MCP dependencies - can be used standalone
- Handles JSON loading/saving with proper encoding (UTF-8)

**src/codetour_mcp/server.py**
- MCP server implementation using `mcp.server.Server`
- Defines all tool schemas in `list_tools()`
- Implements tool handlers in `call_tool()`
- Entry point: `main()` runs the stdio server

**src/codetour_mcp/__init__.py**
- Package metadata only

### Data Flow

1. MCP tools receive requests with arguments
2. `call_tool()` validates and extracts arguments
3. Core functions (`load_tour`, `save_tour`) handle file I/O
4. Results returned as `TextContent` objects (JSON strings)

### Tour File Structure

Tours are JSON files conforming to the [CodeTour schema](https://raw.githubusercontent.com/microsoft/codetour/refs/heads/main/schema.json):

```json
{
  "title": "Tour Title",
  "description": "Optional description",
  "steps": [
    {
      "file": "path/to/file.py",
      "pattern": "regex pattern",
      "description": "Step description",
      "title": "Optional step title"
    }
  ]
}
```

**Key Location Methods:**
- `pattern` (regex): Preferred - robust to code changes
- `line` (number): Fragile - breaks when code moves
- `directory`: For directory-level steps

## Development Guidelines

### Adding New MCP Tools

1. Add tool definition in `server.py::list_tools()`:
```python
Tool(
    name="tool_name",
    description="What it does",
    inputSchema={
        "type": "object",
        "properties": {...},
        "required": [...]
    }
)
```

2. Add handler in `server.py::call_tool()`:
```python
elif name == "tool_name":
    # Extract arguments
    # Call core functions if needed
    # Return TextContent
```

3. Update README.md with documentation

### Code Style Requirements

- Use type hints: `def func(param: str) -> dict[str, Any]:`
- Python 3.10+ syntax (requires-python = ">=3.10")
- PEP 8 formatting
- Docstrings for public functions
- UTF-8 encoding for all file I/O

### Tour Validation

All tours must have:
- `title` (string)
- `steps` (array)

Each step must have:
- `description` (string)
- At least one location: `file`, `directory`, `uri`, or `view`

### Testing Changes

Before commits:
1. Run `python examples/demo.py` - must complete without errors
2. Validate syntax: `python -m py_compile src/codetour_mcp/*.py`
3. Check generated JSON: `python -m json.tool .tours/demo-tour.tour`

## Key Patterns

### Pattern Regex Usage
When creating steps with `insert_step`, use escaped regex:
- Class definition: `class MyClass\\(`
- Function definition: `def main\\(\\):`
- Import statement: `from module import \\w+`

### Index-based Operations
- Step indices are 0-based
- `insert_step` with no index → appends to end
- `insert_step` with index → inserts at position
- Validate index range: `0 <= index < len(steps)`

### Error Handling
- `FileNotFoundError`: Tour file doesn't exist
- `IndexError`: Step index out of range
- Return empty arrays for non-existent directories (not errors)
