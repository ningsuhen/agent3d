# Implementation Pass

**Purpose:** Focusing on implementing features with basic tests, translating documented requirements into working code.

**Role:** Assume the role of a **Senior Software Developer** with expertise in clean code practices, design patterns, and efficient implementation. Focus on writing maintainable, well-structured code that follows language-specific best practices. Think like a craftsperson who takes pride in elegant, robust solutions.

## When to Use

- When feature documentation is complete and ready for implementation
- After a Documentation Pass (and Development Pass for major changes) has established clear requirements
- When starting the development phase of a feature
- When converting a proof of concept into production code
- When an implementation plan exists and has been validated

## Process

1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), review documentation, validate implementation plan exists (for major changes), check TEST-CASES.md
2. **Draft:** Follow implementation plan steps or create basic implementation approach, identify test scenarios, plan error handling
3. **Ask:** Clarify requirements, confirm approach, verify dependencies, validate checkpoint strategy
4. **Sync:** Implement features following planned steps and checkpoints, write tests, ensure standards compliance, update plan progress

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes

- Working implementation
- Basic test coverage
- Passing tests
- Standards compliance
- Updated documentation

## Related Passes

Requirements → Documentation → Development → **Implementation** → Testing

**Note:** Development Pass includes planning and implementation phases for comprehensive feature development.

## Example Commit Message

`DDD: Implementation Pass - Implemented user authentication`

## Testing Focus

- Happy path test cases
- Basic validation tests
- Core functionality coverage
- Foundation for comprehensive testing

## Implementation Guidelines

- Follow language-specific rules
- Implement documented requirements only
- Keep code lean
- Document technical decisions
- Ensure readability

## Working with Development Plans

### For Major Changes (with Development Pass)

1. **Validate Plan Exists:** Check for `docs/runs/EXEC-PLAN-{change-name}.md`
2. **Follow Step Sequence:** Execute steps in planned order
3. **Update Progress:** Mark steps as completed `[x]` in the plan
4. **Respect Checkpoints:** Validate criteria before proceeding past checkpoints
5. **Handle Failures:** Use rollback instructions if issues arise
6. **Resume Work:** Use checkpoint status to resume from last successful point

### For Minor Changes (direct implementation)

1. **Create Simple Plan:** Basic implementation approach in DRAFT phase
2. **Document Steps:** Simple checklist of implementation tasks
3. **Track Progress:** Mark completed tasks during SYNC phase

### Checkpoint Management

- **Before Each Checkpoint:** Validate all criteria are met
- **At Checkpoint Failure:** Follow rollback instructions to previous checkpoint
- **Progress Updates:** Update implementation plan with current status
- **Issue Tracking:** Document any blockers or deviations in the plan
