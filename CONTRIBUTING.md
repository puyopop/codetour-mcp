# Contributing to CodeTour MCP

Thank you for your interest in contributing to CodeTour MCP! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/puyopop/codetour-mcp.git
cd codetour-mcp
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run the demo to verify everything works:
```bash
python examples/demo.py
```

## Project Structure

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
├── QUICKSTART.md        # Quick start guide
└── pyproject.toml       # Package configuration
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Add docstrings to all public functions and classes
- Use descriptive variable names

## Testing

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

## Adding New Features

When adding new features:

1. **Update core.py** if adding tour management functionality
2. **Update server.py** if adding new MCP tools
3. **Add examples** to demonstrate the new feature
4. **Update documentation** in README.md and QUICKSTART.md
5. **Test thoroughly** with the demo script

## Adding New MCP Tools

To add a new tool:

1. Add the tool definition in `list_tools()`:
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

2. Add the handler in `call_tool()`:
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

## CodeTour Schema

All tours must comply with the [CodeTour schema](https://raw.githubusercontent.com/microsoft/codetour/refs/heads/main/schema.json).

Required fields:
- `title` (string)
- `steps` (array)

Each step must have:
- `description` (string)
- At least one location field: `file`, `directory`, `uri`, or `view`

## Commit Messages

Use clear, descriptive commit messages:

- Start with a verb in present tense (Add, Fix, Update, Remove)
- Keep the first line under 72 characters
- Add details in the body if needed

Good examples:
- `Add support for line-based step insertion`
- `Fix error handling in remove_step`
- `Update README with new examples`

## Pull Requests

1. Create a new branch for your feature:
```bash
git checkout -b feature/my-new-feature
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Add my new feature"
```

3. Push to GitHub:
```bash
git push origin feature/my-new-feature
```

4. Open a pull request with:
   - Clear description of what changed
   - Why the change is needed
   - Any testing you've done

## Questions?

If you have questions about contributing:
- Open an issue on GitHub
- Check existing issues and pull requests
- Review the examples in the `examples/` directory

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
