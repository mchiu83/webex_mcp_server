import json
import os
import sys
import logging
from typing import Any
from pathlib import Path
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("webex-mcp")

server = Server("webex-calling-mcp")

# Use absolute path to JSON file
SCRIPT_DIR = Path(__file__).parent.absolute()
API_COLLECTION_PATH = SCRIPT_DIR / "webex_api_collection.json"
ENABLED_FEATURES_PATH = SCRIPT_DIR / "enabled_features.json"
BEARER_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN", "")

import re

api_data = {}
tools_map = {}

def sanitize_name(text: str) -> str:
    """Remove invalid characters and ensure valid tool name"""
    # Replace spaces and invalid chars with underscore
    text = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    # Remove consecutive underscores
    text = re.sub(r'_+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    return text.lower()

def load_api_collection():
    global api_data, tools_map
    print(f"Loading API collection from: {API_COLLECTION_PATH}", file=sys.stderr)
    with open(API_COLLECTION_PATH, 'r', encoding='utf-8') as f:
        api_data = json.load(f)
    
    # Load enabled features filter
    enabled_features = {}
    if ENABLED_FEATURES_PATH.exists():
        with open(ENABLED_FEATURES_PATH, 'r') as f:
            enabled_features = json.load(f)
        print(f"Loaded feature filter: {sum(1 for v in enabled_features.values() if v)} features enabled", file=sys.stderr)
    
    for feature, endpoints in api_data['endpoints'].items():
        # Skip if feature is not enabled (when filter exists)
        if enabled_features and not enabled_features.get(feature, False):
            continue
            
        for endpoint in endpoints:
            # Create valid tool name (only a-zA-Z0-9_- allowed, max 64 chars)
            feature_clean = sanitize_name(feature)[:20]
            title_clean = sanitize_name(endpoint['title'])[:40]
            tool_name = f"{feature_clean}_{title_clean}"[:64]
            tools_map[tool_name] = {
                'feature': feature,
                'endpoint': endpoint
            }
    logger.info(f"Loaded {len(tools_map)} API endpoints")

def create_tool_from_endpoint(tool_name: str, feature: str, endpoint: dict) -> Tool:
    spec = endpoint['spec']['spec']
    # Use only summary, keep it short
    description = spec.get('summary', endpoint['title'])[:100]
    
    input_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    
    if 'parameters' in spec:
        for param in spec['parameters']:
            param_name = param['name']
            param_schema = param.get('schema', {})
            input_schema['properties'][param_name] = {
                "type": param_schema.get('type', 'string'),
                "description": param.get('description', '')[:50]  # Limit description length
            }
            if param.get('required', False):
                input_schema['required'].append(param_name)
    
    if 'requestBody' in spec:
        content = spec['requestBody'].get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        
        if 'properties' in schema:
            for prop_name, prop_schema in schema['properties'].items():
                input_schema['properties'][prop_name] = {
                    "type": prop_schema.get('type', 'string'),
                    "description": prop_schema.get('description', '')[:50]  # Limit description length
                }
        
        if 'required' in schema:
            input_schema['required'].extend(schema['required'])
    
    return Tool(
        name=tool_name,
        description=description,
        inputSchema=input_schema
    )

@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    for tool_name, data in tools_map.items():
        tool = create_tool_from_endpoint(tool_name, data['feature'], data['endpoint'])
        tools.append(tool)
    return tools

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name not in tools_map:
        return [TextContent(type="text", text=f"Error: Tool '{name}' not found")]
    
    if not BEARER_TOKEN:
        return [TextContent(type="text", text="Error: WEBEX_ACCESS_TOKEN not set")]
    
    tool_data = tools_map[name]
    endpoint = tool_data['endpoint']
    spec = endpoint['spec']['spec']
    
    base_url = endpoint['spec']['meta']['servers'][0]['url'].rstrip('/')
    path = endpoint['path']
    
    for key, value in arguments.items():
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
    
    if 'parameters' in spec:
        for param in spec['parameters']:
            param_name = param['name']
            if param_name in arguments and f"{{{param_name}}}" not in endpoint['path']:
                if param.get('in') == 'query':
                    query_params[param_name] = arguments[param_name]
    
    if 'requestBody' in spec:
        for key, value in arguments.items():
            if f"{{{key}}}" not in endpoint['path']:
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

async def main():
    try:
        print("Starting Webex MCP Server...", file=sys.stderr)
        load_api_collection()
        print(f"Loaded {len(tools_map)} tools", file=sys.stderr)
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
