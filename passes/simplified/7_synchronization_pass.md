# Synchronization Pass

**Purpose:** Align documentation with code implementation, ensuring consistency between documentation and current codebase.

## When to Use
- After code changes without corresponding documentation updates
- When documentation needs updates to match implementation
- After major refactoring without documentation updates
- During technical debt reduction efforts
- When preparing for releases
- **Legacy documentation refactoring** (e.g., updating `ARCHITECTURE.md` references to `HIGH-LEVEL-DESIGN.md`)

## Process
1. **Scan:**
   - Identify discrepancies between code and documentation
   - Review areas where implementation has diverged from specs
   - Note specific changes that need documentation
   - **Legacy Check**: Search for `ARCHITECTURE.md` references in code, comments, and configuration files

2. **Draft:**
   - Update documentation to match current implementation
   - Revise affected documentation sections
   - Document any new implementation details
   - **Legacy Refactoring**: Update all `ARCHITECTURE.md` references to `HIGH-LEVEL-DESIGN.md`

3. **Ask:**
   - Clarify complex implementation details or design decisions
   - Confirm intended behavior for ambiguous implementations
   - Verify technical constraints and dependencies

4. **Sync:**
   - Ensure documentation accurately reflects current code
   - Update architectural diagrams and specifications
   - Validate alignment across all documentation

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Documentation that accurately reflects current implementation
- Updated status markers in task lists
- Corrected technical details in specifications
- Aligned feature descriptions with actual functionality
- Updated architectural diagrams reflecting current structure
- Comprehensive feature documentation matching implementation
- Aligned test cases and deployment documentation

## Example Commit Message
`DDD: Synchronization Pass - Updated API documentation to match current implementation and reconciled database schema changes`
