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
**Golden Tests:** Use `pytest-goldie` for complex output/regression testing, `pytest --goldie-update` to update
**TC ID Mapping:** **CRITICAL** - Each test function MUST include TC-NNNN in name or docstring for 1:1 traceability
**Test Quality:** **CRITICAL** - Every test MUST import project code and call project functions, never test only mock data
**Real Testing:** **CRITICAL** - Tests must validate actual project behavior, not just assert against hardcoded values

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

**CRITICAL:** pytest usage and proper patterns.

- pytest over unittest
- pytest-goldie for complex output validation
- Fixtures for test setup
- **TC ID Mapping:** Each test function MUST include TC-NNNN in name or docstring
- **Test Quality:** Every test MUST import project code and call project functions
- **Real Testing:** Tests must validate actual behavior, not just hardcoded assertions

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

**Critical:** Missing type hints, string-based data access, catch-all exceptions, manual dependency editing, security issues, tests without project imports
**High:** Inefficient data structures, missing tests, poor error messages, memory issues, import problems, tests without function calls
**Medium:** Missing docstrings, long functions, naming inconsistencies, tests with only mock data
**Low:** Style improvements, performance micro-optimizations, weak test assertions

### Anti-Patterns to Reject

- Mutable default arguments, eval()/exec(), bare except clauses
- String concatenation in loops, not using context managers
- Using 'is' for value comparison, inappropriate comprehensions

### Quality Gates

**Python-Specific:**

- [ ] All public functions have type hints
- [ ] pytest used for all tests
- [ ] pyproject.toml used for configuration
- [ ] Appropriate data structures chosen
- [ ] Proper import organization
- [ ] All tests import project code
- [ ] All tests call project functions
- [ ] Tests validate actual behavior, not just hardcoded values

**Universal (see [Common Procedures](../docs/COMMON-PROCEDURES.md#quality-standards)):**

- [ ] Specific exception handling throughout
- [ ] Memory-efficient patterns
- [ ] No security anti-patterns
- [ ] Comprehensive test coverage
