# Python Code Review Guidelines

**Role:** Senior Python Engineer with expertise in Pythonic code, performance optimization, and maintainability.

## Critical Review Areas

### 1. Type Safety and Annotations
**CRITICAL:** Demand proper type hints for all function parameters and return values.

**Key Points:**
- Missing type hints reduces maintainability and IDE support
- Require type annotations for all parameters and return values
- Use Optional[Type] for nullable returns
- Enforce typing imports for complex types

### 2. Data Structure Design
**CRITICAL:** Reject string-based data access; require structured types.

**Key Points:**
- Replace dictionaries with dataclasses for type safety
- String-based data access violates Python best practices
- Use Enum for constants instead of string literals
- Prefer NamedTuple or dataclass for structured data

### 3. Testing Framework Compliance
**CRITICAL:** Enforce pytest usage and appropriate testing patterns.

**Key Points:**
- Use pytest instead of unittest for consistency
- Consider pytest-goldie for complex output validation
- Add fixtures for test setup instead of setUp methods
- Implement proper test organization and naming

### 4. Configuration Management
**CRITICAL:** Require pyproject.toml for modern Python projects.

**Key Points:**
- Use pyproject.toml instead of requirements.txt for modern projects
- Configure tools in pyproject.toml for centralized management
- Separate development dependencies from production dependencies
- Never manually edit dependency files; use package managers

### 5. Error Handling Patterns
**CRITICAL:** Demand specific exception types and proper error handling.

**Key Points:**
- Use specific exception types instead of catching Exception
- Include meaningful error messages with context
- Use exception chaining with 'raise ... from e'
- Never silently ignore exceptions

### 6. Performance and Memory Efficiency
**CRITICAL:** Review data structure choices and memory usage.

**Key Points:**
- Use generators for large datasets to minimize memory usage
- Choose appropriate data structures from collections module
- Profile memory usage for data-intensive operations
- Avoid creating unnecessary temporary objects

### 7. Import Organization and Dependencies
**CRITICAL:** Enforce proper import structure and dependency management.

**Key Points:**
- Organize imports: standard library → third-party → local
- Use absolute imports over relative imports
- Avoid wildcard imports (from module import *)
- Group related imports together

## Severity Classification

### Critical Issues (Must Fix)
- Missing type hints on public APIs
- String-based data access instead of structured types
- Catch-all exception handling
- Manual dependency file editing
- Security vulnerabilities

### High Priority Issues (Should Fix)
- Inefficient data structure choices
- Missing test coverage
- Poor error messages
- Memory inefficient patterns
- Import organization issues

### Medium Priority Issues (Consider Fixing)
- Missing docstrings on public methods
- Long functions that could be refactored
- Inconsistent naming conventions
- Missing logging in error paths

### Low Priority Issues (Nice to Have)
- Code style improvements
- Additional type hints on private methods
- Performance micro-optimizations
- Documentation enhancements

## Anti-Patterns to Reject
- Mutable default arguments
- Using eval() or exec()
- Bare except: clauses
- String concatenation in loops
- Not using context managers for resources
- Ignoring PEP 8 style guidelines
- Using is for value comparison
- Not using list/dict comprehensions appropriately

## Quality Gates
- [ ] All public functions have type hints
- [ ] No string-based data access patterns
- [ ] pytest used for all tests
- [ ] pyproject.toml used for configuration
- [ ] Specific exception handling throughout
- [ ] Appropriate data structures chosen
- [ ] Memory-efficient patterns for large data
- [ ] Proper import organization
- [ ] No security anti-patterns
- [ ] Comprehensive test coverage
