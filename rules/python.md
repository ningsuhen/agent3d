# Python Development Rules

## Environment Setup

**Virtual Environment:**
- Create virtual environment: `python -m venv venv` at project root
- Activate before development:
  - Unix/MacOS: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- Add `venv/` to `.gitignore`

**Dependencies:**
- Use `requirements.txt` or `pyproject.toml` for dependency management
- Pin versions to prevent unexpected updates
- Separate development from production dependencies
- Test environment before running `pip freeze > requirements.txt`

## Code Style

**Formatting:**
- Follow PEP 8 style guide
- Use 88-character line length (Black default)
- Use 4 spaces for indentation (never tabs)
- Use Black and isort for automated formatting

**Naming Conventions:**
- `snake_case` for variables, functions, methods
- `PascalCase` for classes
- `UPPER_CASE` for constants
- `_private_var` for private attributes
- `__special__` for dunder methods

**Imports:**
- Group in order: standard library → third-party → local
- Use absolute imports over relative imports
- Avoid wildcard imports (`from module import *`)

## Documentation

**Docstrings:**
- Use for all public modules, functions, classes, and methods
- Follow Google or NumPy style consistently
- Include type hints in function signatures (PEP 484)
- Document parameters, return values, and exceptions

**Comments:**
- Explain complex logic that isn't immediately obvious
- Keep comments synchronized with code changes
- Use TODO comments for temporary solutions

## Testing

**Test Framework:**
- Use pytest for writing and running tests
- Mirror application code structure in test organization
- Name test files and functions with `test_` prefix

**Test Coverage:**
- Target minimum 80% coverage for production code
- Write unit tests for all public functions and methods
- Include integration tests for critical paths
- Use fixtures for test environment setup

## Error Handling

**Exceptions:**
- Use specific exception types instead of catching all exceptions
- Create custom exception classes for application-specific errors
- Include meaningful error messages
- Use context managers (`with` statements) for resource management

**Logging:**
- Use built-in `logging` module instead of print statements
- Configure appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include contextual information in log messages
- Never log sensitive information

## Performance

**Efficiency:**
- Use appropriate data structures for each task
- Prefer list comprehensions over map/filter when readable
- Use generators for large datasets to minimize memory usage
- Profile code to identify bottlenecks before optimizing

**Concurrency:**
- Use `asyncio` for I/O-bound tasks
- Use `multiprocessing` for CPU-bound tasks
- Ensure thread safety with shared resources
- Use appropriate synchronization primitives

## Security

**Input Validation:**
- Validate all user inputs
- Use parameterized queries for database operations
- Sanitize data before displaying to users
- Avoid eval(), exec(), and similar functions

**Dependency Security:**
- Regularly update dependencies for security patches
- Use tools like safety or Snyk to check for vulnerabilities
- Review security implications before adding new dependencies

## Deployment

**Containerization:**
- Use Docker for containerizing Python applications
- Create minimal container images with multi-stage builds
- Never run containers as root user

**Configuration:**
- Use environment variables for configuration
- Never hardcode sensitive information (passwords, API keys)
- Use python-dotenv for local development
- Document all configuration options clearly
