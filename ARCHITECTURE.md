# Webex Calling MCP - Architecture

## System Overview

The Webex Calling MCP server is a Python-based Model Context Protocol server that dynamically exposes 967 Webex Calling API endpoints as MCP tools, enabling natural-language administrative control through Claude Desktop.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Desktop                         │
│                         (Client)                            │
│  - Natural language interface                               │
│  - Intent interpretation                                    │
│  - Multi-step workflow orchestration                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ MCP Protocol (stdio)
                         │ - Tool discovery
                         │ - Tool invocation
                         │ - Structured responses
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    server.py (MCP Server)                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Initialization                                     │   │
│  │  - Load webex_api_collection.json                   │   │
│  │  - Parse 967 endpoints across 49 features           │   │
│  │  - Generate tool definitions dynamically            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Tool Discovery (@server.list_tools)                │   │
│  │  - Return all 967 tool definitions                  │   │
│  │  - Include schemas, descriptions, parameters        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Tool Execution (@server.call_tool)                 │   │
│  │  - Validate tool name and parameters                │   │
│  │  - Build HTTP request (method, URL, headers, body)  │   │
│  │  - Execute API call with Bearer token               │   │
│  │  - Parse and return response                        │   │
│  │  - Log action for audit trail                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS (Bearer Token Auth)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Webex Calling APIs                         │
│                  (webexapis.com/v1)                         │
│                                                             │
│  - User Management                                          │
│  - Location Management                                      │
│  - Number Management                                        │
│  - Call Routing (Hunt Groups, Queues, Auto Attendants)     │
│  - Device Management                                        │
│  - Call Settings (Forwarding, Voicemail, DND)              │
│  - Conference Controls                                      │
│  - Emergency Services                                       │
│  - Reporting & Analytics                                    │
│  - And 40+ more feature categories                         │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. webex_api_collection.json
**Purpose**: Complete API specification database

**Structure**:
```json
{
  "version": "1.0",
  "total_endpoints": 967,
  "endpoints": {
    "Feature Name": [
      {
        "id": "unique_id",
        "title": "Endpoint Title",
        "method": "GET|POST|PUT|DELETE",
        "path": "/api/path/{param}",
        "spec": {
          "spec": {
            "summary": "Brief description",
            "description": "Detailed description",
            "parameters": [...],
            "requestBody": {...},
            "responses": {...}
          }
        }
      }
    ]
  }
}
```

**Key Features**:
- Pre-scraped from Webex Developer Portal
- Complete OpenAPI 3.0 specifications
- Includes all parameters, schemas, and descriptions
- Easily updatable without code changes

### 2. server.py
**Purpose**: MCP server implementation

**Key Functions**:

#### load_api_collection()
- Loads JSON file at startup
- Parses all endpoints
- Creates tool name mappings
- Generates 967 tool definitions

#### create_tool_from_endpoint()
- Converts API spec to MCP Tool schema
- Extracts parameters from OpenAPI spec
- Builds input schema with types and descriptions
- Handles both query parameters and request bodies

#### @server.list_tools()
- MCP protocol handler for tool discovery
- Returns all 967 tools with full schemas
- Called by Claude Desktop on connection

#### @server.call_tool()
- MCP protocol handler for tool execution
- Validates tool name and parameters
- Constructs HTTP request:
  - Method: GET, POST, PUT, DELETE
  - URL: Base URL + path with parameter substitution
  - Headers: Authorization (Bearer token), Content-Type
  - Body: JSON payload for POST/PUT
  - Query params: For GET requests
- Executes API call via httpx
- Returns structured response
- Logs all actions

### 3. Authentication Flow

```
┌──────────────┐
│ User obtains │
│ Webex Token  │
│ (OAuth/PAT)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Token stored in      │
│ Environment Variable │
│ WEBEX_ACCESS_TOKEN   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Claude Desktop       │
│ passes token to      │
│ server.py via env    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ server.py includes   │
│ token in every       │
│ API request header   │
│ Authorization:       │
│ Bearer {token}       │
└──────────────────────┘
```

