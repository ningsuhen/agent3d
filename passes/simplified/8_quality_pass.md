# Quality Pass

**Purpose:** Verify documentation accuracy and improve quality through enhanced clarity, formatting, and content refinement.

## When to Use
- Before major releases or milestones
- During periodic quality assurance reviews
- When documentation needs refinement for clarity
- Before sharing documentation with new stakeholders
- As part of continuous integration processes

## Process
1. **Scan:** Review documentation accuracy, identify clarity improvements, find outdated content
2. **Draft:**
   - **CRITICAL**: Verify `## Groups`/`### Sub-Groups` structure and feature completion evidence
   - Enhance formatting, examples, and explanations
   - Mark content for removal or archiving
3. **Ask:** Clarify requirements, confirm removal decisions, seek readability feedback
4. **Sync:** Apply improvements, remove outdated content, ensure consistent formatting

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Verified consistency and resolved documentation gaps
- Improved readability, clarity, and formatting
- Enhanced examples, diagrams, and explanations
- Streamlined, relevant documentation with deprecated content removed

## Related Passes
- **Follows:** [Reverse Pass](10_reverse_pass.md) - Ensures all content exists before quality validation
- **Follows:** [Synchronization Pass](7_synchronization_pass.md) - Ensures alignment before quality checks
- **Precedes:** [Prune Pass](9_prune_pass.md) - Quality validation before content cleanup

## Example Commit Message
`DDD: Quality Pass - Verified documentation accuracy, improved API examples, and removed deprecated features`
