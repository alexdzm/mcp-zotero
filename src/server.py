#!/usr/bin/env python3
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv
from pydantic import BaseModel

# Import MCP SDK
from mcp.server.fastmcp import FastMCP
from src.types.zotero_types import ZoteroCreator, ZoteroTag

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("mcp-zotero")

# Load environment variables
load_dotenv()

class ZoteroServer:
    def __init__(self):
        logger.info("Initializing ZoteroServer...")

        # Get API credentials from environment
        self.api_key = os.environ.get('ZOTERO_API_KEY')
        self.user_id = os.environ.get('ZOTERO_USER_ID')
        
        if not self.api_key or not self.user_id:
            error_msg = "Missing ZOTERO_API_KEY or ZOTERO_USER_ID environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.info(f"Using Zotero user ID: {self.user_id}")
        
        # Initialize Zotero API client
        try:
            from pyzotero import zotero
            self.zotero_api = zotero.Zotero(self.user_id, 'user', self.api_key)
            logger.info("Zotero API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Zotero API client: {str(e)}")
            raise
            
        # Create MCP Server
        self.mcp = FastMCP("Zotero")
        self._setup_tools()

    def _setup_tools(self):
        """Register all tools with the MCP server"""
        
        @self.mcp.tool()
        def get_collections() -> str:
            """List all collections in your Zotero library"""
            logger.info(f"GET_COLLECTIONS: Starting with userId {self.user_id}")
            
            try:
                collections = self.zotero_api.collections()
                logger.info(f"GET_COLLECTIONS: Found {len(collections)} collections")
                
                if not collections:
                    return json.dumps({
                        "error": "No collections found",
                        "suggestion": "Create a collection in your Zotero library first", 
                        "helpUrl": "https://www.zotero.org/support/collections"
                    }, indent=2)
                    
                return json.dumps(collections, default=lambda o: o.__dict__, indent=2)
            except Exception as e:
                logger.error(f"GET_COLLECTIONS: Failed: {str(e)}")
                return json.dumps({"error": str(e)}, indent=2)

        @self.mcp.tool()
        def get_collection_items(collection_key: str) -> str:
            """Get all items in a specific collection in your Zotero library"""
            logger.info(f"GET_COLLECTION_ITEMS: Fetching items for collection {collection_key}")
            
            try:
                items = self.zotero_api.collection_items(collection_key)
                logger.info(f"GET_COLLECTION_ITEMS: Found {len(items)} items")
                
                if not items:
                    return json.dumps({
                        "error": "Collection is empty",
                        "collectionKey": collection_key,
                        "suggestion": "Add some items to this collection in Zotero",
                        "status": "empty"
                    }, indent=2)
                    
                formatted = []
                for item in items:
                    creators = item.get('creators', [])
                    authors = ", ".join([
                        f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() 
                        for c in creators if c
                    ]) or "No authors listed"
                    
                    formatted.append({
                        "title": item.get('title', 'Untitled'),
                        "authors": authors,
                        "date": item.get('date', 'No date'),
                        "key": item.get('key', 'No key'),
                        "itemType": item.get('itemType', 'Unknown type'),
                        "abstractNote": item.get('abstractNote', 'No abstract available'),
                        "tags": [t.get('tag') for t in item.get('tags', []) if t.get('tag')],
                        "doi": item.get('DOI'),
                        "url": item.get('url'),
                        "publicationTitle": item.get('publicationTitle')
                    })
                    
                logger.info(f"GET_COLLECTION_ITEMS: Formatted {len(formatted)} items")
                return json.dumps(formatted, indent=2)
                
            except Exception as e:
                logger.error(f"GET_COLLECTION_ITEMS: Failed: {str(e)}")
                if "404" in str(e):
                    return json.dumps({
                        "error": "Collection is empty or not accessible",
                        "collectionKey": collection_key,
                        "suggestion": "Verify the collection exists and try adding some items to it",
                        "status": "not_found"
                    }, indent=2)
                return json.dumps({"error": str(e)}, indent=2)

        @self.mcp.tool()
        def get_item_details(item_key: str) -> str:
            """Get detailed information about a specific paper in your Zotero library"""
            if not item_key or not item_key.strip():
                return json.dumps({"error": "Item key is required"}, indent=2)
                
            try:
                item = self.zotero_api.item(item_key)
                logger.info(f"GET_ITEM_DETAILS: Retrieved item {item_key}")
                
                if not item:
                    return json.dumps({
                        "error": "Item not found or inaccessible",
                        "itemKey": item_key,
                        "suggestion": "Verify the item exists and you have permission to access it"
                    }, indent=2)
                    
                creators = item.get('creators', [])
                authors = ", ".join([
                    f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() 
                    for c in creators if c
                ]) or "No authors listed"
                
                formatted = {
                    "title": item.get('title', 'Untitled'),
                    "authors": authors,
                    "date": item.get('date', 'No date'),
                    "abstract": item.get('abstractNote', 'No abstract available'),
                    "publicationTitle": item.get('publicationTitle', 'No publication title'),
                    "doi": item.get('DOI', 'No DOI'),
                    "url": item.get('url', 'No URL'),
                    "tags": [t.get('tag') for t in item.get('tags', [])],
                    "collections": item.get('collections', [])
                }
                
                return json.dumps(formatted, indent=2)
            except Exception as e:
                logger.error(f"GET_ITEM_DETAILS: Failed: {str(e)}")
                return json.dumps({"error": str(e)}, indent=2)

        @self.mcp.tool()
        def search_library(query: str) -> str:
            """Search your entire Zotero library"""
            if not query or not query.strip():
                return json.dumps({"error": "Search query is required"}, indent=2)
                
            try:
                items = self.zotero_api.items(q=query)
                logger.info(f"SEARCH_LIBRARY: Found {len(items)} items for query '{query}'")
                
                if not items:
                    return json.dumps({
                        "error": "No results found",
                        "query": query,
                        "suggestion": "Try a different search term or verify your library contains matching items"
                    }, indent=2)
                    
                formatted = []
                for item in items:
                    creators = item.get('creators', [])
                    authors = ", ".join([
                        f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() 
                        for c in creators if c
                    ]) or "No authors listed"
                    
                    formatted.append({
                        "title": item.get('title', 'Untitled'),
                        "authors": authors,
                        "date": item.get('date', 'No date'),
                        "key": item.get('key'),
                        "itemType": item.get('itemType'),
                        "abstractNote": item.get('abstractNote', 'No abstract available')
                    })
                    
                return json.dumps(formatted, indent=2)
            except Exception as e:
                logger.error(f"SEARCH_LIBRARY: Failed: {str(e)}")
                return json.dumps({"error": str(e)}, indent=2)

        @self.mcp.tool()
        def get_recent(limit: Optional[int] = 10) -> str:
            """Get recently added papers to your library"""
            try:
                # Cap at 100 items max
                actual_limit = min(limit or 10, 100)
                
                items = self.zotero_api.items(sort='dateAdded', direction='desc', limit=actual_limit)
                logger.info(f"GET_RECENT: Found {len(items)} recent items")
                
                if not items:
                    return json.dumps({
                        "error": "No recent items found",
                        "suggestion": "Add some items to your Zotero library first"
                    }, indent=2)
                    
                formatted = []
                for item in items:
                    creators = item.get('creators', [])
                    authors = ", ".join([
                        f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() 
                        for c in creators if c
                    ]) or "No authors listed"
                    
                    formatted.append({
                        "title": item.get('title', 'Untitled'),
                        "authors": authors,
                        "dateAdded": item.get('dateAdded', 'No date'),
                        "key": item.get('key'),
                        "itemType": item.get('itemType')
                    })
                    
                return json.dumps(formatted, indent=2)
            except Exception as e:
                logger.error(f"GET_RECENT: Failed: {str(e)}")
                return json.dumps({"error": str(e)}, indent=2)

    def start(self):
        """Start the server using MCP SDK"""
        logger.info("Starting Zotero MCP server")
        self.mcp.run()


def main():
    """Entry point for the application"""
    try:
        logger.info("Starting MCP Zotero Server...")
        server = ZoteroServer()
        server.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 