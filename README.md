# CodeTour MCP Server

An MCP (Model Context Protocol) server for generating VS Code's CodeTour extension files. This tool assists in creating interactive code tours using AI coding tools like Claude Code and Gemini CLI.

## What is CodeTour?

[CodeTour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) is a VS Code extension that allows you to create guided walkthroughs of your codebase. Tours are stored as JSON files in a `.tours` directory.

## Installation

Install using `uvx` (part of the `uv` toolchain):

```bash
uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp
```

Or add to Claude Desktop configuration:

```bash
claude mcp add codetour -- uvx --from git+https://github.com/puyopop/codetour-mcp codetour-mcp
```

## Available Tools

### create_tour
Create a new CodeTour file in the `.tours` directory.

**Parameters:**
- `title` (required): Title of the tour
- `description` (optional): Description of what the tour covers
- `workspace_path` (optional): Path to the workspace (default: current directory)

**Example:**
```
Create a tour titled "Getting Started" with description "Introduction to the project structure"
```

### add_step
Add a step to an existing CodeTour.

**Parameters:**
- `tour_title` (required): Title of the tour to add the step to
- `file` (required): Relative path to the file for this step
- `line` (optional): Line number in the file (1-indexed)
- `description` (required): Explanation text for this step
- `title` (optional): Optional title for this step
- `workspace_path` (optional): Path to the workspace (default: current directory)

**Example:**
```
Add a step to "Getting Started" tour: file "src/main.py", line 10, description "This is where the application starts"
```

### list_tours
List all CodeTour files in the workspace.

**Parameters:**
- `workspace_path` (optional): Path to the workspace (default: current directory)

### get_tour
Get the full content of a specific CodeTour.

**Parameters:**
- `tour_title` (required): Title of the tour to retrieve
- `workspace_path` (optional): Path to the workspace (default: current directory)

## Usage with AI Coding Tools

Once installed, you can ask your AI coding assistant to:
- Create tours to document your codebase
- Add steps explaining key parts of your code
- Generate comprehensive walkthroughs for onboarding

Example prompts:
- "Create a tour called 'API Overview' that explains the REST endpoints"
- "Add a step to the Authentication tour for the login function in auth.py"
- "List all existing tours in this project"

## Development

Install in development mode:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

MIT