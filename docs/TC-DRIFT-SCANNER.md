# Multi-Mode Drift Scanner

**Comprehensive drift detection tool for Agent3D framework with multiple analysis modes.**

## Overview

The Multi-Mode Drift Scanner is a comprehensive tool that analyzes various types of drift between documentation and implementation across multiple programming languages. It supports multiple analysis modes:

### Analysis Modes

- **tc-mapping** - TC ID mapping between TEST-CASES.md and test implementations
- **code-coverage** - Test coverage analysis and missing test detection
- **feature-impl** - Feature implementation status drift between FEATURES.md and code
- **all** - Comprehensive analysis running all drift detection modes

### Drift Types Detected

**TC ID Mapping Drift:**
- **Test cases without implementations** - TC IDs documented but not implemented
- **Implementations without TC IDs** - Test functions missing TC ID references
- **Orphaned TC IDs** - TC IDs in code but not in TEST-CASES.md
- **Successful mappings** - Proper 1:1 documentation-to-implementation alignment

**Code Coverage Drift:**
- **Missing test files** - Source files without corresponding test files
- **Untested functions** - Public functions without test coverage
- **Orphaned tests** - Test functions without corresponding source functions
- **Coverage percentage** - Overall test coverage metrics

**Feature Implementation Drift:**
- **Status mismatches** - Features marked complete but not implemented
- **Missing implementations** - Documented features without code
- **Undocumented features** - Implemented features not in FEATURES.md
- **Priority conflicts** - Implementation priority vs documented priority

## Supported Languages

- **Python** - `test_*.py`, `*_test.py`, pytest patterns
- **JavaScript/TypeScript** - `*.test.js`, `*.spec.js`, Jest/Mocha patterns
- **Java** - `*Test.java`, `*Tests.java`, JUnit patterns
- **Go** - `*_test.go`, standard Go test patterns
- **Rust** - `#[test]` annotated functions

## Usage

### Prerequisites

**CRITICAL:** The drift scanner must be run from the DDD project root directory (where `.agent3d-config.yaml` is located), not from the Agent3D framework directory.

### Basic Usage

```bash
# Navigate to your DDD project root first
cd /path/to/your/ddd-project

# TC ID mapping analysis (default)
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping

# Code coverage analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode code-coverage

# Feature implementation analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode feature-impl

# Comprehensive analysis (all modes)
python3 ~/.agent3d/tools/drift_scanner.py --mode all

# Custom TEST-CASES.md location
python3 ~/.agent3d/tools/drift_scanner.py --test-cases-file docs/custom-test-cases.md

# Custom output file (default: auto-generated in .agent3d-tmp/drift-reports/)
python3 ~/.agent3d/tools/drift_scanner.py --output my-drift-report.yaml

# Quiet mode (minimal output)
python3 ~/.agent3d/tools/drift_scanner.py --quiet
```

### Agent Guidelines

**For LLM Agents:**
1. **Always run from DDD project root** - The directory containing `.agent3d-config.yaml`
2. **Use full path to drift scanner** - `~/.agent3d/tools/drift_scanner.py`
3. **Do NOT copy the tool** - Run it directly from the Agent3D framework location
4. **Check working directory** - Ensure you're in the correct project directory before running
5. **Use MCP wrapper** - For easier integration, use the drift scanner MCP tool

### MCP Wrapper Usage

For easier integration, use the MCP wrapper that automatically handles DDD project root detection:

**Prerequisites:**
```bash
# Install required dependency (if not already installed)
pip3 install pyyaml
```

**Usage:**
```bash
# Run from DDD project root directory (auto-detects .agent3d-config.yaml)
cd /path/to/ddd/project
python3 ~/.agent3d/tools/drift_scanner.py --mode all
```

### MCP Server Usage

For MCP client integration, use the MCP server wrapper:

**Server Command:**
```bash
~/.agent3d/tools/drift_scanner_mcp_server.sh
```

**IMPORTANT:** The MCP server communicates via JSON-RPC over stdin/stdout. Do NOT call it with command-line arguments. MCP clients should launch it as a subprocess and communicate via the MCP protocol.

**DDD Root Detection Priority:**
1. **Explicit `ddd_root` parameter** - If provided in tool arguments
2. **`DDD_ROOT` environment variable** - Set in MCP server configuration
3. **Auto-detection** - Searches for `.agent3d-config.yaml` starting from working directory

