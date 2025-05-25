# JavaScript Code Review Guidelines

**Role:** Senior JavaScript/TypeScript Engineer with expertise in modern JavaScript patterns, async programming, and performance optimization.

## Critical Review Areas

### 1. Type Safety and TypeScript Usage
**CRITICAL:** Enforce TypeScript usage for type safety and maintainability.

**Key Points:**
- Use TypeScript for type safety and better IDE support
- Define interfaces for complex data structures
- Avoid any type; use specific types or generics
- Enforce strict TypeScript configuration

### 2. Async/Await and Promise Handling
**CRITICAL:** Demand proper error handling in async operations.

**Key Points:**
- Add proper error handling for all async operations
- Check response status before processing
- Use custom error types for better error handling
- Never ignore promise rejections

### 3. Modern JavaScript Patterns
**CRITICAL:** Enforce ES6+ patterns and avoid legacy JavaScript.

**Key Points:**
- Use const/let instead of var
- Use array methods (filter, map, reduce) instead of loops
- Use strict equality (===) instead of loose equality (==)
- Leverage destructuring and spread operator

### 4. Component Architecture (React/Vue)
**CRITICAL:** Enforce proper component patterns and lifecycle management.

**Key Points:**
- Use functional components with hooks instead of class components
- Implement proper loading and error states
- Use TypeScript interfaces for props
- Handle cleanup in useEffect when necessary

### 5. Performance Optimization
**CRITICAL:** Review for performance anti-patterns and memory leaks.

**Key Points:**
- Use useMemo for expensive calculations
- Use useCallback for event handlers passed to children
- Avoid creating new objects/functions in render
- Implement proper key props for list items

### 6. Module System and Imports
**CRITICAL:** Enforce proper ES6 module patterns.

**Key Points:**
- Use ES6 import/export syntax consistently
- Use barrel exports for cleaner import statements
- Import types separately when using TypeScript
- Organize imports logically

### 7. Error Handling and Logging
**CRITICAL:** Implement comprehensive error handling strategies.

**Key Points:**
- Use structured logging instead of console.log
- Implement proper error classification
- Include context in error messages
- Use error boundaries in React applications

## Severity Classification

### Critical Issues (Must Fix)
- Missing error handling in async operations
- Memory leaks or performance anti-patterns
- Security vulnerabilities (XSS, injection)
- Missing TypeScript types on public APIs
- Unhandled promise rejections

### High Priority Issues (Should Fix)
- Using legacy JavaScript patterns
- Missing component optimization
- Poor error messages
- Inconsistent module patterns
- Missing input validation

### Medium Priority Issues (Consider Fixing)
- Missing JSDoc comments
- Inconsistent naming conventions
- Suboptimal bundle size
- Missing accessibility attributes

### Low Priority Issues (Nice to Have)
- Code style improvements
- Additional TypeScript strictness
- Performance micro-optimizations
- Documentation enhancements

## Anti-Patterns to Reject
- Using var instead of const/let
- Mutating props or state directly
- Missing dependency arrays in useEffect
- Using any type in TypeScript
- Not handling async errors
- Creating functions inside render
- Using == instead of ===
- Not cleaning up event listeners/subscriptions

## Quality Gates
- [ ] TypeScript used with proper type definitions
- [ ] All async operations have error handling
- [ ] Modern JavaScript patterns used throughout
- [ ] Components optimized for performance
- [ ] Proper module import/export patterns
- [ ] Comprehensive error handling and logging
- [ ] No memory leaks or performance anti-patterns
- [ ] Security best practices followed
- [ ] Accessibility considerations implemented
- [ ] Comprehensive test coverage
