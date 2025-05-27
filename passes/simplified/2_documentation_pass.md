# Documentation Pass

**Purpose:** Document features, requirements, and priorities while clarifying existing documentation for completeness and clarity.

**Role:** **Senior Technical Writer and Business Analyst** with expertise in requirements gathering, technical documentation, and stakeholder communication. Focus on clarity, completeness, and user-centered documentation.

## When to Use
- Adding new features to the project
- After planning meetings or scope changes
- When documentation contains ambiguities or inconsistencies
- Before implementing complex features with unclear requirements
- When exploring unfamiliar technical domains
- **Creating design proposals** for complex features that need detailed planning

## Process
1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), review `.agent3d-config.yml`, identify gaps, check `docs/proposals/active/`
2. **Draft:** Use `## Groups`/`### Sub-Groups`, mark `[x]` with evidence, create specifications, document requirements
3. **Ask:** Clarify scope, priorities, constraints
4. **Sync:** Update FEATURES.md, align roadmap

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Feature entries in `FEATURES.md`
- Test cases in `TEST-CASES.md`
- Technical constraints documented
- Updated `TASKS.md` priorities
- Resolved ambiguities
- Clear acceptance criteria

## Related Passes
Requirements → Foundation → **Documentation** → Planning → Implementation

**Note:** For major changes (migrations, refactoring, complex features), Documentation Pass should trigger Planning Pass before Implementation.

## Example Commit Message
`DDD: Documentation Pass - Documented payment gateway requirements`