**MCP Tool Schema:**
```json
{
  "name": "drift_scanner",
  "description": "Agent3D Drift Scanner - Multi-mode drift detection",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ddd_root": {"type": "string", "description": "DDD project root path"},
      "mode": {"enum": ["tc-mapping", "code-coverage", "feature-impl", "all"]},
      "test_cases_file": {"type": "string", "description": "Custom TEST-CASES.md path"},
      "output": {"type": "string", "description": "Custom output file path"},
      "quiet": {"type": "boolean", "description": "Suppress detailed output"}
    }
  }
}
```

**MCP Server Features:**
- **Hybrid Architecture** - Shell wrapper for environment setup + Python for MCP protocol
- **Virtual Environment** - Automatically activates venv if available
- **Dependency Management** - Ensures PyYAML is installed
- **Clean JSON-RPC Protocol** - Pure Python implementation with proper stdout/stderr separation
- **Error Handling** - Comprehensive error handling with proper MCP error responses
- **DDD_ROOT Support** - Uses environment variable for flexible project targeting
- **Robust Logging** - All logging to stderr, clean JSON-RPC responses to stdout

### MCP Configuration for Augment Code

Add this to your MCP configuration JSON:

```json
{
  "mcpServers": {
    "agent3d-drift-scanner": {
      "command": "/Users/nwaikhom/.agent3d/tools/drift_scanner_mcp_server.sh",
      "args": [],
      "env": {
        "DDD_ROOT": "/Users/nwaikhom/git/ProtobufRegistry/tools/protoc-gen-httpx-fastapi",
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

**Configuration Options:**
- **Set `DDD_ROOT`** - Points to your DDD project root directory
- **No arguments needed** - MCP server handles all communication via JSON-RPC
- **PATH environment** - Ensures Python and shell commands are available

**Usage in Augment Code:**
```
Please run a drift analysis using the agent3d drift scanner with mode "all"
```

### Temporary Directory Structure

The drift scanner automatically creates and uses a temporary directory structure:

```
.agent3d-tmp/
├── drift-reports/          # Generated YAML reports (consistent naming)
│   ├── tc-mapping-drift-report.yaml
│   ├── code-coverage-drift-report.yaml
│   ├── feature-impl-drift-report.yaml
│   └── all-drift-report.yaml
├── analysis-cache/         # Cached analysis data (future use)
└── logs/                   # Analysis session logs (timestamped)
    ├── drift-analysis-20240528_162310.log
    └── drift-analysis-20240528_162345.log
```

**Benefits:**
- **Clean workspace** - No temporary files cluttering the project root
- **Consistent naming** - Predictable file names for easy integration and scripting
- **Organized structure** - Separate directories for different types of outputs
- **Git-ignored** - Temporary directory is automatically excluded from version control
- **Easy reference** - Known file paths for CI/CD and automation scripts

### Automation-Friendly File Paths

The consistent naming scheme enables easy automation and scripting:

```bash
# Known file paths for each analysis mode
TC_MAPPING_REPORT=".agent3d-tmp/drift-reports/tc-mapping-drift-report.yaml"
CODE_COVERAGE_REPORT=".agent3d-tmp/drift-reports/code-coverage-drift-report.yaml"
FEATURE_IMPL_REPORT=".agent3d-tmp/drift-reports/feature-impl-drift-report.yaml"
COMPREHENSIVE_REPORT=".agent3d-tmp/drift-reports/all-drift-report.yaml"

# CI/CD integration example
python3 ~/.agent3d/tools/drift_scanner.py --mode all --quiet
echo "📊 Drift analysis complete - reports in .agent3d-tmp/drift-reports/"
```

### Integration with DDD Passes

#### Testing Pass Integration

Add to Testing Pass workflow:

```bash
# Step 1: Run TC ID drift analysis
echo "🔍 Analyzing TC ID drift..."
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping

# Step 2: Check drift level and review report
echo "📄 Drift report generated in .agent3d-tmp/drift-reports/"
```

#### Synchronization Pass Integration

Add to Synchronization Pass workflow:

```bash
# Validate TC ID mappings during synchronization
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping --quiet
```

#### Reverse Pass Integration

Add to Reverse Pass workflow:

```bash
# Check for undocumented test implementations
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping
```

## Output Format

### YAML Report Structure

```yaml
metadata:
  total_test_cases: 68
  total_test_functions: 45
  test_cases_with_implementations: 42
  test_functions_with_tc_ids: 38
  unique_tc_ids_in_code: 35
  orphaned_tc_ids_count: 3
  languages_detected: ["python", "javascript"]

