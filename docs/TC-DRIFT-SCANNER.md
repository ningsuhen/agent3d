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

### Basic Usage

```bash
# TC ID mapping analysis (default)
python3 tools/drift_scanner.py --mode tc-mapping

# Code coverage analysis
python3 tools/drift_scanner.py --mode code-coverage

# Feature implementation analysis
python3 tools/drift_scanner.py --mode feature-impl

# Comprehensive analysis (all modes)
python3 tools/drift_scanner.py --mode all

# Scan specific directory
python3 tools/drift_scanner.py --root-dir /path/to/project

# Custom TEST-CASES.md location
python3 tools/drift_scanner.py --test-cases-file docs/custom-test-cases.md

# Custom output file
python3 tools/drift_scanner.py --output my-drift-report.yaml

# Quiet mode (minimal output)
python3 tools/drift_scanner.py --quiet
```

### Integration with DDD Passes

#### Testing Pass Integration

Add to Testing Pass workflow:

```bash
# Step 1: Run TC ID drift analysis
echo "🔍 Analyzing TC ID drift..."
python3 tools/tc-drift-scanner.py --output tc-drift-report.yaml

# Step 2: Check drift level
DRIFT_LEVEL=$?
if [ $DRIFT_LEVEL -eq 2 ]; then
    echo "❌ HIGH DRIFT: >25% - Must fix before proceeding"
    exit 1
elif [ $DRIFT_LEVEL -eq 1 ]; then
    echo "⚠️  MODERATE DRIFT: 10-25% - Cleanup recommended"
fi

# Step 3: Review drift report
echo "📄 Drift report generated: tc-drift-report.yaml"
```

#### Synchronization Pass Integration

Add to Synchronization Pass workflow:

```bash
# Validate TC ID mappings during synchronization
python3 tools/tc-drift-scanner.py --quiet
if [ $? -ne 0 ]; then
    echo "⚠️  TC ID drift detected - updating mappings"
    # Add remediation steps here
fi
```

#### Reverse Pass Integration

Add to Reverse Pass workflow:

```bash
# Check for undocumented test implementations
python3 tools/tc-drift-scanner.py --output reverse-drift-check.yaml
grep -q "implementations_without_test_cases: \[\]" reverse-drift-check.yaml
if [ $? -ne 0 ]; then
    echo "📝 Found undocumented test implementations"
    # Process and document missing test cases
fi
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

**Python:**
```python
def test_guideline_fetch_tc_0001():
    """Test TC-0001: Agent retrieves and caches guidelines."""
    pass

class TestGuidelines:
    def test_cache_validation(self):
        # TC-0001c: Cache validation and integrity check
        pass
```

**JavaScript:**
```javascript
// TC-0001: Agent retrieves and caches guidelines
it('should fetch guidelines from remote URL', () => {
    // Test implementation
});

describe('TC-0001a: Initial guideline fetch', () => {
    // Test suite
});
```

**Java:**
```java
@Test
@DisplayName("TC-0001: Agent retrieves and caches guidelines")
public void testGuidelineFetch() {
    // Test implementation
}

// TC-0001b: Local cache creation
@Test
public void testCacheCreation() {
    // Test implementation
}
```

**Go:**
```go
// TC-0001: Agent retrieves and caches guidelines
func TestGuidelineFetch(t *testing.T) {
    // Test implementation
}
```

**Rust:**
```rust
/// TC-0001: Agent retrieves and caches guidelines
#[test]
fn test_guideline_fetch() {
    // Test implementation
}
```

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
    python3 tools/tc-drift-scanner.py --quiet
    if [ $? -eq 2 ]; then
      echo "❌ High TC ID drift detected"
      exit 1
    fi
```

## Troubleshooting

### Common Issues

**No test files found:**
- Check file naming patterns match language conventions
- Verify test directories exist and contain test files
- Use `--root-dir` to specify correct project root

**TC IDs not detected:**
- Ensure TC IDs follow the pattern `TC-[A-Z0-9]+-\d+[a-z]?`
- Place TC IDs within 1000 characters of test function definition
- Use comments or docstrings if function names can't include TC IDs

**High drift percentage:**
- Review test cases marked as "completed" but without implementations
- Add TC ID references to existing test functions
- Remove or update obsolete test cases in TEST-CASES.md

## Integration Examples

See [DDD Pass Integration Guide](COMMON-PROCEDURES.md#tc-id-drift-scanning) for complete integration examples with all DDD passes.
