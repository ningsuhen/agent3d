# Python Development Rules

## Environment & Dependencies

**Setup:** `python -m venv venv`, `source venv/bin/activate`, add `venv/` to `.gitignore`
**Dependencies:** Prefer `pyproject.toml` (PEP 518/621), pin versions, separate dev/prod dependencies, use package managers
**Config:** pyproject.toml with project metadata, dependencies, tool configurations (pytest, black, isort)

## Code Style

**Formatting:** PEP 8, 88-char lines, 4 spaces, Black + isort
**Naming:** snake_case (vars/functions), PascalCase (classes), UPPER_CASE (constants), _private, **special**
**Data:** Prefer dataclass/typed objects over dicts, Enum over string literals, NamedTuple for structured data
**Imports:** Standard → third-party → local, absolute imports, no wildcards

## Documentation & Testing

**Docstrings:** All public modules/functions/classes, Google/NumPy style, type hints (PEP 484), document params/returns/exceptions
**Type Hints:** Function args/returns, complex structures, `typing` module, `Optional[Type]` for nullable
**Comments:** Explain complex logic, keep synchronized, use TODO for temporary solutions

**Testing:** **Prefer pytest**, mirror app structure, `test_` prefix, 80% coverage minimum, fixtures for setup
**CRITICAL PRINCIPLE:** **EVERY TEST MUST TEST PROJECT FUNCTIONALITY** - No test should exist without testing actual project code
**Test Implementation:** **CRITICAL** - Tests should implement the best end-to-end behavior of the project code that covers the test description
**Golden Tests:** Use `pytest-goldie` for complex output/regression testing, `pytest --goldie-update` to update
**TC ID Mapping:** **CRITICAL** - Each test function MUST include TC-NNNN in name or docstring for 1:1 traceability
**FT-TC Validation:** **CRITICAL** - When TC is linked to an FT, the test MUST actually use and validate that specific feature functionality
**Parameterization:** Use `@pytest.mark.parametrize` for testing multiple inputs/scenarios efficiently
**Sub-Test Cases:** **CRITICAL** - Sub-test cases are variations of a single test case (e.g., TC-HTTP-001-a, TC-HTTP-001-b) that test different inputs, conditions, or scenarios within the same logical test. When implementing sub-test cases, prefer `@pytest.mark.parametrize` with TC ID comments above each test case parameter:
```python
@pytest.mark.parametrize("http_method,test_data", [
    # TC-HTTP-001-a
    ("GET", {
        "method_name": "GetItem",
        "request_type": "GetItemRequest",
        "response_type": "GetItemResponse",
        "request_data": {"item_id": "test-item-123"},
        "expected_response": {"item": {"id": "test-item-123", "name": "Test Item"}}
    }),
    # TC-HTTP-001-b
    ("POST", {
        "method_name": "CreateItem",
        "request_type": "CreateItemRequest",
        "response_type": "CreateItemResponse",
        "request_data": {"name": "New Item", "description": "New Description"},
        "expected_response": {"item": {"id": "new-item-456", "name": "New Item"}}
    }),
])
@pytest.mark.asyncio
async def test_basic_http_operations(http_method, test_data):
    """TC-HTTP-001: Basic HTTP Operations - Verify GET, POST operations."""
```
**Test Quality:** **CRITICAL** - Every test MUST test actual project functionality by importing project code from git-tracked directories and calling project functions, never test only mock data or trivial assertions
**Project Code Imports:** **CRITICAL** - Tests must import from actual project source directories (parent/subdirectories checked into git), not just test libraries
**Import Failure Handling:** **CRITICAL** - Never use try-except on imports in tests. If imports fail, the test should fail immediately
**Import Organization:** **CRITICAL** - All imports in tests must be at the top of the file, following standard library → third-party → local order
**Real Testing:** **CRITICAL** - Tests must validate actual project behavior through end-to-end execution that matches the test description, not just assert against hardcoded values

## Error Handling, Performance & Security

**Exceptions:** Specific types, custom classes, meaningful messages, context managers (`with`)
**Logging:** Built-in `logging` module, appropriate levels, contextual info, no sensitive data
**Performance:** Appropriate data structures, list comprehensions, generators for large datasets, profile before optimizing
**Concurrency:** `asyncio` (I/O-bound), `multiprocessing` (CPU-bound), thread safety, synchronization primitives
**Security:** Validate inputs, parameterized queries, sanitize data, avoid eval()/exec(), update dependencies, use safety/Snyk
**Deployment:** Docker with minimal images, non-root user, environment variables, python-dotenv for dev

## Code Review Standards

**Role:** Senior Python Engineer with expertise in Pythonic code, performance optimization, and maintainability.

### Critical Review Areas

#### 1. Type Safety and Annotations

**CRITICAL:** Type hints for all function parameters and return values.

