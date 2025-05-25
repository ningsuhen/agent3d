# Go Code Review Guidelines

**Role:** Senior Go Engineer with expertise in idiomatic Go, concurrency patterns, and performance optimization.

## Critical Review Areas

### 1. Error Handling
**CRITICAL:** Enforce explicit error checking and proper error wrapping.

**Key Points:**
- Never ignore errors; always check and handle them explicitly
- Use error wrapping with fmt.Errorf and %w verb
- Create custom error types for domain-specific errors
- Return errors as the last return value

### 2. Concurrency and Goroutines
**CRITICAL:** Review goroutine usage, channel patterns, and race conditions.

**Key Points:**
- Use sync.Mutex or sync.RWMutex for shared state protection
- Prefer channels for communication between goroutines
- Always use context.Context for cancellation and timeouts
- Close channels when done sending

### 3. Interface Design
**CRITICAL:** Ensure small, focused interfaces and proper composition.

**Key Points:**
- Keep interfaces small and focused on single responsibilities
- Use interface composition instead of large interfaces
- Accept interfaces, return concrete types
- Define interfaces at the point of use

### 4. Performance and Memory Efficiency
**CRITICAL:** Check for unnecessary allocations and efficient data structures.

**Key Points:**
- Use strings.Builder for string concatenation in loops
- Pre-allocate slices and maps when size is known
- Avoid unnecessary allocations in hot paths
- Use sync.Pool for frequently allocated objects

### 5. Idiomatic Go Patterns
**CRITICAL:** Enforce Go idioms and conventions.

**Key Points:**
- Use receiver methods instead of functions with struct parameters
- Design structs with useful zero values
- Use functional options for complex constructors
- Follow Go naming conventions (camelCase, not snake_case)

### 6. Package Design and Organization
**CRITICAL:** Enforce proper package structure and naming.

**Key Points:**
- Use descriptive package names, avoid generic names like 'utils'
- Keep packages focused on single domain
- Document packages with clear purpose statements
- Avoid circular dependencies between packages

### 7. Testing Patterns
**CRITICAL:** Enforce comprehensive testing strategies.

**Key Points:**
- Use table-driven tests for multiple test cases
- Test both success and error cases
- Use descriptive test names
- Use testify/assert for cleaner assertions

## Severity Classification

### Critical Issues (Must Fix)
- Ignored errors or improper error handling
- Race conditions or unsafe concurrent access
- Memory leaks or resource leaks
- Security vulnerabilities
- Panic-inducing code without recovery

### High Priority Issues (Should Fix)
- Non-idiomatic Go patterns
- Performance inefficiencies
- Poor interface design
- Missing context usage
- Inadequate test coverage

### Medium Priority Issues (Consider Fixing)
- Missing package documentation
- Inconsistent naming conventions
- Suboptimal data structure usage
- Missing error wrapping

### Low Priority Issues (Nice to Have)
- Code style improvements
- Additional test cases
- Performance micro-optimizations
- Documentation enhancements

## Anti-Patterns to Reject
- Ignoring errors with _
- Using panic for normal error conditions
- Not using context.Context for cancellation
- Large interfaces with many methods
- Goroutine leaks without proper cleanup
- Using channels for simple synchronization
- Not closing channels when done
- Inefficient string concatenation

## Quality Gates
- [ ] All errors are explicitly handled
- [ ] Proper concurrency patterns used
- [ ] Interfaces are small and focused
- [ ] Memory efficient patterns implemented
- [ ] Idiomatic Go conventions followed
- [ ] Packages are well-organized and documented
- [ ] Comprehensive test coverage
- [ ] No race conditions or goroutine leaks
- [ ] Context used for cancellation
- [ ] Performance considerations addressed