summary:
  total_test_cases: 68
  total_test_functions: 45
  test_cases_without_implementations: 26
  implementations_without_test_cases: 7
  orphaned_tc_ids: 3
  drift_percentage: 15.2

test_cases_without_implementations:
  - tc_id: "TC-0103"
    title: "Implementation Pass follows documentation"
    status: "pending"
    execution_type: "Manual"
    priority: "High"

implementations_without_test_cases:
  - file: "test/test_scanner.py"
    function: "test_language_detection"
    full_name: "TestScanner::test_language_detection"
    type: "class_method"
    line_number: 45

orphaned_tc_ids_in_code: ["TC-9999", "TC-OLD-001"]

tc_mappings:
  "TC-0001":
    - file: "test/test_guidelines.py"
      function: "test_guideline_fetch"
      full_name: "TestGuidelines::test_guideline_fetch"
      type: "class_method"
      line_number: 23
```

### Console Output

```
🎯 TC ID DRIFT ANALYSIS SUMMARY
================================================================================

📊 OVERVIEW:
  Test Cases in TEST-CASES.md: 68
  Test Functions in Code: 45
  Languages Detected: python, javascript
  Unique TC IDs in Code: 35

🎯 DRIFT METRICS:
  Total Drift Items: 33
  Drift Percentage: 15.2%
  Status: ⚠️  MODERATE - Some drift detected

❌ TEST CASES WITHOUT IMPLEMENTATIONS (26):
------------------------------------------------------------
  ⏸️ TC-0103 - Implementation Pass follows documentation...
      Type: Manual, Priority: High

❌ IMPLEMENTATIONS WITHOUT TC IDs (7):
------------------------------------------------------------
  📁 test/test_scanner.py (3 functions):
    - TestScanner::test_language_detection:45
    - test_standalone_function:67

✅ SUCCESSFUL MAPPINGS (35):
  35 TC IDs have proper documentation-to-implementation mapping
```

## Exit Codes

- **0** - Low drift (<10%) - Excellent TC ID mapping
- **1** - Moderate drift (10-25%) - Some cleanup recommended
- **2** - High drift (>25%) - Significant issues requiring attention

## TC ID Pattern Recognition

The scanner recognizes TC IDs in the following formats:

- `TC-0001` - Basic format
- `TC-ENV-007` - Category prefix format
- `TC-0001a` - Sub-test case format
- `TC-ABC-123b` - Complex category format

### Language-Specific Detection

The scanner detects TC IDs in comments, docstrings, and function names across multiple languages:

- **Python**: Function names, docstrings, and `# TC-ID` comments
- **JavaScript/TypeScript**: `// TC-ID` comments and test descriptions
- **Java**: `@DisplayName` annotations and `// TC-ID` comments
- **Go/Rust**: Function comments and inline comments

## Best Practices

### For Developers

1. **Always include TC IDs** in test function names or nearby comments
2. **Use consistent naming** - prefer `test_feature_tc_0001` format
3. **Document in docstrings** for complex test cases
4. **One TC ID per test function** for clear 1:1 mapping

### For DDD Pass Integration

1. **Run during Testing Pass** to validate test coverage
2. **Include in Synchronization Pass** to catch drift early
3. **Use in Reverse Pass** to find undocumented implementations
4. **Set drift thresholds** appropriate for your project (recommend <10%)

### For CI/CD Integration

```yaml
# GitHub Actions example
- name: Check TC ID Drift
  run: |
    python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping --quiet
    if [ $? -eq 2 ]; then
      echo "❌ High TC ID drift detected"
      exit 1
    fi
```

## Troubleshooting

**No test files found:** Check file naming patterns and verify test directories exist.

**TC IDs not detected:** Ensure TC IDs follow the pattern `TC-[A-Z0-9]+-\d+[a-z]?` and are within 1000 characters of test functions.

**High drift percentage:** Review completed test cases without implementations and add TC ID references to existing tests.

## Integration Examples

See [DDD Pass Integration Guide](COMMON-PROCEDURES.md#drift-scanning) for complete integration examples with all DDD passes.
