import json
import os
import sys
import logging
from typing import Any
from pathlib import Path
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, ResourceTemplate
from pydantic import AnyUrl
import re

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("webex-mcp")

server = Server("webex-calling-mcp")

SCRIPT_DIR = Path(__file__).parent.absolute()
API_COLLECTION_PATH = SCRIPT_DIR / "webex_api_collection.json"
BEARER_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN", "")

api_data = {}

def load_api_collection():
    global api_data
    print(f"Loading API collection from: {API_COLLECTION_PATH}", file=sys.stderr)
    with open(API_COLLECTION_PATH, 'r', encoding='utf-8') as f:
        api_data = json.load(f)
    logger.info(f"Loaded {api_data['total_endpoints']} API endpoints")

# Expose API catalog as resources
@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = [
        Resource(
            uri="webex://api/catalog",
            name="Webex API Catalog",
            mimeType="application/json",
            description="Complete catalog of all Webex Calling APIs organized by feature"
        )
    ]
    
    for feature in api_data['endpoints'].keys():
        resources.append(Resource(
            uri=f"webex://api/feature/{feature}",
            name=f"{feature} APIs",
            mimeType="application/json",
            description=f"All API endpoints for {feature}"
        ))
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "webex://api/catalog":
        catalog = {}
        for feature, endpoints in api_data['endpoints'].items():
            catalog[feature] = {
                'count': len(endpoints),
                'endpoints': [
                    {
                        'title': ep['title'],
                        'method': ep['method'],
                        'path': ep['path'],
                        'summary': ep['spec']['spec'].get('summary', '')
                    }
                    for ep in endpoints
                ]
            }
        return json.dumps(catalog, indent=2)
    
    if uri.startswith("webex://api/feature/"):
        feature = uri.replace("webex://api/feature/", "")
        if feature in api_data['endpoints']:
            return json.dumps(api_data['endpoints'][feature], indent=2)
    
    return json.dumps({"error": "Resource not found"})

# Single generic tool for executing any API
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="webex_api_call",
            description="Execute any Webex Calling API. Provide feature name, endpoint title, and parameters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "string",
                        "description": "Feature category (e.g., 'People', 'Locations', 'Numbers')"
                    },
                    "endpoint_title": {
                        "type": "string",
                        "description": "Exact endpoint title from API catalog"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "API parameters as key-value pairs"
                    }
                },
                "required": ["feature", "endpoint_title"]
            }
        ),
        Tool(
            name="webex_api_search",
            description="Search for Webex APIs by keyword to find relevant endpoints",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (e.g., 'user', 'location', 'phone number')"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "webex_api_search":
        query = arguments.get('query', '').lower()
        results = []
        
        for feature, endpoints in api_data['endpoints'].items():
            for endpoint in endpoints:
                title = endpoint['title'].lower()
                summary = endpoint['spec']['spec'].get('summary', '').lower()
                if query in title or query in summary or query in feature.lower():
                    results.append({
                        'feature': feature,
                        'title': endpoint['title'],
                        'method': endpoint['method'],
                        'path': endpoint['path'],
                        'summary': endpoint['spec']['spec'].get('summary', '')[:100]
                    })
        
        return [TextContent(
            type="text",
            text=json.dumps({'results': results[:20], 'total_found': len(results)}, indent=2)
        )]
    
    if name == "webex_api_call":
        if not BEARER_TOKEN:
            return [TextContent(type="text", text="Error: WEBEX_ACCESS_TOKEN not set")]
        
        feature = arguments.get('feature')
        endpoint_title = arguments.get('endpoint_title')
        params = arguments.get('parameters', {})
        
        # Find endpoint
        endpoint = None
        if feature in api_data['endpoints']:
            for ep in api_data['endpoints'][feature]:
                if ep['title'] == endpoint_title:
                    endpoint = ep
                    break
        
        if not endpoint:
            return [TextContent(type="text", text=f"Error: Endpoint '{endpoint_title}' not found in feature '{feature}'")]
        
        spec = endpoint['spec']['spec']
        base_url = endpoint['spec']['meta']['servers'][0]['url'].rstrip('/')
        path = endpoint['path']
        
        # Replace path parameters
        for key, value in params.items():
            if f"{{{key}}}" in path:
                path = path.replace(f"{{{key}}}", str(value))
        
        url = base_url + path
        method = endpoint['method'].upper()
        
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        body_params = {}
        query_params = {}
        
        # Separate query params from body params
        if 'parameters' in spec:
            for param in spec['parameters']:
                param_name = param['name']
                if param_name in params and f"{{{param_name}}}" not in endpoint['path']:
                    if param.get('in') == 'query':
                        query_params[param_name] = params[param_name]
        
        # Body params
        for key, value in params.items():
            if f"{{{key}}}" not in endpoint['path'] and key not in query_params:
                body_params[key] = value
        
        logger.info(f"Executing {method} {url}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    json=body_params if body_params else None,
                    params=query_params if query_params else None
                )
                
                result = {
                    'status_code': response.status_code,
                    'body': response.json() if response.text else {}
                }
                
                logger.info(f"Action: {method} {path} | Status: {response.status_code}")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
        
        except Exception as e:
            logger.error(f"Error executing {name}: {str(e)}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    try:
        print("Starting Webex MCP Server (Resource Mode)...", file=sys.stderr)
        load_api_collection()
        print(f"Exposing {len(api_data['endpoints'])} feature resources + 2 tools", file=sys.stderr)
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
