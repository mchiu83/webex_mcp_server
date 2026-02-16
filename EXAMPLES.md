# Webex Calling MCP - Usage Examples

This document provides real-world examples of natural language commands you can use with the Webex Calling MCP server through Claude Desktop.

## User Management

### List Users
```
"Show me all users in my Webex Calling organization"
"List users with voicemail enabled"
"Find user with email john.doe@company.com"
```

### Create Users
```
"Create a new Webex Calling user:
- Email: jane.smith@company.com
- First name: Jane
- Last name: Smith
- Location: Chicago Office
- Enable voicemail"
```

### Update Users
```
"Update user john.doe@company.com to enable call forwarding to +1-555-0199"
"Change the display name for user jane.smith@company.com to 'Jane Smith - Sales'"
```

### Delete Users
```
"Remove Webex Calling services from user old.employee@company.com"
```

## Location Management

### List Locations
```
"Show me all locations in my organization"
"List locations with their timezone settings"
```

### Create Locations
```
"Create a new location:
- Name: Dallas Office
- Address: 123 Main St, Dallas, TX
- Timezone: America/Chicago"
```

### Update Locations
```
"Update the Chicago location to use external caller ID +1-312-555-0100"
```

## Phone Number Management

### List Numbers
```
"Show me all phone numbers in the Chicago location"
"List all unassigned phone numbers"
"Find phone number +1-312-555-0100"
```

### Assign Numbers
```
"Assign phone number +1-312-555-0100 to user john.doe@company.com"
"Assign the next available number in Chicago to the Sales hunt group"
```

### Unassign Numbers
```
"Unassign phone number +1-312-555-0100 from its current user"
```

## Call Routing

### Hunt Groups
```
"Create a hunt group named 'Sales Team' with:
- Phone number: +1-312-555-0200
- Members: john.doe@company.com, jane.smith@company.com
- Call policy: Circular"

"Add user bob.jones@company.com to the Sales Team hunt group"

"Show me all hunt groups in the Chicago location"
```

### Call Queues
```
"Create a call queue named 'Support Queue' with:
- Phone number: +1-312-555-0300
- Queue size: 50
- Wait time: 300 seconds
- Overflow action: Transfer to voicemail"

"Show statistics for the Support Queue"
```

### Auto Attendants
```
"Create an auto attendant named 'Main Reception' with:
- Phone number: +1-312-555-0400
- Business hours: Monday-Friday 9am-5pm
- After hours greeting: 'Our office is currently closed'"

"Update the Main Reception auto attendant menu options"
```

## Call Settings

### Call Forwarding
```
"Enable call forwarding for john.doe@company.com to forward all calls to +1-555-0199"
"Set up selective call forwarding for jane.smith@company.com to forward calls from +1-555-0100"
"Disable call forwarding for bob.jones@company.com"
```

### Voicemail
```
"Enable voicemail for user john.doe@company.com"
"Configure voicemail settings for jane.smith@company.com:
- Send notifications to email
- Include voicemail transcription"
"Show voicemail settings for the Chicago location"
```

### Do Not Disturb
```
"Enable Do Not Disturb for john.doe@company.com"
"Disable Do Not Disturb for all users in the Sales hunt group"
```

## Device Management

### List Devices
```
"Show me all devices in the Chicago location"
"List all Cisco phones assigned to users"
"Find device with MAC address 00:11:22:33:44:55"
```

### Configure Devices
```
"Update device settings for MAC address 00:11:22:33:44:55:
- Display name: Conference Room A
- Enable hoteling"
```

## Reporting & Analytics

### Call History
```
"Show me call history for the last 7 days"
"Get call history for user john.doe@company.com for yesterday"
"Show all calls to phone number +1-312-555-0100 in the last 24 hours"
```

### Call Statistics
```
"Generate a report of total calls by location for last month"
"Show me average call duration for the Support Queue"
"Get missed call statistics for the Sales Team hunt group"
```

## Conference Controls

### Active Conferences
```
"Show me all active conferences"
"List participants in conference ID abc123"
```

### Manage Conferences
```
"Add participant +1-555-0199 to conference ID abc123"
"Mute all participants in conference ID abc123"
"Remove participant john.doe@company.com from conference ID abc123"
```

## Emergency Services

### Configure E911
```
"Configure emergency services for location Chicago Office:
- Emergency callback number: +1-312-555-0100
- Address: 123 Main St, Chicago, IL 60601"

"Show emergency service settings for all locations"
```

## Workspaces

### List Workspaces
```
"Show me all workspaces in the Chicago location"
"List conference room workspaces"
```

### Create Workspaces
```
"Create a workspace:
- Name: Conference Room A
- Location: Chicago Office
- Type: Meeting room
- Capacity: 10"
```

## Advanced Multi-Step Workflows

### Onboard New Employee
```
"Onboard a new employee:
1. Create user with email new.hire@company.com
2. Assign them to Chicago location
3. Assign phone number +1-312-555-0500
4. Enable voicemail with email notifications
5. Add them to the Sales Team hunt group
6. Configure call forwarding to mobile +1-555-0199 after 4 rings"
```

### Setup New Office Location
```
"Setup a new office location:
1. Create location 'Austin Office' with timezone America/Chicago
2. Configure emergency services with address 456 Tech Blvd, Austin, TX
3. Import 100 phone numbers with prefix +1-512-555-01XX
4. Create hunt groups for Sales, Support, and Reception
5. Setup main auto attendant with business hours menu"
```

### Decommission User
```
"Offboard employee old.employee@company.com:
1. Forward their calls to manager@company.com
2. Unassign their phone number
3. Remove them from all hunt groups and call queues
4. Export their voicemail messages
5. Disable their Webex Calling services"
```

## Tips for Best Results

1. **Be Specific**: Include all relevant details (emails, phone numbers, location names)
2. **Use Exact Names**: Reference users by their full email addresses
3. **Confirm Actions**: Ask Claude to confirm before making destructive changes
4. **Multi-Step**: Break complex workflows into clear numbered steps
5. **Check First**: List or get details before making changes

## Error Handling

If you encounter errors, Claude will explain:
- What went wrong
- Why it failed (permissions, invalid data, etc.)
- How to fix it

Example:
```
User: "Assign phone number +1-999-999-9999 to john.doe@company.com"

Claude: "I encountered an error: Phone number +1-999-999-9999 not found in your organization. 
Would you like me to:
1. List available unassigned numbers
2. Search for numbers with a different prefix
3. Add this number to your organization first"
```
