# JavaScript Development Rules

## Environment Setup

1. **Node.js**
   - Use the LTS (Long Term Support) version of Node.js
   - Use nvm (Node Version Manager) to manage multiple Node.js versions
   - Document the required Node.js version in package.json

2. **Package Management**
   - Prefer npm or yarn, but be consistent within a project
   - Lock dependencies with package-lock.json (npm) or yarn.lock (yarn)
   - Use exact versions for critical dependencies (`"express": "4.17.1"` instead of `"express": "^4.17.1"`)
   - Regularly update dependencies to patch security vulnerabilities

## Code Style

1. **Formatting**
   - Use ESLint for linting and Prettier for formatting
   - Use 2 spaces for indentation
   - Limit lines to 80-100 characters
   - Use semicolons consistently (either always or never)
   - Use single quotes for strings unless escaping is needed

2. **Naming Conventions**
   - Use camelCase for variables, functions, and methods
   - Use PascalCase for classes and React components
   - Use UPPER_CASE for constants
   - Use descriptive names that reflect purpose

3. **Modern JavaScript**
   - Use ES6+ features when appropriate
   - Use arrow functions for anonymous functions
   - Use destructuring for objects and arrays
   - Use template literals instead of string concatenation
   - Use async/await instead of raw promises when possible

## Project Structure

1. **Organization**
   - Group files by feature or type, depending on project size
   - Keep related files close to each other
   - Use index.js files to expose public APIs
   - Separate business logic from UI components

2. **Modules**
   - Use ES modules (import/export) instead of CommonJS (require/module.exports)
   - Export one thing per file when possible
   - Avoid circular dependencies
   - Use absolute imports for project files when supported

## Documentation

1. **Code Comments**
   - Document complex logic and non-obvious solutions
   - Use JSDoc for public APIs and libraries
   - Include examples in documentation when helpful
   - Keep comments up-to-date with code changes

2. **README and Documentation**
   - Include clear installation and setup instructions
   - Document available scripts (build, test, lint, etc.)
   - Provide examples of common use cases
   - Document environment variables and configuration options

## Testing

1. **Test Framework**
   - Use Jest, Mocha, or another established testing framework
   - Write unit tests for utility functions and business logic
   - Write integration tests for API endpoints
   - Write end-to-end tests for critical user flows

2. **Test Organization**
   - Co-locate tests with the code they test when possible
   - Use descriptive test names that explain the expected behavior
   - Use setup and teardown functions to avoid repetition
   - Mock external dependencies to isolate tests

## Error Handling

1. **Async Code**
   - Always handle promise rejections
   - Use try/catch blocks with async/await
   - Provide meaningful error messages
   - Log errors with appropriate context

2. **Error Types**
   - Create custom error classes for application-specific errors
   - Include stack traces in development
   - Sanitize error messages in production
   - Return appropriate HTTP status codes in API responses

## Performance

1. **Optimization**
   - Optimize only after measuring performance
   - Use performance profiling tools (Chrome DevTools, Lighthouse)
   - Minimize DOM manipulations
   - Use debouncing and throttling for frequent events

2. **Loading**
   - Use code splitting to reduce initial bundle size
   - Lazy load components and routes when appropriate
   - Optimize and compress images and assets
   - Use appropriate caching strategies

## Security

1. **Input Validation**
   - Validate all user inputs
   - Sanitize data before rendering to prevent XSS
   - Use parameterized queries for database operations
   - Be cautious with eval(), Function(), and similar functions

2. **Authentication and Authorization**
   - Use established libraries for authentication
   - Store tokens securely (HttpOnly cookies)
   - Implement proper CSRF protection
   - Use HTTPS for all production traffic

## Frontend Specific (React/Vue/Angular)

1. **Component Design**
   - Keep components small and focused
   - Separate container and presentational components
   - Use composition over inheritance
   - Implement proper prop validation

2. **State Management**
   - Choose appropriate state management based on project complexity
   - Keep state normalized to avoid inconsistencies
   - Document state shape and mutations
   - Minimize state changes for better performance
