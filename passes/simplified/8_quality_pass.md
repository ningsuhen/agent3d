# Quality Pass

**Purpose:** Verify documentation accuracy and improve quality through enhanced clarity, formatting, and content refinement.

## When to Use
- Before major releases or milestones
- During periodic quality assurance reviews
- When documentation needs refinement for clarity
- Before sharing documentation with new stakeholders
- As part of continuous integration processes

## Process
1. **Scan:**
   - Review all documentation against current code
   - Identify inconsistencies between code and documentation
   - Note areas where clarity can be improved
   - Find outdated or redundant content

2. **Draft:**
   - Document discrepancies and required updates
   - **CRITICAL**: Verify `## Groups` and `### Sub-Groups` heading structure
   - **CRITICAL**: Validate that features marked `[x]` have verifiable evidence (tests or manual verification)
   - **CRITICAL**: Ensure no features marked `[x]` based solely on interface definitions or prototypes
   - Enhance formatting, examples, and explanations
   - Mark sections for removal or archiving
   - Improve diagrams and visual aids

3. **Ask:**
   - Clarify uncertainties about implementation or requirements
   - Confirm which documentation is safe to remove
   - Seek feedback on clarity and readability

4. **Sync:**
   - Apply all approved improvements and corrections
   - Remove or archive outdated content
   - Ensure consistent formatting and terminology

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Verified consistency across all documentation
- Identified and resolved documentation gaps
- Updated status of all features and tasks
- Early detection of documentation drift
- Streamlined, relevant documentation
- Removed references to deprecated features
- Improved documentation maintainability
- Improved readability and clarity
- Consistent formatting and terminology
- Enhanced diagrams and visual aids
- Better examples and explanations

## Related Passes
- **Follows:** [Reverse Pass](10_reverse_pass.md) - Ensures all content exists before quality validation
- **Follows:** [Synchronization Pass](7_synchronization_pass.md) - Ensures alignment before quality checks
- **Precedes:** [Prune Pass](9_prune_pass.md) - Quality validation before content cleanup

## Example Commit Message
`DDD: Quality Pass - Verified documentation accuracy, improved API examples, and removed deprecated features`
