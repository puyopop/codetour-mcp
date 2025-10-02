# codetour-mcp

MCP server for managing [VS Code's CodeTour](https://github.com/microsoft/codetour) extension files. This tool helps you create and manage interactive code tours programmatically through AI coding assistants like Claude Code and Gemini CLI.

## Features

- **Tour Management**: Create, read, and list CodeTour files
- **Step Management**: Add, update, remove, and retrieve tour steps
- **Pattern-based Steps**: Define steps using regex patterns for precise code location
- **Directory-based Steps**: Create steps associated with directories

## Quick Start

### Installation with Claude Desktop

The easiest way to use CodeTour MCP is with Claude Desktop:

```bash
claude mcp add codetour-mcp -- uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp
```

After this command, restart Claude Desktop and you'll have access to all CodeTour tools.

### Manual Installation

```bash
# Install with uvx
uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp

# Or install from source
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp
pip install -e .
```

### Quick Test

Try the demo script to see the functionality:

```bash
python examples/demo.py
```

This will:
1. Create a sample tour
2. Add various types of steps
3. Show you how to manipulate tours
4. Output the final tour JSON

## Available Tools

### Tour Management

#### `create_tour`
Create a new CodeTour file.

**Parameters:**
- `path` (required): Path to the tour file (e.g., `.tours/my-tour.tour`)
- `title` (required): Title of the tour
- `description` (optional): Description of the tour

**Example:**
```json
{
  "path": ".tours/getting-started.tour",
  "title": "Getting Started",
  "description": "A tour of the basic features"
}
```

#### `read_tour`
Read the complete tour object from a file.

**Parameters:**
- `path` (required): Path to the tour file

#### `list_tours`
List all tours in a directory.

**Parameters:**
- `dir` (optional): Directory to search (default: `.tours`)

**Returns:**
```json
[
  {
    "path": ".tours/my-tour.tour",
    "title": "My Tour",
    "description": "Tour description",
    "stepCount": 5
  }
]
```

### Step Listing and Retrieval

#### `list_steps`
List all steps in a tour.

**Parameters:**
- `tour_path` (required): Path to the tour file

**Returns:**
```json
[
  {
    "index": 0,
    "title": "Step Title",
    "file": "src/main.py",
    "pattern_regex": "def main\\(",
    "description": "This is the first step..."
  }
]
```

#### `get_step`
Get a specific step by index.

**Parameters:**
- `tour_path` (required): Path to the tour file
- `index` (required): Step index (0-based)

### Step Addition

#### `insert_step`
Insert a step using pattern regex (preferred method).

**Parameters:**
- `tour_path` (required): Path to the tour file
- `file` (required): File path relative to workspace root
- `pattern_regex` (required): Regular expression to match (e.g., `function main\\(`)
- `description` (required): Description of the step
- `index` (optional): Position to insert (omit to append)
- `title` (optional): Title for the step

**Example:**
```json
{
  "tour_path": ".tours/my-tour.tour",
  "file": "src/server.py",
  "pattern_regex": "def main\\(\\):",
  "description": "This is the main entry point",
  "title": "Main Function"
}
```

#### `insert_step_by_directory`
Insert a step using directory location.

**Parameters:**
- `tour_path` (required): Path to the tour file
- `file` (required): File path relative to workspace root
- `directory` (required): Directory path
- `description` (required): Description of the step
- `index` (optional): Position to insert (omit to append)
- `title` (optional): Title for the step

### Step Editing and Deletion

#### `update_step`
Update an existing step's description or title.

**Parameters:**
- `tour_path` (required): Path to the tour file
- `index` (required): Step index (0-based)
- `description` (optional): New description
- `title` (optional): New title

**Note:** You cannot change pattern/file/directory through update. Delete and recreate the step instead.

#### `remove_step`
Remove a step from a tour.

**Parameters:**
- `tour_path` (required): Path to the tour file
- `index` (required): Step index (0-based)

## CodeTour File Format

Tours are stored as JSON files conforming to the [CodeTour schema](https://raw.githubusercontent.com/microsoft/codetour/refs/heads/main/schema.json). Each tour file contains:

- `title`: Tour title
- `description` (optional): Tour description
- `steps`: Array of step objects

Each step can contain:
- `file`: File path
- `pattern`: Regex pattern to locate code
- `directory`: Directory path
- `description`: Step description
- `title` (optional): Step title
- And other properties per the CodeTour schema

## Usage Examples

### Creating a Tour

```javascript
// Create a new tour
create_tour({
  path: ".tours/architecture.tour",
  title: "System Architecture",
  description: "Overview of the system components"
})

// Add steps
insert_step({
  tour_path: ".tours/architecture.tour",
  file: "src/main.py",
  pattern_regex: "class Application",
  description: "This is the main application class that orchestrates everything",
  title: "Application Entry"
})
```

### Managing Steps

```javascript
// List all steps
list_steps({
  tour_path: ".tours/architecture.tour"
})

// Update a step
update_step({
  tour_path: ".tours/architecture.tour",
  index: 0,
  description: "Updated description for better clarity"
})

// Remove a step
remove_step({
  tour_path: ".tours/architecture.tour",
  index: 2
})
```

## Viewing Tours

To view your tours in VS Code:

1. Install the [CodeTour extension](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour)
2. Open your project in VS Code
3. Click the CodeTour icon in the Activity Bar
4. Select your tour from the list
5. Click "Start Tour"

## Tips

- Use `pattern_regex` instead of line numbers when possible - they're more maintainable
- Keep step descriptions concise but informative
- Use titles to help users navigate longer tours
- Test your tours by opening them in VS Code with the CodeTour extension
- Tours are just JSON files - you can edit them manually if needed

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp

# Install in development mode
pip install -e .

# Run the demo to verify everything works
python examples/demo.py
```

### Testing

Before submitting a PR, make sure:

1. All existing functionality still works:
```bash
python examples/demo.py
```

2. Your code passes syntax checks:
```bash
python -m py_compile src/codetour_mcp/*.py
```

3. Generated tours are valid JSON:
```bash
python -m json.tool .tours/demo-tour.tour
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Add docstrings to all public functions and classes
- Use descriptive variable names

### Adding New MCP Tools

To add a new tool:

1. Add the tool definition in `server.py::list_tools()`:
```python
Tool(
    name="my_new_tool",
    description="Description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)
```

2. Add the handler in `server.py::call_tool()`:
```python
elif name == "my_new_tool":
    param1 = arguments["param1"]
    # Implementation here
    return [TextContent(
        type="text",
        text="Result"
    )]
```

3. Update README.md with documentation for the new tool

### Project Structure

```
codetour-mcp/
├── src/codetour_mcp/
│   ├── __init__.py      # Package metadata
│   ├── core.py          # Core tour management (no MCP dependencies)
│   └── server.py        # MCP server implementation
├── examples/
│   ├── demo.py          # Demonstration script
│   └── .tours/          # Example tour files
├── README.md            # Main documentation
└── pyproject.toml       # Package configuration
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

When adding new features:
1. Update `core.py` if adding tour management functionality
2. Update `server.py` if adding new MCP tools
3. Add examples to demonstrate the new feature
4. Update documentation in README.md
5. Test thoroughly with the demo script