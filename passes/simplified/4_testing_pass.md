# Testing Pass

**Purpose:** Adding comprehensive test coverage and verifying edge cases, focusing on the test cases documented in `TEST-CASES.md`.

**Role:** Assume the role of a **Senior QA Engineer** with expertise in test strategy, automation, and quality assurance. Apply rigorous testing methodologies, focus on edge cases, and ensure comprehensive coverage. Think like a quality-focused professional who takes pride in finding issues before they reach production.

## When to Use
- After an Implementation Pass has established basic functionality
- When increasing test coverage for existing features
- Before releasing features to production
- When addressing quality concerns or bug reports
- As part of regular quality assurance cycles

## Process
1. **Scan:**
   - Review existing test coverage and identify gaps
   - Analyze `TEST-CASES.md` for untested scenarios
   - Identify edge cases and error conditions
   - Review bug reports or quality concerns

2. **Draft:**
   - Plan comprehensive test strategy
   - Document additional test cases for edge conditions
   - Identify integration test scenarios
   - Plan performance or stress tests if applicable

3. **Ask:**
   - Clarify expected behavior for edge cases
   - Confirm test priorities and coverage goals
   - Discuss complex test scenarios or setup requirements
   - Verify acceptance criteria for tests

4. **Sync:**
   - Implement comprehensive test suite
   - Add tests for edge cases and error conditions
   - Create integration tests for component interactions
   - Update `TEST-CASES.md` with test status

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Comprehensive test coverage for features
- Tests for edge cases and error conditions
- Integration tests for component interactions
- Updated test documentation with status
- Increased confidence in code quality and reliability

## Related Passes
- **Validates:** [Requirements Pass](0_requirements_pass.md) - Tests verify requirements are met
- **Follows:** [Implementation Pass](3_implementation_pass.md) - After basic functionality is implemented
- **Precedes:** [Refactoring Pass](5_refactoring_pass.md) - Before code cleanup and optimization

## Example Commit Message
`DDD: Testing Pass - Added comprehensive test coverage for payment processing including edge cases`

## Testing Focus
- Expand beyond "happy path" to edge cases
- Test error handling and recovery
- Verify boundary conditions and input validation
- Create integration tests for component interactions
- Test performance under various conditions
- Verify security constraints and access controls

## Test Types to Consider
- Unit tests for individual components
- Integration tests for component interactions
- End-to-end tests for critical user flows
- Performance tests for response time and throughput
- Security tests for access controls and data protection
- Stress tests for system behavior under load
- Regression tests to prevent regressions

## Documentation Updates
- Mark test cases as automated in `TEST-CASES.md`
- Document test coverage metrics
- Update test documentation with new scenarios
- Document any discovered issues or limitations
