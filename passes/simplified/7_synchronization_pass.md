# Synchronization Pass

**Purpose:** Align documentation with code implementation, ensuring consistency between documentation and current codebase.

**Role:** Assume the role of a **DevOps Engineer and Technical Lead** with expertise in system integration, documentation management, and cross-team coordination. Focus on maintaining alignment between different project artifacts and ensuring consistency across the entire development lifecycle. Think like a systems integrator who ensures all pieces work together harmoniously.

## When to Use
- After code changes without corresponding documentation updates
- When documentation needs updates to match implementation
- After major refactoring without documentation updates
- During technical debt reduction efforts
- When preparing for releases
- **Legacy documentation refactoring** (e.g., updating `ARCHITECTURE.md` references to `HIGH-LEVEL-DESIGN.md`)

## Process
1. **Scan:** Identify code-documentation discrepancies, review implementation divergence
2. **Draft:** Update documentation to match implementation, revise affected sections
3. **Ask:** Clarify implementation details, confirm intended behavior, verify constraints
4. **Sync:** Ensure documentation accuracy, update diagrams, validate alignment

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Documentation reflects implementation
- Updated status markers
- Corrected technical details
- Aligned feature descriptions
- Updated diagrams
- Aligned test cases

## Related Passes
Implementation → **Synchronization** → Quality

## Example Commit Message
`DDD: Synchronization Pass - Updated API documentation to match implementation`