### 4. Request Flow

```
1. User → Claude Desktop
   "Create a user john.doe@company.com"

2. Claude Desktop → server.py (MCP)
   Tool: people_create_a_person
   Params: {
     "emails": ["john.doe@company.com"],
     "firstName": "John",
     "lastName": "Doe"
   }

3. server.py → Webex API
   POST https://webexapis.com/v1/people
   Headers: {
     "Authorization": "Bearer {token}",
     "Content-Type": "application/json"
   }
   Body: {
     "emails": ["john.doe@company.com"],
     "firstName": "John",
     "lastName": "Doe"
   }

4. Webex API → server.py
   Response: {
     "id": "user123",
     "emails": ["john.doe@company.com"],
     "displayName": "John Doe",
     ...
   }

5. server.py → Claude Desktop
   {
     "status_code": 200,
     "body": { ... }
   }

6. Claude Desktop → User
   "Successfully created user John Doe with email john.doe@company.com"
```

## Dynamic Tool Generation

The server automatically generates MCP tools from the API collection:

```python
# Tool name generation
feature = "People"
title = "Create a Person"
tool_name = "people_create_a_person"

# Schema extraction
spec = endpoint['spec']['spec']
parameters = spec.get('parameters', [])
request_body = spec.get('requestBody', {})

# MCP Tool creation
Tool(
    name=tool_name,
    description=f"[{feature}] {title}: {description}",
    inputSchema={
        "type": "object",
        "properties": {...},
        "required": [...]
    }
)
```

## Security Architecture

### Token Security
- Tokens stored in environment variables (never in code)
- Passed securely from Claude Desktop to server
- Never logged or exposed
- Support for OAuth tokens (recommended) or PATs

### Local Execution
- All processing runs locally on user's machine
- No cloud relay or external services
- Direct communication with Webex APIs
- Full control over data flow

### Audit Logging
- All API calls logged with:
  - Timestamp
  - HTTP method and path
  - Response status code
- Logs stored locally for compliance
- No sensitive data in logs

### Role-Based Access
- Controlled by Webex token scopes
- `spark:calls_read` for GET operations
- `spark:calls_write` for POST/PUT/DELETE
- Webex enforces permissions server-side

## Extensibility

### Adding New APIs
1. Update webex_api_collection.json with new endpoints
2. Restart server
3. New tools automatically available

### Custom Features
- Add custom logging handlers
- Implement rate limiting
- Add request/response transformations
- Integrate with other systems

### Multi-API Support
- Architecture supports multiple API collections
- Can load additional JSON files
- Namespace tools by API source

## Performance Considerations

### Startup Time
- Loads 967 endpoints in <1 second
- Minimal memory footprint (~50MB)
- Fast tool discovery

### Request Latency
- Direct API calls (no middleware)
- Async HTTP client (httpx)
- Typical response time: 200-500ms

### Scalability
- Handles concurrent requests
- No state management required
- Stateless design

## Error Handling

### API Errors
- HTTP status codes passed through
- Error messages from Webex preserved
- Structured error responses

### Authentication Errors
- Clear error messages for missing/invalid tokens
- Guidance on token renewal

### Validation Errors
- Parameter validation via MCP schemas
- Type checking before API calls

## Monitoring & Observability

### Logging
```
INFO: Loaded 967 API endpoints
INFO: Executing POST /telephony/config/people
INFO: Action: POST /telephony/config/people | Status: 200
```

### Metrics (Future)
- API call counts by endpoint
- Success/failure rates
- Response time distributions
- Token expiration tracking

## Deployment Models

### Development
- Run directly with Python
- Token in environment variable
- Console logging

### Production
- Systemd service (Linux)
- Windows Service
- Docker container
- Token from secrets manager

## Future Enhancements

1. **Caching**: Cache GET responses for performance
2. **Rate Limiting**: Respect Webex API rate limits
3. **Batch Operations**: Support bulk operations
4. **Webhooks**: Real-time event notifications
5. **Multi-Tenant**: Support multiple Webex orgs
6. **GUI**: Web-based management interface
