# Python Development Rules

## Environment & Dependencies

**Setup:** `python -m venv venv`, `source venv/bin/activate`, add `venv/` to `.gitignore`
**Dependencies:** Prefer `pyproject.toml` (PEP 518/621), pin versions, separate dev/prod dependencies, use package managers
**Config:** pyproject.toml with project metadata, dependencies, tool configurations (pytest, black, isort)

## Code Style

**Formatting:** PEP 8, 88-char lines, 4 spaces, Black + isort
**Naming:** snake_case (vars/functions), PascalCase (classes), UPPER_CASE (constants), _private, __special__
**Data:** Prefer dataclass/typed objects over dicts, Enum over string literals, NamedTuple for structured data
**Imports:** Standard → third-party → local, absolute imports, no wildcards

## Documentation & Testing

**Docstrings:** All public modules/functions/classes, Google/NumPy style, type hints (PEP 484), document params/returns/exceptions
**Type Hints:** Function args/returns, complex structures, `typing` module, `Optional[Type]` for nullable
**Comments:** Explain complex logic, keep synchronized, use TODO for temporary solutions

**Testing:** **Prefer pytest**, mirror app structure, `test_` prefix, 80% coverage minimum, fixtures for setup
**Golden Tests:** Use `pytest-goldie` for complex output/regression testing, `pytest --goldie-update` to update

## Error Handling, Performance & Security

**Exceptions:** Specific types, custom classes, meaningful messages, context managers (`with`)
**Logging:** Built-in `logging` module, appropriate levels, contextual info, no sensitive data
**Performance:** Appropriate data structures, list comprehensions, generators for large datasets, profile before optimizing
**Concurrency:** `asyncio` (I/O-bound), `multiprocessing` (CPU-bound), thread safety, synchronization primitives
**Security:** Validate inputs, parameterized queries, sanitize data, avoid eval()/exec(), update dependencies, use safety/Snyk
**Deployment:** Docker with minimal images, non-root user, environment variables, python-dotenv for dev
