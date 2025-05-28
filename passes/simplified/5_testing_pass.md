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

1. **Scan:** Review coverage gaps, analyze `TEST-CASES.md`, identify edge cases, check bug reports
2. **Draft:** Plan test strategy, document edge cases, identify integration scenarios, plan performance tests
3. **Ask:** Clarify edge case behavior, confirm priorities, verify acceptance criteria
4. **Sync:** Implement test suite, add edge case tests, create integration tests, update `TEST-CASES.md`

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes

- Comprehensive test coverage
- Edge case and error tests
- Integration tests
- Updated test documentation
- Increased quality confidence

## Related Passes

Implementation → **Testing** → Refactoring

## Example Commit Message

`DDD: Testing Pass - Added comprehensive test coverage for payment processing`

## Testing Focus

- Edge cases beyond happy path
- Error handling and recovery
- Boundary conditions
- Integration tests
- Performance testing
- Security constraints

## Test Types

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Security tests
- Stress tests
- Regression tests

## Documentation Updates

- Mark automated tests in `TEST-CASES.md`
- Document coverage metrics
- Update test scenarios
- Document issues/limitations
