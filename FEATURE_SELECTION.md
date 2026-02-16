# Feature Selection Guide

## Problem
Claude Desktop has a context limit that can be exceeded when loading all 967 Webex API endpoints at once.

## Solution
Use the graphical configuration UI to select only the API features you need.

## Quick Start

### 1. Launch Configuration UI

**Windows:**
```bash
configure.bat
```

**Or manually:**
```bash
python config_server.py
```

### 2. Open Browser
Navigate to: **http://localhost:5000**

### 3. Select Features
- Browse the 49 available feature categories
- Toggle features on/off with the switch
- Click feature names to see endpoint details
- Use search to find specific features quickly

### 4. Save Configuration
Click **"💾 Save Configuration"** button

### 5. Restart Claude Desktop
Your selection persists across sessions until you change it.

## Features

### Visual Interface
- **Beautiful UI**: Modern, gradient design
- **Real-time Stats**: See total vs enabled endpoints
- **Search**: Quickly find features
- **Expand Details**: Click features to see all endpoints
- **Bulk Actions**: Select All / Deselect All buttons

### Persistent Configuration
- Saves to `enabled_features.json`
- Automatically loaded by MCP server
- Survives restarts
- Easy to modify anytime

### Smart Filtering
- Only enabled features load into Claude
- Reduces context size significantly
- Maintains full API library intact
- No need to modify JSON files

## Recommended Configurations

### Minimal (50-100 endpoints)
Enable only:
- People
- Locations
- Numbers
- Call Controls

### Standard (200-300 endpoints)
Add:
- User Call Settings
- Location Call Settings
- Device Call Settings
- Call Routing

### Full (967 endpoints)
Enable all features (may hit context limits)

## Tips

1. **Start Small**: Enable 5-10 features initially
2. **Test**: Restart Claude and verify it works
3. **Expand**: Add more features as needed
4. **Monitor**: Check Claude's response for context warnings

## Workflow

```
1. Run configure.bat
2. Select features in browser
3. Click Save
4. Restart Claude Desktop
5. Test with Claude
6. Adjust as needed (repeat)
```

## File Structure

```
enabled_features.json  ← Your selections saved here
config_server.py       ← Flask web server
templates/
  └── config.html      ← Web UI
configure.bat          ← Quick launcher
```

## Troubleshooting

### "Context size exceeds limit"
- Open config UI
- Disable some features
- Save and restart Claude

### "No tools available"
- Ensure at least one feature is enabled
- Check `enabled_features.json` exists
- Restart Claude Desktop

### Config UI won't start
- Install Flask: `pip install flask`
- Check port 5000 is available
- Run: `python config_server.py`

## Advanced

### Manual Configuration
Edit `enabled_features.json` directly:
```json
{
  "People": true,
  "Locations": true,
  "Numbers": false,
  "Call Controls": true
}
```

### Reset to All Features
Delete `enabled_features.json` and restart server.

### Check Current Selection
```bash
python -c "import json; print(json.load(open('enabled_features.json')))"
```