- Use Optional[Type] for nullable returns
- Import complex types from typing module

#### 2. Data Structure Design

**CRITICAL:** Structured types over string-based data access.

- Use dataclasses/NamedTuple instead of dictionaries
- Use Enum for constants instead of string literals

#### 3. Testing Framework Compliance

**CRITICAL:** pytest usage and proper patterns. **EVERY TEST MUST TEST PROJECT FUNCTIONALITY.**

- pytest over unittest
- pytest-goldie for complex output validation
- Fixtures for test setup
- **TC ID Mapping:** Each test function MUST include TC-NNNN in name or docstring
- **FT-TC Validation:** When TC is linked to an FT, the test MUST actually use and validate that specific feature functionality
- **Parameterization:** Use `@pytest.mark.parametrize` for testing multiple inputs/scenarios efficiently
- **Sub-Test Cases:** Sub-test cases are variations of a single test case (e.g., TC-HTTP-001-a, TC-HTTP-001-b) that test different inputs, conditions, or scenarios within the same logical test. When implementing sub-test cases, prefer `@pytest.mark.parametrize` with TC ID comments above each test case parameter
- **Test Quality:** Every test MUST test actual project functionality by importing project code from git-tracked directories and calling project functions
- **Project Code Imports:** Tests must import from actual project source directories (parent/subdirectories checked into git)
- **Import Failure Handling:** Never use try-except on imports in tests - let import failures cause test failures
- **Import Organization:** All imports in tests must be at the top of the file, following standard library → third-party → local order
- **Real Testing:** Tests must validate actual behavior through end-to-end execution that matches the test description, not just hardcoded assertions
- **Test Description Alignment:** Test implementation must cover the best end-to-end behavior described in the test case

#### 4. Configuration Management

**CRITICAL:** pyproject.toml for modern Python projects.

- pyproject.toml over requirements.txt
- Centralized tool configuration
- Use package managers, never manual editing

#### 5. Error Handling Patterns

**CRITICAL:** Specific exception types and proper error handling.

- Specific exceptions instead of catching Exception
- Meaningful error messages with context
- Exception chaining with 'raise ... from e'

#### 6. Performance and Memory Efficiency

**CRITICAL:** Efficient data structures and memory usage.

- Generators for large datasets
- Appropriate collections module data structures
- Avoid unnecessary temporary objects

#### 7. Import Organization

**CRITICAL:** Proper import structure.

- Order: standard library → third-party → local
- Absolute imports over relative
- No wildcard imports

### Severity Classification

**Critical:** Missing type hints, string-based data access, catch-all exceptions, manual dependency editing, security issues, tests that don't test project functionality, tests without project imports from git-tracked directories, try-except on imports in tests, tests linked to FT that don't validate the specific feature
**High:** Inefficient data structures, missing tests, poor error messages, memory issues, import problems, tests without function calls to project code, tests that don't implement end-to-end behavior matching the test description
**Medium:** Missing docstrings, long functions, naming inconsistencies, tests with only mock data, tests importing only test libraries
**Low:** Style improvements, performance micro-optimizations, weak test assertions

### Anti-Patterns to Reject

- Mutable default arguments, eval()/exec(), bare except clauses
- String concatenation in loops, not using context managers
- Using 'is' for value comparison, inappropriate comprehensions
- Try-except blocks around imports in tests (let import failures fail the test)
- Imports scattered throughout test files instead of at the top
- Tests that don't test any project functionality (only test mocks, constants, or trivial assertions)
- Tests that don't implement the end-to-end behavior described in the test case description
- Tests linked to an FT that don't actually use or validate the specific feature functionality

### Quality Gates

**Python-Specific:**

- [ ] All public functions have type hints
- [ ] pytest used for all tests
- [ ] pyproject.toml used for configuration
- [ ] Appropriate data structures chosen
- [ ] Proper import organization (all imports at top of file)
- [ ] Test imports follow standard library → third-party → local order
- [ ] Every test tests actual project functionality (no tests without project code execution)
- [ ] All tests import actual project code from git-tracked directories
- [ ] All tests call project functions from imported modules
- [ ] Tests validate actual behavior, not just hardcoded values
- [ ] No tests import only test libraries without project code
- [ ] No try-except blocks around imports in tests (let import failures fail tests)
- [ ] Tests linked to FT actually use and validate the specific feature functionality
- [ ] Parameterization used appropriately for multiple inputs/scenarios
- [ ] Sub-test cases implemented using @pytest.mark.parametrize with TC ID comments above each parameter

**Universal (see [Common Procedures](../docs/COMMON-PROCEDURES.md#quality-standards)):**

- [ ] Specific exception handling throughout
- [ ] Memory-efficient patterns
- [ ] No security anti-patterns
- [ ] Comprehensive test coverage
