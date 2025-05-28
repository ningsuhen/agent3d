# DDD Navigator - VS Code Extension

Navigate seamlessly between Test Cases, Features, and Requirements in documentation-driven development projects.

## Features

### 🔍 Smart Navigation
- **Go to Definition**: Ctrl+Click on any `TC-####` or `REQ-###` identifier to jump to its definition
- **Find All References**: Right-click → "Find All References" to see all mentions
- **Quick Navigation**: Use Command Palette to quickly jump to any test case, requirement, or feature

### 💡 Rich Hover Information
- **Status Indicators**: See completion status (✅ complete, ⏸️ pending, ⏭️ skipped)
- **Descriptions**: Preview content without leaving your current location
- **Reference Count**: See how many times an item is referenced
- **Related Items**: Discover connected test cases, requirements, and features

### ⚡ Quick Commands
- `Ctrl+Shift+T` (Cmd+Shift+T on Mac): Go to Test Case
- `Ctrl+Shift+R` (Cmd+Shift+R on Mac): Go to Requirement  
- `Ctrl+Shift+F` (Cmd+Shift+F on Mac): Go to Feature

### 🎯 Supported Patterns
- **Test Cases**: `TC-0001`, `TC-0101a`, `TC-1234b`
- **Requirements**: `REQ-001`, `REQ-INT-001`, `REQ-UI-123`
- **Features**: Items in FEATURES.md with `[x]` or `[ ]` markers

## Installation

### From VS Code Marketplace
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "DDD Navigator"
4. Click Install

### From Source
1. Clone this repository
2. Run `npm install`
3. Run `npm run compile`
4. Press F5 to launch Extension Development Host

## Configuration

### File Locations
Configure where the extension looks for definitions:

```json
{
    "dddNavigator.testCaseFiles": ["TEST-CASES.md", "docs/TEST-CASES.md"],
    "dddNavigator.requirementFiles": ["REQUIREMENTS.md", "docs/REQUIREMENTS.md"],
    "dddNavigator.featureFiles": ["FEATURES.md", "docs/FEATURES.md"]
}
```

### Identifier Patterns
Customize the patterns used to recognize identifiers:

```json
{
    "dddNavigator.testCasePattern": "TC-\\d{4}[a-z]*",
    "dddNavigator.requirementPattern": "REQ-[A-Z]*-?\\d{3}"
}
```

### Enable/Disable Features
```json
{
    "dddNavigator.enableTestCases": true,
    "dddNavigator.enableRequirements": true,
    "dddNavigator.enableFeatures": true
}
```

## Usage Examples

### Test Case Navigation
```markdown
<!-- In any markdown file -->
This feature is covered by TC-0001 and TC-0002a.

<!-- Ctrl+Click on TC-0001 jumps to TEST-CASES.md -->
```

### Requirement Tracing
```markdown
<!-- In REQUIREMENTS.md -->
- **REQ-001:** User Authentication
  - Priority: High
  - User Story: As a user, I want to log in securely

<!-- Reference in other files -->
The login form implements REQ-001 requirements.
```

### Feature Status
```markdown
<!-- In FEATURES.md -->
- [x] User Authentication - Complete login system (Criteria: Secure authentication)
- [ ] Password Reset - Email-based password recovery (Criteria: Secure reset flow)

<!-- Hover shows status and description -->
```

## Commands

| Command | Shortcut | Description |
|---------|----------|-------------|
| `DDD Navigator: Go to Test Case` | `Ctrl+Shift+T` | Quick picker for test cases |
| `DDD Navigator: Go to Requirement` | `Ctrl+Shift+R` | Quick picker for requirements |
| `DDD Navigator: Go to Feature` | `Ctrl+Shift+F` | Quick picker for features |
| `DDD Navigator: Show Related Items` | - | Show items related to current identifier |
| `DDD Navigator: Refresh Index` | - | Rebuild the identifier index |

## File Structure Requirements

### TEST-CASES.md
```markdown
## Test Cases

### Authentication
- [x] **TC-0001** - User login with valid credentials (Automated, High)
- [ ] **TC-0002** - User login with invalid credentials (Automated, High)
- [x] **TC-0003a** - Password reset request (Manual, Medium)
```

### REQUIREMENTS.md
```markdown
## Functional Requirements

- **REQ-001:** User Authentication
  - Priority: High
  - User Story: As a user, I want to log in securely
  - Acceptance Criteria: System validates credentials and creates session

- **REQ-UI-001:** Login Interface
  - Priority: Medium
  - User Story: As a user, I want an intuitive login form
```

### FEATURES.md
```markdown
## Core Features

- [x] User Authentication - Complete login system (Criteria: Secure authentication)
  - [x] Login Form - User interface for authentication (Criteria: Intuitive design)
  - [x] Session Management - Secure session handling (Criteria: Automatic timeout)
- [ ] Password Reset - Email-based password recovery (Criteria: Secure reset flow)
```

## Troubleshooting

### Extension Not Working
1. Ensure you're working with markdown files
2. Check that your identifier patterns match the configuration
3. Run "DDD Navigator: Refresh Index" command
4. Verify file paths in configuration match your project structure

### Identifiers Not Found
1. Check file naming matches configuration (e.g., `TEST-CASES.md`)
2. Verify identifier format matches patterns (e.g., `TC-0001` not `tc-1`)
3. Ensure files are in workspace folder

### Performance Issues
1. Exclude large directories from workspace
2. Use specific file patterns in configuration
3. Restart VS Code to rebuild index

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### 1.0.0
- Initial release
- Basic navigation for test cases and requirements
- Hover information and quick commands
- Configurable patterns and file locations
