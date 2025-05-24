# Java Development Rules

## Environment Setup

**JDK Version:**
- Use LTS (Long Term Support) versions of Java when possible
- Document required Java version in build files
- Use consistent JDK version across development, CI/CD, and production

**Build Tools:**
- Use Gradle or Maven for build automation
- Include wrapper scripts (gradlew/mvnw) in the repository
- Define all dependencies in build file, not in IDE
- Use dependency locking to ensure reproducible builds

## Code Style

**Formatting:**
- Follow Google Java Style Guide or similar established style
- Use 4 spaces for indentation, not tabs
- Limit line length to 100-120 characters
- Use tools like Checkstyle, PMD, or SpotBugs for static analysis

**Naming Conventions:**
- `camelCase` for variables, methods, parameters
- `PascalCase` for classes and interfaces
- `UPPER_SNAKE_CASE` for constants
- Use descriptive names that reflect purpose
- Prefix interfaces with 'I' only when both interface and implementation exist

**Organization:**
- One top-level class per file
- Group related classes in packages
- Follow standard package naming conventions (com.company.project.module)
- Order class members logically (constants, fields, constructors, methods)

## Best Practices

**Object-Oriented Design:**
- Follow SOLID principles
- Prefer composition over inheritance
- Design for extension but restrict subclassing when appropriate
- Make fields private and provide getters/setters only when necessary

**Immutability:**
- Make classes immutable when possible
- Use final for fields that shouldn't change after initialization
- Use defensive copying for mutable parameters and return values
- Use immutable collections when appropriate

**Exception Handling:**
- Use checked exceptions for recoverable conditions
- Use unchecked exceptions for programming errors
- Include meaningful error messages
- Clean up resources in finally blocks or use try-with-resources

**Concurrency:**
- Prefer higher-level concurrency utilities over raw threads
- Use thread pools for managing worker threads
- Make classes thread-safe or clearly document thread safety guarantees
- Be cautious with synchronization to avoid deadlocks

## Documentation

1. **Javadoc**
   - Write Javadoc for all public classes and methods
   - Include @param, @return, and @throws tags
   - Document thread safety guarantees
   - Keep documentation up-to-date with code changes

2. **Comments**
   - Use comments to explain complex algorithms or non-obvious solutions
   - Avoid redundant comments that just repeat the code
   - Use TODO comments for temporary solutions or incomplete implementations
   - Document performance characteristics for critical operations

## Testing

1. **Test Framework**
   - Use JUnit 5 for unit testing
   - Use Mockito for mocking dependencies
   - Use AssertJ or similar for fluent assertions
   - Write both unit and integration tests

2. **Test Organization**
   - Mirror the package structure of the main code
   - Name test classes with "Test" suffix
   - Write focused tests that verify a single behavior
   - Use appropriate test fixtures and setup methods

## Performance

1. **Optimization**
   - Optimize only after measuring performance
   - Use profiling tools to identify bottlenecks
   - Consider memory usage and garbage collection
   - Document performance characteristics and requirements

2. **Collections**
   - Choose appropriate collection types for the use case
   - Specify initial capacity for collections when the size is known
   - Use streams for processing collections when appropriate
   - Be cautious with large collections and memory usage

## Security

1. **Input Validation**
   - Validate all user inputs
   - Use parameterized queries for database operations
   - Sanitize data before displaying it to users
   - Be cautious with reflection, deserialization, and dynamic code execution

2. **Sensitive Data**
   - Don't log sensitive information
   - Don't include sensitive data in exception messages
   - Properly handle secrets and credentials
   - Use secure random number generation for security-sensitive operations

## Deployment

1. **Containerization**
   - Use Docker for containerizing Java applications
   - Create minimal container images
   - Use multi-stage builds to reduce image size
   - Don't run containers as root

2. **Configuration**
   - Use environment variables or external configuration sources
   - Never hardcode sensitive information
   - Provide sensible defaults for all configuration options
   - Document all configuration parameters
