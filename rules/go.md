# Go Development Rules

## Environment Setup

1. **Go Version**
   - Use the latest stable version of Go
   - Document the required Go version in go.mod
   - Use Go modules for dependency management
   - Initialize modules with `go mod init github.com/organization/project`

2. **Project Structure**
   - Follow the standard Go project layout
   - Use cmd/ directory for main applications
   - Use pkg/ directory for library code
   - Use internal/ directory for private application and library code

## Code Style

1. **Formatting**
   - Use `gofmt` or `go fmt` to format code
   - Run `go vet` and `golint` regularly
   - Follow the style recommendations in Effective Go
   - Use `golangci-lint` for comprehensive linting

2. **Naming Conventions**
   - Use MixedCaps (camelCase or PascalCase) for multi-word names
   - Use PascalCase for exported names (public)
   - Use camelCase for unexported names (private)
   - Use short, concise variable names in small scopes
   - Use descriptive names for package-level declarations

3. **Package Organization**
   - Keep packages focused on a single responsibility
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
