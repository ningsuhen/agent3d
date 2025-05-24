# Implementation Pass

**Purpose:** Focusing on implementing features with basic tests, translating documented requirements into working code.

## When to Use
- When feature documentation is complete and ready for implementation
- After a Foundation Pass or Documentation Pass has established clear requirements
- When starting the development phase of a feature
- When converting a proof of concept into production code

## Process
1. **Scan:**
   - Review feature documentation and requirements
   - Identify implementation priorities and dependencies
   - Understand the architectural context for the implementation
   - Review existing test cases in `TEST-CASES.md`

2. **Draft:**
   - Create implementation plan with component breakdown
   - Identify key test scenarios for basic validation
   - Determine integration points with existing code
   - Plan for basic error handling and edge cases

3. **Ask:**
   - Clarify any ambiguities in the requirements
   - Confirm technical approach and design decisions
   - Verify assumptions about dependencies and interfaces
   - Discuss any potential technical challenges

4. **Sync:**
   - Implement the feature according to documentation
   - Write basic tests to verify core functionality
   - Ensure code meets project standards and conventions
   - Update documentation with any implementation details

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Working implementation of the documented feature
- Basic test coverage for core functionality
- Passing tests for the happy path scenarios
- Code that follows project standards and conventions
- Updated documentation reflecting implementation details

## Example Commit Message
`DDD: Implementation Pass - Implemented user authentication feature with basic test coverage`

## Testing Focus
- Focus on "happy path" test cases
- Implement basic validation tests
- Cover core functionality and main use cases
- Establish foundation for more comprehensive testing
- Ensure all implemented code has at least basic test coverage

## Implementation Guidelines
- Follow language-specific rules from the rules directory
- Implement only what is documented in the requirements
- Keep code lean and avoid speculative abstractions
- Document any technical decisions made during implementation
- Ensure code is readable and maintainable
