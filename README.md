# MCP Zotero

A Model Context Protocol (MCP) integration for Zotero, allowing AI assistants to access and interact with your Zotero library.

This Python implementation provides the same functionality as the original TypeScript version but uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for improved compatibility and maintainability.

## Features

- List all collections in your Zotero library
- Get all items in a specific collection
- Get detailed information about a specific paper
- Search your entire Zotero library
- Get recently added papers to your library

## Installation

### Using UV (Recommended)

This project uses [UV](https://github.com/astral-sh/uv), a modern Python package manager that is significantly faster than pip.

If you don't have UV installed:

```bash
# Install UV
curl -sSf https://astral.sh/uv/install.sh | bash
```

Install mcp-zotero with UV:

```bash
# Create a virtual environment and install dependencies
uv sync
```

## Usage

1. Set up your environment variables:

```bash
export ZOTERO_API_KEY="your_zotero_api_key"
export ZOTERO_USER_ID="your_zotero_user_id"
```

2. Run the server:

```bash

uv run src/server.py
```

3. Integration with Claude Desktop:

```bash
# With environment variables
mcp install src/server.py --name "Zotero Library" -v ZOTERO_API_KEY=your_key -v ZOTERO_USER_ID=your_id
```

## Docker

You can also run using Docker:

```bash
docker build -t mcp-zotero-python .
docker run -e ZOTERO_API_KEY="your_api_key" -e ZOTERO_USER_ID="your_user_id" mcp-zotero-python
```

## Development

### Using UV for Development

UV provides efficient workflow for Python development:

```bash
# Install in development mode
uv pip install -e .

# Install a specific version of a dependency
uv pip install pydantic==2.5.2

# Add a new dependency to pyproject.toml
uv pip install some-package --upgrade-package
```

### Running with the MCP Development Tools

```bash
# Run with the MCP development tools for debugging
mcp dev src/server.py

# Run with the MCP development tools and edit mode
mcp dev src/server.py --with-editable .
```

## Finding Your Zotero API Key and User ID

### API Key
1. Log in to your Zotero account at https://www.zotero.org/
2. Go to Settings → API Keys
3. Create a new private key with read-only permissions (or read/write if you plan to add functionality later)

### User ID
1. Go to https://www.zotero.org/settings/keys
2. Your user ID is listed under "Your userID for use in API calls"

## License

ISC
