# Python Code Review Guidelines

**Role:** Senior Python Engineer with expertise in Pythonic code, performance optimization, and maintainability.

## Critical Review Areas

### 1. Type Safety and Annotations
**CRITICAL:** Type hints for all function parameters and return values.
- Use Optional[Type] for nullable returns
- Import complex types from typing module

### 2. Data Structure Design
**CRITICAL:** Structured types over string-based data access.
- Use dataclasses/NamedTuple instead of dictionaries
- Use Enum for constants instead of string literals

### 3. Testing Framework Compliance
**CRITICAL:** pytest usage and proper patterns.
- pytest over unittest
- pytest-goldie for complex output validation
- Fixtures for test setup

### 4. Configuration Management
**CRITICAL:** pyproject.toml for modern Python projects.
- pyproject.toml over requirements.txt
- Centralized tool configuration
- Use package managers, never manual editing

### 5. Error Handling Patterns
**CRITICAL:** Specific exception types and proper error handling.
- Specific exceptions instead of catching Exception
- Meaningful error messages with context
- Exception chaining with 'raise ... from e'

### 6. Performance and Memory Efficiency
**CRITICAL:** Efficient data structures and memory usage.
- Generators for large datasets
- Appropriate collections module data structures
- Avoid unnecessary temporary objects

### 7. Import Organization
**CRITICAL:** Proper import structure.
- Order: standard library → third-party → local
- Absolute imports over relative
- No wildcard imports

## Severity Classification

**Critical:** Missing type hints, string-based data access, catch-all exceptions, manual dependency editing, security issues
**High:** Inefficient data structures, missing tests, poor error messages, memory issues, import problems
**Medium:** Missing docstrings, long functions, naming inconsistencies
**Low:** Style improvements, performance micro-optimizations

## Anti-Patterns to Reject
- Mutable default arguments, eval()/exec(), bare except clauses
- String concatenation in loops, not using context managers
- Using 'is' for value comparison, inappropriate comprehensions

## Quality Gates
**Python-Specific:**
- [ ] All public functions have type hints
- [ ] pytest used for all tests
- [ ] pyproject.toml used for configuration
- [ ] Appropriate data structures chosen
- [ ] Proper import organization

**Universal (see [Common Procedures](../docs/COMMON-PROCEDURES.md#quality-standards)):**
- [ ] Specific exception handling throughout
- [ ] Memory-efficient patterns
- [ ] No security anti-patterns
- [ ] Comprehensive test coverage
