# Troubleshooting Guide

## Common Issues and Solutions

### 1. Server Not Starting

#### Symptom
Claude Desktop shows "No tools available" or server doesn't appear connected.

#### Solutions

**Check Python Installation:**
```bash
python --version
```
Should show Python 3.8 or higher.

**Verify Dependencies:**
```bash
pip install -r requirements.txt
```

**Test Server Manually:**
```bash
python test_load.py
```
Should show: `[OK] All tests passed!`

**Check File Paths:**
- Ensure `webex_api_collection.json` is in the same directory as `server.py`
- Use absolute paths in Claude Desktop config
- Windows: Use double backslashes `C:\\Users\\...`

---

### 2. Authentication Errors

#### Symptom
Error: "WEBEX_ACCESS_TOKEN not set" or "401 Unauthorized"

#### Solutions

**Verify Token is Set:**

Windows PowerShell:
```powershell
echo $env:WEBEX_ACCESS_TOKEN
```

Windows CMD:
```cmd
echo %WEBEX_ACCESS_TOKEN%
```

**Check Token in Claude Config:**
Open `%APPDATA%\Claude\claude_desktop_config.json` and verify:
```json
{
  "mcpServers": {
    "webex-calling": {
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_ACTUAL_TOKEN_HERE"
      }
    }
  }
}
```

**Get New Token:**
1. Visit https://developer.webex.com/docs/api/getting-started
2. Copy your personal access token
3. Update Claude Desktop config
4. Restart Claude Desktop

**Check Token Scopes:**
Required scopes:
- `spark:calls_read` (for GET operations)
- `spark:calls_write` (for POST/PUT/DELETE operations)

---

### 3. API Call Failures

#### Symptom
Error: "404 Not Found" or "400 Bad Request"

#### Solutions

**Check Parameter Format:**
- User emails must be valid email addresses
- Phone numbers should include country code: `+1-555-0100`
- IDs must be exact (no typos)

**Verify Resource Exists:**
Before updating/deleting, verify the resource exists:
```
"Show me user john.doe@company.com"
```

**Check Permissions:**
Your Webex account must have admin permissions for the operation.

**Review API Response:**
Ask Claude to show the full error response for details.

---

### 4. Claude Desktop Not Recognizing Server

#### Symptom
Claude doesn't show Webex tools or says server is unavailable.

#### Solutions

**Restart Claude Desktop:**
1. Completely quit Claude Desktop (check system tray)
2. Wait 5 seconds
3. Restart Claude Desktop

**Verify Config File Location:**

Windows:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Mac:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Check Config Syntax:**
- Valid JSON format (use a JSON validator)
- No trailing commas
- Proper quotes and brackets

**View Claude Logs:**

Windows:
```
%APPDATA%\Claude\logs\
```

Mac:
```
~/Library/Logs/Claude/
```

---

### 5. Slow Performance

#### Symptom
API calls take a long time or timeout.

#### Solutions

**Check Network Connection:**
Ensure stable internet connection to webexapis.com

**Verify API Status:**
Check Webex API status: https://status.webex.com/

**Increase Timeout:**
Edit `server.py` line with `httpx.AsyncClient`:
```python
async with httpx.AsyncClient(timeout=60.0) as client:  # Increase from 30 to 60
```

---

### 6. Missing Tools

#### Symptom
Some Webex API operations aren't available.

#### Solutions

**Verify API Collection:**
```bash
python test_load.py
```
Should show 967 endpoints.

**Check File Integrity:**
Ensure `webex_api_collection.json` is complete and not corrupted.

**Reload Server:**
Restart Claude Desktop to reload all tools.

---

### 7. Unicode/Encoding Errors

#### Symptom
Errors with special characters or non-English text.

#### Solutions

**Ensure UTF-8 Encoding:**
The server uses UTF-8 by default. If issues persist, check your terminal encoding.

**Avoid Special Characters:**
Use standard ASCII characters for names and identifiers when possible.

---

### 8. Permission Denied Errors

#### Symptom
Error: "403 Forbidden" or "You don't have permission"

#### Solutions

**Check Admin Rights:**
Your Webex account must have appropriate admin permissions.

**Verify Organization Access:**
Ensure you're accessing resources in your organization.

**Check Token Scopes:**
Personal access tokens have full permissions, but OAuth tokens need correct scopes.

---

### 9. Rate Limiting

#### Symptom
Error: "429 Too Many Requests"

#### Solutions

**Wait and Retry:**
Webex APIs have rate limits. Wait 60 seconds and try again.

**Reduce Request Frequency:**
Batch operations when possible instead of individual calls.

**Check Rate Limits:**
Webex typically allows:
- 100 requests per minute per token
- 10,000 requests per day per token

---

### 10. Installation Issues

#### Symptom
`pip install` fails or dependencies won't install.

#### Solutions

**Upgrade pip:**
```bash
python -m pip install --upgrade pip
```

**Install with Verbose Output:**
```bash
pip install -r requirements.txt -v
```

**Use Virtual Environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Check Python Version:**
Requires Python 3.8+. Upgrade if necessary.

---

## Diagnostic Commands

### Test API Collection Loading
```bash
python test_load.py
```

### Test Python Environment
```bash
python -c "import mcp; import httpx; print('Dependencies OK')"
```

### Check File Paths
```bash
dir server.py
dir webex_api_collection.json
```

### Verify JSON Syntax
```bash
python -m json.tool webex_api_collection.json > nul
```
No output = valid JSON

---

## Getting Help

### Check Logs
Server logs show detailed information about each API call:
```
INFO: Executing POST /telephony/config/people
INFO: Action: POST /telephony/config/people | Status: 200
```

### Enable Debug Logging
Edit `server.py` line 7:
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

### Test Individual Endpoints
Ask Claude to test specific operations:
```
"Test the connection by listing all locations"
```

### Verify Token Validity
```
"Make a simple API call to verify my token is working"
```

---

## Still Having Issues?

1. **Review Documentation:**
   - README.md - Complete documentation
   - QUICKSTART.md - Setup guide
   - ARCHITECTURE.md - Technical details
   - EXAMPLES.md - Usage examples

2. **Check Webex Status:**
   - https://status.webex.com/

3. **Webex Developer Support:**
   - https://developer.webex.com/support

4. **MCP Documentation:**
   - https://modelcontextprotocol.io/

5. **Verify Prerequisites:**
   - Python 3.8+
   - Valid Webex token
   - Claude Desktop installed
   - Network access to webexapis.com
