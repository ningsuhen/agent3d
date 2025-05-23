# Synchronization Pass

**Purpose:** Aligning documentation with code at any scale, from minor updates to major reconciliations, ensuring consistency between implementation and documentation.

**Combines:** Alignment Pass + Reconciliation Pass

## When to Use
- After code changes that weren't documented (small or large)
- When implementing features or bug fixes of any size
- When documentation needs updates to match implementation
- After major refactoring without documentation updates
- When significant undocumented features have been implemented
- During technical debt reduction efforts
- When preparing for a release

## Process
1. **Scan:** 
   - Identify discrepancies between code and documentation (of any scale)
   - Comprehensively identify all areas of divergence
   - Identify specific changes that need documentation

2. **Draft:** 
   - Make targeted updates to documentation
   - Create detailed updates to bring documentation in line with code
   - Update affected documentation sections

3. **Ask:** 
   - Clarify uncertainties about implementation details
   - Clarify complex implementation details or design decisions
   - Clarify details about specific changes

4. **Sync:** 
   - Ensure documentation accurately reflects current code
   - Ensure documentation fully reflects the current implementation
   - Ensure specific changes are accurately documented

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
