# Python Development Rules

## Environment Setup

**Virtual Environment:**
- Create virtual environment: `python -m venv venv` at project root
- Activate before development:
  - Unix/MacOS: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- Add `venv/` to `.gitignore`

**Dependencies:**
- **Prefer `pyproject.toml`** for modern Python projects (PEP 518/621)
- Use `requirements.txt` only for legacy projects or simple scripts
- Pin versions to prevent unexpected updates
- Separate development from production dependencies
- Use package managers like `pip`, `poetry`, or `pipenv` instead of manually editing dependency files

**pyproject.toml Configuration:**
- Use `pyproject.toml` as the central configuration file for modern Python projects
- Include project metadata, dependencies, and tool configurations
- Example structure:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-project"
version = "0.1.0"
description = "Project description"
dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-goldie>=0.2.0",
    "black>=22.0.0",
    "isort>=5.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
```

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

**Data Structures:**
- Prefer using static types or references rather than strings
- Prefer using dataclass or typed objects rather than dict objects which need key access by strings
- Use Enum for constants instead of string literals
- Use NamedTuple or dataclass for structured data

**Examples:**
```python
# Prefer this:
@dataclass
class User:
    name: str
    email: str

# Over this:
user = {"name": "John", "email": "john@example.com"}

# Prefer this:
class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Over this:
status = "active"
```

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

**Type Hints:**
- Prefer adding type hints where ambiguous like function args and return types
- Use type hints for complex data structures and class attributes
- Import types from `typing` module when needed
- Use `Optional[Type]` for nullable parameters

**Comments:**
- Explain complex logic that isn't immediately obvious
- Keep comments synchronized with code changes
- Use TODO comments for temporary solutions

## Testing

**Test Framework:**
- **Prefer pytest** for all testing (unit tests, integration tests, etc.)
- Pytest is the recommended framework over unittest or other alternatives
- Mirror application code structure in test organization
- Name test files and functions with `test_` prefix

**Test Coverage:**
- Target minimum 80% coverage for production code
- Write unit tests for all public functions and methods
- Include integration tests for critical paths
- Use fixtures for test environment setup

**Golden Tests:**
- Use `pytest-goldie` for snapshot/golden file testing when appropriate
- Golden tests are ideal for:
  - Testing complex output formats (JSON, XML, HTML, etc.)
  - Regression testing for data transformations
  - Validating generated code or templates
  - Testing CLI output or API responses
- Install with: `pip install pytest-goldie`
- Example usage:
```python
def test_data_transformation(goldie):
    result = transform_data(input_data)
    goldie.assert_against(result, "expected_output.json")
```
- Update golden files when output legitimately changes: `pytest --goldie-update`

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
