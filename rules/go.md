# Go Development Rules

## Environment Setup

**Go Version:**

- Use latest stable version of Go
- Document required Go version in go.mod
- Use Go modules for dependency management
- Initialize modules with `go mod init github.com/organization/project`

**Project Structure:**

- Follow standard Go project layout
- Use cmd/ directory for main applications
- Use pkg/ directory for library code
- Use internal/ directory for private application and library code

## Code Style

**Formatting:**

- Use `gofmt` or `go fmt` to format code
- Run `go vet` and `golint` regularly
- Follow style recommendations in Effective Go
- Use `golangci-lint` for comprehensive linting

**Naming Conventions:**

- Use MixedCaps (camelCase or PascalCase) for multi-word names
- Use PascalCase for exported names (public)
- Use camelCase for unexported names (private)
- Use short, concise variable names in small scopes
- Use descriptive names for package-level declarations

**Package Organization:**

- Keep packages focused on single responsibility
- Avoid package names like "util" or "common"
- Organize code by domain, not by layer
- Avoid circular dependencies between packages

## Best Practices

1. **Error Handling**
   - Always check error returns
   - Return errors rather than using panic
   - Use custom error types for specific error conditions
   - Wrap errors with context using `fmt.Errorf("... %w", err)` or errors.Wrap

2. **Concurrency**
   - Use goroutines for concurrent operations
   - Use channels for communication between goroutines
   - Be careful with shared memory; use mutexes when necessary
   - Consider using sync.WaitGroup for waiting on multiple goroutines

3. **Resource Management**
   - Use defer for cleanup operations
   - Close resources in the reverse order of acquisition
   - Check for nil before closing resources
   - Use context for cancellation and timeouts

4. **Interface Design**
   - Keep interfaces small and focused
   - Define interfaces where they're used, not where they're implemented
   - Use embedding to compose interfaces
   - Accept interfaces, return concrete types

## Documentation

1. **Comments**
   - Write package comments for all packages
   - Document all exported functions, types, and constants
   - Follow the godoc conventions
   - Include examples in documentation when helpful

2. **README and Documentation**
   - Include clear installation and setup instructions
   - Document available commands and flags
   - Provide examples of common use cases
   - Document environment variables and configuration options

## Testing

1. **Test Organization**
   - Place tests in the same package as the code they test
   - Name test files with _test.go suffix
   - Use table-driven tests for testing multiple cases
   - Use subtests for organizing related test cases

2. **Test Coverage**
   - Aim for high test coverage, especially for critical code
   - Use `go test -cover` to measure coverage
   - Write both unit and integration tests
   - Use testify or other assertion libraries when helpful

## Performance

1. **Optimization**
   - Profile before optimizing
   - Use benchmarks to measure performance
   - Consider memory allocations and garbage collection
   - Use sync.Pool for frequently allocated objects

2. **Efficiency**
   - Prefer slices over arrays when length might change
   - Pre-allocate slices when the size is known
   - Use strings.Builder for string concatenation
   - Be mindful of copying large structs

## Security

1. **Input Validation**
   - Validate all user inputs
   - Use prepared statements for SQL queries
   - Sanitize data before displaying it to users
   - Be cautious with reflection and unsafe operations

2. **Sensitive Data**
   - Don't log sensitive information
   - Don't include sensitive data in error messages
   - Use secure random number generation for security-sensitive operations
   - Clear sensitive data from memory when no longer needed

## Deployment

1. **Containerization**
   - Use multi-stage Docker builds for smaller images
   - Build for the correct architecture and OS
   - Use scratch or distroless base images when possible
   - Don't run containers as root

2. **Configuration**
   - Use environment variables for configuration
   - Consider using a configuration library like Viper
   - Provide sensible defaults for all configuration options
   - Document all configuration parameters

## Dependency Management

1. **Versioning**
   - Use semantic versioning for your modules
   - Pin dependencies to specific versions in go.mod
   - Regularly update dependencies for security fixes
   - Use go.sum to ensure reproducible builds

2. **Vendoring**
   - Consider vendoring dependencies for production builds
   - Use `go mod vendor` to create the vendor directory
   - Include vendor directory in version control for deployment stability
   - Document vendoring strategy in the project README

## Code Review Standards

**Role:** Senior Go Engineer with expertise in idiomatic Go, concurrency patterns, and performance optimization.

### Critical Review Areas

#### 1. Error Handling

**CRITICAL:** Enforce explicit error checking and proper error wrapping.

- Never ignore errors; always check and handle them explicitly
- Use error wrapping with fmt.Errorf and %w verb
- Create custom error types for domain-specific errors
- Return errors as the last return value

#### 2. Concurrency and Goroutines

**CRITICAL:** Review goroutine usage, channel patterns, and race conditions.

- Use sync.Mutex or sync.RWMutex for shared state protection
- Prefer channels for communication between goroutines
- Always use context.Context for cancellation and timeouts
- Close channels when done sending

#### 3. Interface Design

**CRITICAL:** Ensure small, focused interfaces and proper composition.

- Keep interfaces small and focused on single responsibilities
- Use interface composition instead of large interfaces
- Accept interfaces, return concrete types
- Define interfaces at the point of use

#### 4. Performance and Memory Efficiency

**CRITICAL:** Check for unnecessary allocations and efficient data structures.

- Use strings.Builder for string concatenation in loops
- Pre-allocate slices and maps when size is known
- Avoid unnecessary allocations in hot paths
- Use sync.Pool for frequently allocated objects

#### 5. Idiomatic Go Patterns

**CRITICAL:** Enforce Go idioms and conventions.

- Use receiver methods instead of functions with struct parameters
- Design structs with useful zero values
- Use functional options for complex constructors
- Follow Go naming conventions (camelCase, not snake_case)

#### 6. Package Design and Organization

**CRITICAL:** Enforce proper package structure and naming.

- Use descriptive package names, avoid generic names like 'utils'
- Keep packages focused on single domain
- Document packages with clear purpose statements
- Avoid circular dependencies between packages

#### 7. Testing Patterns

**CRITICAL:** Enforce comprehensive testing strategies.

- Use table-driven tests for multiple test cases
- Test both success and error cases
- Use descriptive test names
- Use testify/assert for cleaner assertions

### Severity Classification

**Critical:** Ignored errors or improper error handling, race conditions or unsafe concurrent access, memory leaks or resource leaks, security vulnerabilities, panic-inducing code without recovery
**High:** Non-idiomatic Go patterns, performance inefficiencies, poor interface design, missing context usage, inadequate test coverage
**Medium:** Missing package documentation, inconsistent naming conventions, suboptimal data structure usage, missing error wrapping
**Low:** Code style improvements, additional test cases, performance micro-optimizations, documentation enhancements

### Anti-Patterns to Reject

- Ignoring errors with _, using panic for normal error conditions
- Not using context.Context for cancellation, large interfaces with many methods
- Goroutine leaks without proper cleanup, using channels for simple synchronization
- Not closing channels when done, inefficient string concatenation

### Quality Gates

**Go-Specific:**

- [ ] All errors are explicitly handled
- [ ] Proper concurrency patterns used
- [ ] Interfaces are small and focused
- [ ] Idiomatic Go conventions followed
- [ ] No race conditions or goroutine leaks
- [ ] Context used for cancellation

**Universal (see [Common Procedures](../docs/COMMON-PROCEDURES.md#quality-standards)):**

- [ ] Memory efficient patterns implemented
- [ ] Packages are well-organized and documented
- [ ] Comprehensive test coverage
- [ ] Performance considerations addressed
