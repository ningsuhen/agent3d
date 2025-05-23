# Python Development Rules

## Environment Setup

1. **Virtual Environment**
   - Always source the virtualenv at the project root
   - Use `python -m venv venv` to create a virtual environment named `venv` in the project root
   - Activate the environment before any development work:
     - Unix/MacOS: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`
   - Include `venv/` in `.gitignore`

2. **Dependencies**
   - Always use `requirements.txt` or `pyproject.toml` for dependency management
   - Pin dependency versions to avoid unexpected updates
   - Separate development dependencies from production dependencies
   - Run `pip freeze > requirements.txt` only after testing that the environment works correctly

## Code Style

1. **Formatting**
   - Follow PEP 8 style guide
   - Use a line length of 88 characters (Black default)
   - Use 4 spaces for indentation, never tabs
   - Use tools like Black and isort to automate formatting

2. **Naming Conventions**
   - Use `snake_case` for variables, functions, and methods
   - Use `PascalCase` for classes
   - Use `UPPER_CASE` for constants
   - Prefix private attributes with a single underscore (`_private_var`)
   - Prefix "dunder" methods with double underscores (`__special__`)

3. **Imports**
   - Group imports in the following order:
     1. Standard library imports
     2. Related third-party imports
     3. Local application/library specific imports
   - Use absolute imports over relative imports
   - Avoid wildcard imports (`from module import *`)

## Documentation

1. **Docstrings**
   - Use docstrings for all public modules, functions, classes, and methods
   - Follow Google or NumPy docstring style consistently
   - Include type hints in function signatures (PEP 484)
   - Document parameters, return values, and exceptions

2. **Comments**
   - Write comments for complex logic that isn't immediately obvious
   - Keep comments up-to-date with code changes
   - Use TODO comments for temporary solutions or incomplete implementations

## Testing

1. **Test Framework**
   - Use pytest for writing and running tests
   - Organize tests to mirror the structure of the application code
   - Name test files with `test_` prefix
   - Name test functions with `test_` prefix

2. **Test Coverage**
   - Aim for at least 80% test coverage for production code
   - Write unit tests for all public functions and methods
   - Include integration tests for critical paths
   - Use fixtures to set up test environments

## Error Handling

1. **Exceptions**
   - Use specific exception types rather than catching all exceptions
   - Create custom exception classes for application-specific errors
   - Include meaningful error messages
   - Use context managers (`with` statements) for resource management

2. **Logging**
   - Use the built-in `logging` module instead of print statements
   - Configure appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Include contextual information in log messages
   - Avoid logging sensitive information

## Performance

1. **Efficiency**
   - Use appropriate data structures for the task
   - Prefer list comprehensions over map/filter when appropriate
   - Use generators for large data sets to minimize memory usage
   - Profile code to identify bottlenecks before optimizing

2. **Concurrency**
   - Use `asyncio` for I/O-bound tasks
   - Use `multiprocessing` for CPU-bound tasks
   - Be cautious with thread safety when using shared resources
   - Use appropriate synchronization primitives

## Security

1. **Input Validation**
   - Validate all user inputs
   - Use parameterized queries for database operations
   - Sanitize data before displaying it to users
   - Be cautious with eval(), exec(), and similar functions

2. **Dependency Security**
   - Regularly update dependencies to patch security vulnerabilities
   - Use tools like safety or Snyk to check for vulnerable dependencies
   - Review the security implications of new dependencies before adding them

## Deployment

1. **Containerization**
   - Use Docker for containerizing Python applications
   - Create minimal container images
   - Use multi-stage builds to reduce image size
   - Don't run containers as root

2. **Configuration**
   - Use environment variables for configuration
   - Never hardcode sensitive information (passwords, API keys)
   - Use a library like python-dotenv for local development
   - Provide clear documentation for all configuration options
