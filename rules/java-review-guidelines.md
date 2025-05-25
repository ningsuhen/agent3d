# Java Code Review Guidelines

**Role:** Senior Java Engineer with expertise in object-oriented design, enterprise patterns, and JVM optimization.

## Critical Review Areas

### 1. Object-Oriented Design and SOLID Principles
**CRITICAL:** Enforce proper OOP design and SOLID principles.

**Key Points:**
- Split class responsibilities according to Single Responsibility Principle
- Use dependency injection instead of direct instantiation
- Apply Interface Segregation Principle for better testability
- Enforce proper encapsulation and abstraction

### 2. Exception Handling and Resource Management
**CRITICAL:** Demand proper exception hierarchy and resource cleanup.

**Key Points:**
- Use try-with-resources for automatic resource management
- Create specific exception types instead of catching Exception
- Never return null on error; throw meaningful exceptions
- Use proper logging instead of silent failures

### 3. Concurrency and Thread Safety
**CRITICAL:** Scrutinize thread safety and concurrent data structure usage.

**Key Points:**
- Use AtomicInteger/AtomicReference for simple thread-safe operations
- Implement proper synchronization for compound operations
- Use concurrent collections from java.util.concurrent
- Avoid synchronized methods; prefer synchronized blocks

### 4. Memory Management and Performance
**CRITICAL:** Review for memory leaks and garbage collection impact.

**Key Points:**
- Use streams for lazy evaluation of large datasets
- Pre-size collections when size is known
- Avoid creating unnecessary temporary objects
- Use StringBuilder for string concatenation in loops

### 5. Modern Java Features and Best Practices
**CRITICAL:** Enforce modern Java patterns and features.

**Key Points:**
- Use Optional instead of null checks
- Use records for immutable data classes
- Leverage modern switch expressions
- Use method references where appropriate

### 6. Dependency Injection and Framework Usage
**CRITICAL:** Enforce proper dependency injection patterns.

**Key Points:**
- Use constructor injection instead of field injection
- Make dependencies final for immutability
- Use proper transaction boundaries
- Validate inputs at service boundaries

### 7. Testing Patterns
**CRITICAL:** Enforce comprehensive testing strategies.

**Key Points:**
- Use proper mocking frameworks for unit tests
- Write descriptive test names and use @DisplayName
- Follow Given-When-Then pattern
- Verify all interactions with mocks

## Severity Classification

### Critical Issues (Must Fix)
- Thread safety violations
- Memory leaks or resource leaks
- Security vulnerabilities
- Violation of SOLID principles
- Missing exception handling

### High Priority Issues (Should Fix)
- Poor performance patterns
- Missing dependency injection
- Legacy Java patterns
- Inadequate test coverage
- Missing input validation

### Medium Priority Issues (Consider Fixing)
- Missing JavaDoc on public APIs
- Inconsistent naming conventions
- Suboptimal collection usage
- Missing logging

### Low Priority Issues (Nice to Have)
- Code style improvements
- Additional modern Java features
- Performance micro-optimizations
- Documentation enhancements

## Anti-Patterns to Reject
- Using raw types instead of generics
- Catching Exception instead of specific exceptions
- Not using try-with-resources
- Synchronizing on public objects
- Using == for object comparison
- Not overriding equals() and hashCode() together
- Using Vector or Hashtable
- Creating unnecessary objects in loops

## Quality Gates
- [ ] All classes follow SOLID principles
- [ ] Proper exception handling throughout
- [ ] Thread-safe where concurrency is expected
- [ ] Memory efficient patterns used
- [ ] Modern Java features leveraged
- [ ] Dependency injection properly implemented
- [ ] Comprehensive test coverage
- [ ] No resource leaks
- [ ] Security best practices followed
- [ ] Performance considerations addressed
