# Documentation Pass

**Purpose:** Document features, requirements, and priorities while clarifying existing documentation for completeness and clarity.

**Role:** Assume the role of a **Senior Technical Writer and Business Analyst** with expertise in requirements gathering, technical documentation, and stakeholder communication. Focus on clarity, completeness, and user-centered documentation. Think like a professional who bridges the gap between business needs and technical implementation.

## When to Use
- Adding new features to the project
- After planning meetings or scope changes
- When documentation contains ambiguities or inconsistencies
- Before implementing complex features with unclear requirements
- When exploring unfamiliar technical domains
- **Creating design proposals** for complex features that need detailed planning

## Process
1. **Scan:**
   - **Common Setup**: Follow [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management)
   - Review `.agent3d-config.yml` for project configuration and enabled passes
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
- **Builds on:** [Requirements Pass](0_requirements_pass.md) - Uses business requirements for documentation scope
- **Follows:** [Foundation Pass](1_foundation_pass.md) - After project configuration is established
- **Precedes:** [Implementation Pass](3_implementation_pass.md) - Before feature implementation
- **Templates:** See `~/.agent3d/templates/` for FEATURES, PROPOSAL format specifications

## Example Commit Message
`DDD: Documentation Pass - Documented payment gateway integration requirements and updated Q3 priorities`
