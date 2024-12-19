# MCP Zotero

A Model Context Protocol server for Zotero integration that allows Claude to interact with your Zotero library.

## Setup

1. Get your Zotero credentials:

   ```bash
   # First, create an API key at https://www.zotero.org/settings/keys
   # Then use it to get your user ID:
   curl -H "Zotero-API-Key: YOUR_API_KEY" https://api.zotero.org/keys/current
   ```

   The response will look like:

   ```json
   {
     "userID": 123456,
     "username": "your_username",
     "access": {
       "user": {
         "library": true,
         "files": true,
         "notes": true,
         "write": true
       }
     }
   }
   ```

   The `userID` value is what you need.

2. Set environment variables:

   ```bash
   export ZOTERO_API_KEY="your-api-key"
   export ZOTERO_USER_ID="user-id-from-curl"
   ```

3. Verify your credentials:

   ```bash
   # Test that your credentials work:
   curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        "https://api.zotero.org/users/$ZOTERO_USER_ID/collections"
   ```

   You should see your collections list in the response.

4. Install the package:

   ```bash
   npm install mcp-zotero
   ```

5. Run the server:
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
