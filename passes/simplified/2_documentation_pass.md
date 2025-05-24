# Documentation Pass

**Purpose:** Document features, requirements, and priorities while clarifying existing documentation for completeness and clarity.

## When to Use
- Adding new features to the project
- After planning meetings or scope changes
- When documentation contains ambiguities or inconsistencies
- Before implementing complex features with unclear requirements
- When exploring unfamiliar technical domains
- **Creating design proposals** for complex features that need detailed planning

## Process
1. **Scan:**
   - **Repository Update**: `git -C ~/.agent3d pull origin main`
   - Review existing documentation for gaps and inconsistencies
   - Identify where new features fit within current structure
   - **Proposal Check**: Review `docs/proposals/active/` for relevant design proposals

2. **Draft:**
   - **CRITICAL**: Use `## Groups`/`### Sub-Groups` structure and mark `[x]` only with verifiable evidence
   - Create detailed feature specifications with acceptance criteria
   - Document technical requirements and integration points
   - Create proposals using templates for complex features

3. **Ask:** Clarify feature scope, priorities, edge cases, and technical constraints

4. **Sync:** Update FEATURES.md and documentation, ensure roadmap alignment

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Detailed feature entries in `FEATURES.md`
- Associated test cases in `TEST-CASES.md`
- Documented technical constraints and limitations
- Updated `TASKS.md` with current priorities
- Revised feature documentation reflecting scope changes
- Resolved ambiguities in documentation
- Consistent terminology and specifications
- Clear acceptance criteria for features

## Related Passes
- **Follows:** [Foundation Pass](1_foundation_pass.md) - After foundation documents are established
- **Precedes:** [Implementation Pass](3_implementation_pass.md) - Before feature implementation
- **Templates:** See `~/.agent3d/templates/` for FEATURES, PROPOSAL format specifications

## Example Commit Message
`DDD: Documentation Pass - Documented payment gateway integration requirements and updated Q3 priorities`
