# Webex MCP Server - Mode Selection Guide

## Two Modes Available

### 1. Traditional Mode (server.py)
**Best for**: Specific feature sets, explicit control

- Loads selected features as individual tools
- Requires feature selection via web UI
- Limited by Claude's context window
- Direct tool invocation

### 2. Smart Mode (server_smart.py) ⭐ RECOMMENDED
**Best for**: Full API access, multi-step workflows

- Loads only 2 tools + 50 resources
- No feature selection needed
- All 967 APIs available
- Claude discovers APIs on-demand

## Quick Comparison

| Aspect | Traditional | Smart |
|--------|------------|-------|
| **Tools Loaded** | 50-967 | 2 |
| **Context Usage** | High | Minimal |
| **Setup Required** | Feature selection | None |
| **API Coverage** | Selected only | All 967 |
| **Multi-Step** | Manual | Automatic |
| **Best For** | Simple tasks | Complex workflows |

## How Smart Mode Works

Instead of loading all APIs as tools, Smart Mode:

1. **Exposes 2 Generic Tools:**
   - `webex_api_search` - Find APIs by keyword
   - `webex_api_call` - Execute any API

2. **Provides 50 Resources:**
   - API catalog with all endpoints
   - Feature-specific documentation
   - Read on-demand by Claude

3. **Claude Orchestrates:**
   - Searches for needed APIs
   - Reads specifications
   - Executes in sequence
   - Handles dependencies

## Example: Smart Mode in Action

**User Request:**
```
"Create user john.doe@company.com and assign phone number +1-312-555-0100"
```

**Claude's Process:**
1. Search: "create user" → Finds "Create a Person" API
2. Execute: Create user with email
3. Search: "assign phone number" → Finds "Update Person" API
4. Execute: Assign number to user
5. Report: Success with details

**All without loading 967 tools!**

## Setup Instructions

### Switch to Smart Mode (Recommended)

1. **Update Claude Config:**
   Edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "webex-calling": {
         "command": "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe",
         "args": ["c:\\Users\\Administrator\\Desktop\\WebexMCP\\server_smart.py"],
         "env": {
           "WEBEX_ACCESS_TOKEN": "your_token_here"
         }
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Test:**
   ```
   "Search for APIs related to users"
   "List all locations in my organization"
   ```

### Use Traditional Mode

1. **Run Feature Selector:**
   ```bash
   configure.bat
   ```

2. **Select Features** in browser (http://localhost:5000)

3. **Update Claude Config** to use `server.py`

4. **Restart Claude Desktop**

## When to Use Each Mode

### Use Smart Mode When:
- ✅ You need access to all APIs
- ✅ You want multi-step workflows
- ✅ You hit context limits
- ✅ You want Claude to discover APIs
- ✅ You're doing complex automation

### Use Traditional Mode When:
- You only need 5-10 specific features
- You want explicit tool names
- You prefer manual control
- You're doing simple, repetitive tasks

## Performance

### Smart Mode
- Startup: <1 second
- Memory: ~30MB
- Tools: 2
- Resources: 50
- API Coverage: 100%

### Traditional Mode
- Startup: 1-2 seconds
- Memory: ~50-100MB
- Tools: 50-967
- Resources: 0
- API Coverage: Selected features only

## Recommendation

**Start with Smart Mode** - it provides:
- Full API access without context limits
- Intelligent multi-step workflows
- No configuration needed
- Better scalability

Switch to Traditional Mode only if you have specific requirements for explicit tool control.

## Files

- `server_smart.py` - Smart mode server
- `server.py` - Traditional mode server
- `config_server.py` - Feature selection UI
- `SMART_MODE.md` - Smart mode documentation
- `FEATURE_SELECTION.md` - Traditional mode setup

## Support

Both modes use the same:
- API collection (`webex_api_collection.json`)
- Authentication (WEBEX_ACCESS_TOKEN)
- Logging and error handling

Switch between modes anytime by updating Claude config!
