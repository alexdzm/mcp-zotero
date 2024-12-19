# MCP Zotero

A Model Context Protocol server for Zotero integration that allows Claude to interact with your Zotero library.

## Setup

1. Get your Zotero credentials:

   - Get your API key from https://www.zotero.org/settings/keys
   - Find your User ID from https://www.zotero.org/settings/keys (shown at the top)

2. Set environment variables:

   ```bash
   export ZOTERO_API_KEY="your-api-key"
   export ZOTERO_USER_ID="your-user-id"
   ```

3. Install the package:

   ```bash
   npm install mcp-zotero
   ```

4. Run the server:
   ```bash
   npx mcp-zotero
   ```

## Configure with Claude Desktop

1. Open Claude Desktop
2. Go to Settings (gear icon)
3. Navigate to the "Model Context Protocol" section
4. Click "Add Server"
5. Fill in the details:
   - Name: "Zotero"
   - Description: "Access your Zotero library"
   - Transport Type: "stdio"
   - Command: `npx mcp-zotero`
6. Click "Save"

## Usage with Claude

Once configured, you can ask Claude to:

- "Show me my Zotero collections"
- "What papers are in my [collection name] collection?"
- "Tell me more about [paper title]"
- "Search my library for papers about [topic]"
- "What are my most recently added papers?"

## Available Tools

- `get_collections`: List all collections in your library
- `get_collection_items`: Get items in a specific collection
- `get_item_details`: Get detailed information about a paper
- `search_library`: Search your entire library
- `get_recent`: Get recently added papers
