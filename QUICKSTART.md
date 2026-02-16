# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Claude Desktop installed
- Webex account with API access

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your Webex Access Token

Visit: https://developer.webex.com/docs/getting-started

**For Testing (Quick):**
- Go to https://developer.webex.com/docs/api/getting-started
- Copy your personal access token (valid for 12 hours)

**For Production (Recommended):**
- Create an OAuth integration
- Required scopes: `spark:calls_read`, `spark:calls_write`

### 3. Test the Server

```bash
# Set your token
set WEBEX_ACCESS_TOKEN=your_token_here

# Test API loading
python test_load.py
```

You should see:
```
[OK] Total Endpoints: 967
[OK] Total Tools Generated: 967
[OK] All tests passed!
```

### 4. Configure Claude Desktop

**Find your config file:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Add this configuration:**

```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "python",
      "args": ["C:\\Users\\Administrator\\Desktop\\WebexMCP\\server.py"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**Important:** 
- Use full absolute path to server.py
- Replace `YOUR_TOKEN_HERE` with your actual token
- Use double backslashes (\\) in Windows paths

### 5. Restart Claude Desktop

Completely quit and restart Claude Desktop.

### 6. Verify Connection

In Claude Desktop, type:
```
What Webex Calling tools do you have available?
```

Claude should respond with information about the 967 available Webex Calling API tools.

## Example Commands

Try these natural language commands:

```
"List all locations in my Webex organization"

"Show me the details for user john.doe@company.com"

"Get all phone numbers assigned to the Chicago location"

"Create a new hunt group named 'Sales Team'"

"Show me call history for the last 24 hours"
```

## Troubleshooting

### "No tools available"
- Check that server.py path is correct in config
- Verify webex_api_collection.json is in the same folder as server.py
- Restart Claude Desktop

### "WEBEX_ACCESS_TOKEN not set"
- Verify token is in claude_desktop_config.json
- Check for typos in the token
- Ensure token hasn't expired (personal tokens expire after 12 hours)

### "Authentication failed"
- Verify your token has the required scopes
- Try generating a new token
- Check that your Webex account has admin permissions

### Server not starting
- Run `python test_load.py` to check for errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## Next Steps

Once configured, you can:
- Manage users and workspaces
- Configure call routing and hunt groups
- Assign and manage phone numbers
- Set up voicemail and call forwarding
- Generate reports and analytics
- Configure emergency services
- Manage devices and locations

See README.md for complete documentation.
