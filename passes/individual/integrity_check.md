# Integrity Check

**Purpose:** A **quick, automated pass** to ensure no new drift has occurred since the last commit, often integrated into CI/CD pipelines.

## When to Use
- As part of continuous integration processes
- Before merging pull requests
- During automated build processes
- For routine verification of documentation integrity

## Process
1. **Scan:** Automatically detect inconsistencies between code and documentation
2. **Draft:** Generate reports of detected discrepancies
3. **Ask:** (Usually automated, but may require clarification for false positives)
4. **Sync:** Flag issues for resolution before proceeding

## Expected Outcomes
- Automated verification of documentation accuracy
- Early detection of documentation drift
- Prevented merging of code without documentation updates
- Maintained documentation integrity throughout development

## Example Commit Message
`DDD: Integrity Check - Automated verification of documentation completeness`
