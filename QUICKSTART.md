# Quick Start Guide

## Installation with Claude Desktop

The easiest way to use CodeTour MCP is with Claude Desktop:

```bash
claude mcp add codetour-mcp -- uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp
```

After this command, restart Claude Desktop and you'll have access to all CodeTour tools.

## Manual Installation

If you want to install the package manually:

```bash
# Clone the repository
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp

# Install with pip
pip install -e .

# Run the server
codetour-mcp
```

## Quick Test

Try the demo script to see the functionality:

```bash
python examples/demo.py
```

This will:
1. Create a sample tour
2. Add various types of steps
3. Show you how to manipulate tours
4. Output the final tour JSON

## Using the Tools

### Create Your First Tour

```json
{
  "tool": "create_tour",
  "arguments": {
    "path": ".tours/my-first-tour.tour",
    "title": "Getting Started",
    "description": "A tour of the main features"
  }
}
```

### Add a Step with Pattern Matching

```json
{
  "tool": "insert_step",
  "arguments": {
    "tour_path": ".tours/my-first-tour.tour",
    "file": "src/main.py",
    "pattern_regex": "def main\\(\\):",
    "description": "This is where the application starts",
    "title": "Main Entry Point"
  }
}
```

### List All Steps

```json
{
  "tool": "list_steps",
  "arguments": {
    "tour_path": ".tours/my-first-tour.tour"
  }
}
```

### Update a Step

```json
{
  "tool": "update_step",
  "arguments": {
    "tour_path": ".tours/my-first-tour.tour",
    "index": 0,
    "description": "Updated description with more details"
  }
}
```

## Common Patterns

### Pattern-Based Steps (Recommended)

Use regex patterns to locate code. This is more robust than line numbers:

```json
{
  "pattern_regex": "class MyClass\\(BaseClass\\):"
}
```

### Directory-Based Steps

For steps that point to a whole directory or don't need precise location:

```json
{
  "file": "README.md",
  "directory": ".",
  "description": "Project documentation"
}
```

### Line-Based Steps

You can also use line numbers directly in the JSON (not through insert_step):

```json
{
  "file": "src/main.py",
  "line": 42,
  "description": "Important function"
}
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

## Next Steps

- Check out the [full README](README.md) for detailed documentation
- Look at the [example tour](examples/.tours/example-tour.tour) for a complete example
- Run the [demo script](examples/demo.py) to see all features in action
