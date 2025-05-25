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
- Documentation that accurately reflects current implementation
- Updated status markers in task lists
- Corrected technical details in specifications
- Aligned feature descriptions with actual functionality
- Updated architectural diagrams reflecting current structure
- Comprehensive feature documentation matching implementation
- Aligned test cases and deployment documentation

## Related Passes
- **Aligns with:** [Requirements Pass](0_requirements_pass.md) - Ensures implementation matches requirements
- **Complements:** [Reverse Pass](10_reverse_pass.md) - Backward alignment (code→docs)
- **Follows:** [Implementation Pass](3_implementation_pass.md) - After code changes
- **Precedes:** [Quality Pass](8_quality_pass.md) - Before quality validation

## Example Commit Message
`DDD: Synchronization Pass - Updated API documentation to match current implementation and reconciled database schema changes`
