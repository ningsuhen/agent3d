# Testing Guide - VS Code DDD Navigator Extension

This document describes the comprehensive test suite for the VS Code DDD Navigator extension.

## Test Structure

```
src/test/
├── runTest.ts              # Test runner configuration
├── suite/
│   ├── index.ts           # Test suite index
│   └── extension.test.ts  # Main integration tests
└── fixtures/              # Test data files
    ├── TEST-CASES.md      # Sample test cases
    ├── REQUIREMENTS.md    # Sample requirements
    └── sample.js          # Code file with references
```

## Test Categories

### 1. Identifier Index Tests
- **Index Building**: Verifies that the extension can scan and index identifiers from multiple files
- **Format Support**: Tests various identifier formats:
  - `TC-0001` (basic format)
  - `TC-0003a` (with lowercase suffix)
  - `TC-ENV-002` (with category prefix)
  - `TC-BATCH-001` (batch category)
  - `REQ-001`, `REQ-AUTH-001` (requirements)
- **Cross-File References**: Ensures references are found across different file types

### 2. Definition Provider Tests
- **Go-to-Definition**: Tests Cmd+Click navigation to identifier definitions
- **Multi-File Support**: Verifies navigation works from any file type (.md, .js, .ts, etc.)
- **Complex Formats**: Tests navigation for complex identifier patterns
- **Performance**: Ensures definition lookup completes within 100ms

### 3. Hover Provider Tests
- **Hover Information**: Tests that hovering shows identifier details
- **Status Indicators**: Verifies correct status icons (✅, ⏸️, ⏭️)
- **Content Accuracy**: Ensures hover shows correct type, description, and location
- **Performance**: Ensures hover response within 50ms

### 4. Reference Provider Tests
- **Find All References**: Tests right-click "Find All References" functionality
- **Cross-File References**: Verifies references are found across multiple files
- **File Type Support**: Tests references in markdown, JavaScript, TypeScript, etc.
- **Include Declaration**: Tests both with and without declaration inclusion

### 5. Performance Tests
- **Index Building**: Must complete within 5 seconds for test fixtures
- **Definition Lookup**: Must complete within 100ms
- **Hover Response**: Must complete within 50ms
- **Memory Usage**: Monitors extension memory footprint

## Test Data

### Test Cases (TEST-CASES.md)
```markdown
- [x] **TC-0001** - User login with valid credentials (Automated, High)
- [ ] **TC-0003a** - User login with expired session (Manual, Medium)
- [x] **TC-ENV-001** - Environment variable configuration (Automated, High)
- [ ] **TC-ENV-002** - Environment Map Configuration (Environment, High Priority) ⏸️
- [ ] **TC-BATCH-001** - Parallel execution strategy (Batching, High Priority) ⏸️
- [x] **TC-SYNC-001** - Data synchronization between services (Automated, High)
```

### Requirements (REQUIREMENTS.md)
```markdown
- **REQ-001:** User Authentication
- **REQ-AUTH-001:** Multi-factor Authentication
- **REQ-ENV-001:** Environment Configuration
- **REQ-BATCH-001:** Parallel Processing
```

### Code References (sample.js)
```javascript
// Tests that extension works in code files
// Implements REQ-001 and REQ-AUTH-001
// Tested by TC-0001, TC-0002, TC-0003a
class UserAuth {
    // TC-ENV-001: Environment configuration
    // TC-BATCH-001: Parallel execution strategy
}
```

## Running Tests

### Quick Test Run
```bash
./test.sh
```

### Manual Test Steps
```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Run linter
npm run lint

# Run tests
npm test
```

### VS Code Test Runner
1. Open the extension in VS Code
2. Press `F5` to launch Extension Development Host
3. Run tests from Command Palette: "Tasks: Run Test Task"

## Test Scenarios

