# Refactoring Pass

**Purpose:** Cleaning up and improving code structure without changing functionality, focusing on maintainability, readability, and performance.

## When to Use
- After features are fully implemented and tested
- When technical debt has accumulated
- Before adding new features to existing code
- When performance improvements are needed
- During regular maintenance cycles
- When preparing for a major release

## Process
1. **Scan:**
   - Identify code smells and technical debt
   - Review code for maintainability issues
   - Look for performance bottlenecks
   - Analyze code complexity and duplication
   - Review architectural alignment

2. **Draft:**
   - Plan refactoring approach and priorities
   - Document expected improvements
   - Identify potential risks and mitigation strategies
   - Plan verification approach to ensure functionality is preserved

3. **Ask:**
   - Confirm refactoring priorities
   - Discuss potential architectural improvements
   - Verify that proposed changes align with project direction
   - Clarify performance expectations

4. **Sync:**
   - Implement refactoring changes incrementally
   - Run existing tests to verify functionality is preserved
   - Measure performance improvements
   - Update documentation to reflect architectural changes

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Improved code quality and maintainability
- Reduced technical debt
- Better performance where applicable
- Preserved functionality with all tests passing
- Cleaner architecture and design
- Updated documentation reflecting changes

## Example Commit Message
`DDD: Refactoring Pass - Improved authentication service performance and reduced code complexity`

## Refactoring Focus Areas
- Code duplication elimination
- Complexity reduction
- Performance optimization
- Architectural alignment
- Design pattern application
- Naming improvements
- Code organization
- Interface simplification
- Error handling consistency
- Documentation clarity
- Language-specific guideline compliance
- Consistency across codebase

## Verification Approach
- Run all existing tests to ensure functionality is preserved
- Verify performance metrics before and after changes
- Review changes with team members
- Ensure documentation remains accurate
- Validate that all requirements are still met

## Guidelines
- Make incremental changes with frequent testing
- Focus on one area at a time
- Maintain backward compatibility
- Don't add new features during refactoring
- Keep changes reversible when possible
- Document architectural decisions
- Follow language-specific rules (fetch from agent guidelines links)
- Ensure consistency with existing codebase patterns
- Apply language-specific best practices consistently
