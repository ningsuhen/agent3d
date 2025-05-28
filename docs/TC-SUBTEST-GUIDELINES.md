# Test Case and Sub-Test Guidelines

## 🧪 Test Case Hierarchy and Mapping

### Test Case Structure
- **TC-####** = **Test Cases** (mapped to individual test functions)
- **TC-####-{a,b,c...}** = **Sub-Tests** (mapped to parameters within parameterized tests)

### Implementation Guidelines

#### 1. Test Function Mapping
- Each `TC-####` maps to exactly one test function
- Test function docstring must include the TC-#### identifier
- Function name should be descriptive of the test case purpose

#### 2. Sub-Test Implementation
- Sub-tests `TC-####-{a,b,c...}` are implemented as parameters in `@pytest.mark.parametrize`
- Each parameter set represents one sub-test with specific test data
- Sub-test identifiers follow alphabetical sequence: a, b, c, d, etc.

#### 3. TC Identifier Placement Rules
**✅ ALLOWED Locations:**
- Test function docstrings (for TC-#### main test cases)
- Parameter values in `@pytest.mark.parametrize` (for TC-####-{a,b,c...} sub-tests)
- Comments directly above parameterize decorators (for grouping context)

**❌ FORBIDDEN Locations:**
- Comments outside test functions
- Data structures or constants
- Helper functions or utilities
- Variable names or configuration
- Module-level comments
- Class-level comments

#### 4. Example Implementation

```python
@pytest.mark.parametrize("tc_id,test_aspect,test_data", [
    # TC-CLIENT-001: Client ID Enum Generation
    ("TC-CLIENT-001-a", "enum_values_present", ["VALUE1", "VALUE2"]),
    ("TC-CLIENT-001-b", "enum_utility_methods", {"method": "all", "count": 5}),
    ("TC-CLIENT-001-c", "from_name_functionality", {"input": "VALUE1", "expected": "VALUE1"}),
])
def test_client_id_enum_generation(tc_id, test_aspect, test_data):
    """TC-CLIENT-001: Client ID enum generation with proper granularity."""
    if test_aspect == "enum_values_present":
        # Test enum values exist
        pass
    elif test_aspect == "enum_utility_methods":
        # Test utility methods
        pass
    elif test_aspect == "from_name_functionality":
        # Test from_name method
        pass
```

### Benefits of This Structure

#### 1. Granular Failure Reporting
- **Before**: `test_client_functionality failed` (which part?)
- **After**: `test_client_id_enum_generation[TC-CLIENT-001-a-enum_values_present] failed`

#### 2. Selective Test Execution
```bash
# Run all TC-CLIENT-001 tests
pytest -k "TC-CLIENT-001"

# Run specific sub-test
pytest -k "TC-CLIENT-001-a"

# Run specific test aspect
pytest -k "enum_values_present"
```

#### 3. Perfect Traceability
- Each test failure maps to exactly one TC or Sub-Test
- Clear relationship between documentation and implementation
- Easy to identify which requirement failed

#### 4. Maintainable Test Organization
- Related tests grouped logically
- Easy to add new sub-tests without changing test logic
- Shared setup code with focused test logic
