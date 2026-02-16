# Webex Calling MCP Server

A Model Context Protocol (MCP) server that exposes the complete Webex Calling API to LLMs like Claude Desktop, enabling natural-language administrative control of Webex Calling.

## Features

- **Dynamic API Loading**: Automatically generates 967+ MCP tools from `webex_api_collection.json`
- **Full API Coverage**: Complete Webex Calling administrative API surface
- **Natural Language Control**: Perform complex Webex tasks through conversational commands
- **Local & Secure**: Runs locally with secure token handling
- **Audit Logging**: All API calls are logged for compliance

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Webex Access Token

Obtain a Webex access token from:
- [Webex Developer Portal](https://developer.webex.com/docs/getting-started)
- Use OAuth 2.0 or Personal Access Token (PAT)

Required scopes:
- `spark:calls_read` (for GET operations)
- `spark:calls_write` (for POST/PUT/DELETE operations)

### 3. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:WEBEX_ACCESS_TOKEN="your_token_here"
```

**Windows (CMD):**
```cmd
set WEBEX_ACCESS_TOKEN=your_token_here
```

**Linux/Mac:**
```bash
export WEBEX_ACCESS_TOKEN="your_token_here"
```

### 4. Configure Claude Desktop

Add to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "python",
      "args": ["c:\\Users\\Administrator\\Desktop\\WebexMCP\\server.py"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

Restart Claude Desktop to load the MCP server.

## Usage Examples

Once configured, you can use natural language commands in Claude Desktop:

### User Management
```
"Create a new Webex Calling user with email john.doe@company.com and enable voicemail"
```

### Number Management
```
"List all unassigned phone numbers in the Chicago location"
"Assign phone number +1-312-555-0100 to user john.doe@company.com"
```

### Location Configuration
```
"Show me all locations in the organization"
"Create a new location named 'Dallas Office' with timezone America/Chicago"
```

### Call Routing
```
"Configure call forwarding for user jane.smith@company.com to forward to +1-555-0199"
```

### Reporting
```
"Get call history for the last 7 days for location ID abc123"
```

## Architecture

```
┌─────────────────┐
│ Claude Desktop  │
│      (LLM)      │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│   server.py     │
│  (MCP Server)   │
└────────┬────────┘
         │
         ├─ Loads webex_api_collection.json
         ├─ Generates 967+ tools dynamically
         └─ Executes Webex API calls
                  │
         ┌────────▼────────┐
         │  Webex APIs     │
         │ webexapis.com   │
         └─────────────────┘
```

## API Coverage

The server exposes all Webex Calling APIs including:

- **Conference Controls**: Add/remove participants, mute/unmute
- **Call Controls**: Answer, reject, transfer calls
- **User Management**: Create, update, delete users
- **Location Management**: Configure locations and settings
- **Number Management**: Assign, unassign, list phone numbers
- **Call Routing**: Hunt groups, call queues, auto attendants
- **Voicemail**: Configure voicemail settings
- **Device Management**: Manage phones and devices
- **Reports**: Call history, analytics

## Logging

All API operations are logged to console with format:
```
Action: POST /telephony/config/people | Status: 200
```

## Security

- Tokens stored in environment variables (not in code)
- All operations run locally
- No cloud relay or external services
- Audit trail via logging

## Troubleshooting

### "WEBEX_ACCESS_TOKEN not set"
Ensure the environment variable is set before starting the server.

### "Tool not found"
Verify `webex_api_collection.json` is in the same directory as `server.py`.

### Authentication errors
Check that your token has the required scopes and hasn't expired.

## Updating API Definitions

To update the API collection:
1. Replace `webex_api_collection.json` with the new version
2. Restart the MCP server
3. All tools will be regenerated automatically

## Support

- [Webex Developer Documentation](https://developer.webex.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
