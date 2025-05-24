# Documentation Pass

**Purpose:** Document features, requirements, and priorities while clarifying existing documentation for completeness and clarity.

## When to Use
- Adding new features to the project
- After planning meetings or scope changes
- When documentation contains ambiguities or inconsistencies
- Before implementing complex features with unclear requirements
- When exploring unfamiliar technical domains

## Process
1. **Scan:**
   - Review existing documentation for gaps and inconsistencies
   - Identify where new features fit within current structure
   - Note ambiguities or unclear requirements

2. **Draft:**
   - Create detailed feature specifications with acceptance criteria
   - **🔗 CRITICAL**: Use `## Groups (Modules)` and `### Sub-Groups (Sub-modules)` heading structure
   - **🚨 CRITICAL**: Mark features as `[x]` completed ONLY when verifiable evidence exists (tests or manual verification)
   - Document technical requirements and integration points
   - Update priorities, timelines, and dependencies
   - Prepare questions for unclear areas

3. **Ask:**
   - Clarify feature scope, priorities, and edge cases
   - Resolve ambiguities through stakeholder discussion
   - Confirm technical constraints and dependencies

4. **Sync:**
   - Update `FEATURES.md` and relevant documentation
   - Ensure documentation reflects current project roadmap
   - Document all clarified information and decisions

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

## Example Commit Message
`DDD: Documentation Pass - Documented payment gateway integration requirements and updated Q3 priorities`
