# Quick Reference Card

## 🚀 Quick Start (3 Steps)

1. **Install**: `pip install -r requirements.txt`
2. **Configure**: Edit `%APPDATA%\Claude\claude_desktop_config.json`
3. **Restart**: Restart Claude Desktop

## 📝 Claude Desktop Config

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

## 🔑 Get Webex Token

https://developer.webex.com/docs/api/getting-started

Required scopes:
- `spark:calls_read`
- `spark:calls_write`

## ✅ Verify Setup

```bash
python test_load.py
```

Should show: `[OK] Total Tools Generated: 967`

## 💬 Example Commands

### Users
```
"List all users"
"Create user john.doe@company.com"
"Show details for user jane.smith@company.com"
```

### Numbers
```
"List all phone numbers in Chicago"
"Assign +1-312-555-0100 to john.doe@company.com"
"Show unassigned numbers"
```

### Locations
```
"List all locations"
"Create location 'Dallas Office'"
"Show location details for Chicago"
```

### Call Routing
```
"Create hunt group 'Sales Team'"
"Add user to Support Queue"
"Configure auto attendant"
```

### Reports
```
"Show call history for last 7 days"
"Get statistics for Sales hunt group"
```

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| No tools available | Check config file path, restart Claude |
| Token error | Verify WEBEX_ACCESS_TOKEN in config |
| 401 Unauthorized | Get new token, check scopes |
| 404 Not Found | Verify resource exists first |

## 📚 Documentation

- **Setup**: QUICKSTART.md
- **Usage**: EXAMPLES.md
- **Technical**: ARCHITECTURE.md
- **Problems**: TROUBLESHOOTING.md
- **Complete**: README.md

## 🎯 Key Stats

- **Total Endpoints**: 967
- **Feature Categories**: 49
- **Setup Time**: ~5 minutes
- **Code Files**: 1 (server.py)

## 🔗 Important Links

- Webex Developer: https://developer.webex.com/
- MCP Protocol: https://modelcontextprotocol.io/
- Webex Status: https://status.webex.com/

## 📞 Support

1. Check TROUBLESHOOTING.md
2. Review error messages in Claude
3. Test with `python test_load.py`
4. Verify token at developer.webex.com

## 🎓 Learning Path

1. Read QUICKSTART.md (5 min)
2. Set up server (5 min)
3. Try simple commands (10 min)
4. Review EXAMPLES.md (15 min)
5. Explore advanced workflows (30 min)

## ⚡ Pro Tips

- Use exact email addresses for users
- Include country code in phone numbers: +1-555-0100
- List resources before modifying them
- Ask Claude to confirm destructive actions
- Check token expiration (personal tokens = 12 hours)

## 🛡️ Security Checklist

- ✅ Token in environment variable (not code)
- ✅ Local execution only
- ✅ Audit logging enabled
- ✅ Appropriate token scopes
- ✅ Regular token rotation

## 📊 API Categories (Top 10)

1. User Call Settings (90)
2. Call Settings For Me (80)
3. Workspace Call Settings (75)
4. Virtual Line Call Settings (63)
5. Device Call Settings (56)
6. Call Routing (46)
7. Location Call Settings (38)
8. Features Call Queue (37)
9. Emergency Services (26)
10. Call Controls (24)

---

**Need Help?** See TROUBLESHOOTING.md or README.md
