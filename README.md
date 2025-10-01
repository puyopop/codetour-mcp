# codetour-mcp

MCP server for managing [VS Code's CodeTour](https://github.com/microsoft/codetour) extension files. This tool helps you create and manage interactive code tours programmatically through AI coding assistants like Claude Code and Gemini CLI.

## Features

- **Tour Management**: Create, read, and list CodeTour files
- **Step Management**: Add, update, remove, and retrieve tour steps
- **Pattern-based Steps**: Define steps using regex patterns for precise code location
- **Directory-based Steps**: Create steps associated with directories

## Installation

### Using Claude Desktop

Add to your Claude Desktop configuration:

```bash
claude mcp add codetour-mcp -- uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp
```

### Manual Installation

```bash
# Install with uvx
uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp

# Or install from source
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp
pip install -e .
```

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

## Development

```bash
# Clone the repository
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp

# Install dependencies
pip install -e .

# Run the server
codetour-mcp
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.