### Identifier Recognition
- [x] Basic format: `TC-0001`, `REQ-001`
- [x] With categories: `TC-ENV-002`, `REQ-AUTH-001`
- [x] With suffixes: `TC-0003a`
- [x] Complex patterns: `TC-BATCH-001`, `TC-SYNC-001`
- [x] Case sensitivity: Supports both uppercase and lowercase

### Navigation Features
- [x] Cmd+Click goes to definition
- [x] Hover shows identifier information
- [x] Right-click "Find All References" works
- [x] Quick navigation commands (Cmd+Shift+T, Cmd+Shift+R)
- [x] Multiple reference picker when multiple locations exist

### File Type Support
- [x] Markdown files (.md)
- [x] JavaScript files (.js)
- [x] TypeScript files (.ts)
- [x] Python files (.py)
- [x] Java files (.java)
- [x] Go files (.go)
- [x] Text files (.txt)

### Status Indicators
- [x] ✅ Complete (marked with [x])
- [x] ⏸️ Pending (marked with [ ])
- [x] ⏭️ Skipped (explicitly marked)
- [x] ❓ Unknown status

### Performance Benchmarks
- [x] Index building: < 5 seconds (test fixtures)
- [x] Definition lookup: < 100ms
- [x] Hover response: < 50ms
- [x] Reference finding: < 200ms
- [x] Memory usage: < 50MB for typical projects

## Continuous Integration

### GitHub Actions (Future)
```yaml
name: Test Extension
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm test
```

### Local Pre-commit Hooks
```bash
# Install pre-commit hooks
npm install husky --save-dev
npx husky install
npx husky add .husky/pre-commit "npm test"
```

## Test Coverage Goals

- **Identifier Recognition**: 100% of supported patterns
- **Navigation Features**: 100% of core functionality
- **File Type Support**: 95% of common development files
- **Performance**: All benchmarks met
- **Error Handling**: 90% of error scenarios covered

## Debugging Tests

### VS Code Debug Configuration
```json
{
    "name": "Extension Tests",
    "type": "extensionHost",
    "request": "launch",
    "args": [
        "--extensionDevelopmentPath=${workspaceFolder}",
        "--extensionTestsPath=${workspaceFolder}/out/test/suite/index"
    ],
    "outFiles": ["${workspaceFolder}/out/test/**/*.js"]
}
```

### Common Issues
1. **Tests fail to find fixtures**: Ensure test fixtures are in `src/test/fixtures/`
2. **Extension not activated**: Check that extension ID matches in tests
3. **Timeout errors**: Increase timeout for slow operations
4. **Path issues**: Use `path.resolve()` for cross-platform compatibility

## Contributing Tests

When adding new features:
1. Add test fixtures to `src/test/fixtures/`
2. Write integration tests in `src/test/suite/`
3. Update performance benchmarks if needed
4. Run full test suite before submitting PR
5. Update this documentation

## Test Results

Expected output:
```
🧪 Running VS Code DDD Navigator Extension Tests...
📦 Installing test dependencies...
🔨 Compiling TypeScript...
🧹 Running linter...
🧪 Running integration tests...

  DDD Navigator Extension Test Suite
    Identifier Index Tests
      ✓ Should build index from test fixtures
      ✓ Should find test cases with various formats
      ✓ Should find requirements with various formats
      ✓ Should find references across multiple files
    Definition Provider Tests
      ✓ Should provide definition for test case identifiers
      ✓ Should provide definition for requirement identifiers
      ✓ Should work with identifiers in code files
      ✓ Should handle complex identifier formats
    Hover Provider Tests
      ✓ Should provide hover information for test cases
      ✓ Should provide hover information for requirements
      ✓ Should show status indicators in hover
    Reference Provider Tests
      ✓ Should find all references for test cases
      ✓ Should find references across different file types
    Performance Tests
      ✓ Index building should complete within reasonable time
      ✓ Definition lookup should be fast
      ✓ Hover provider should be responsive

  16 passing (2.3s)

✅ All tests completed successfully!
```
