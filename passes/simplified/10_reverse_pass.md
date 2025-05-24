# Reverse Pass

**Purpose:** Detect and address reverse drift by identifying implemented features that lack documentation, features marked as incomplete despite being implemented, and code that exists without corresponding documentation.

## When to Use
- After significant development work without documentation updates
- When suspecting that implementation has outpaced documentation
- Before major releases to ensure documentation completeness
- During onboarding new team members who need accurate documentation
- When code reviews reveal undocumented functionality
- As part of regular maintenance to prevent documentation debt

## Process
1. **Scan:**
   - Analyze codebase for implemented functionality not reflected in documentation
   - Identify features marked as `[ ]` or `[~]` that are actually working and complete
   - Find API endpoints, database schemas, or components without documentation
   - Detect test coverage gaps for existing functionality
   - Check for configuration changes not reflected in setup documentation

2. **Draft:**
   - **🔍 CRITICAL**: Systematically compare implementation against FEATURES.md status
   - **🔍 CRITICAL**: Identify features marked incomplete that have verifiable working implementations
   - Document all discovered undocumented functionality
   - Create list of features that should be marked `[x]` completed
   - Prepare documentation updates for undocumented implementations
   - Plan test case additions for uncovered functionality

3. **Ask:**
   - Clarify whether undocumented functionality is intentional or oversight
   - Confirm which implemented features should be marked as completed
   - Verify that discovered functionality meets acceptance criteria
   - Discuss whether some implementations should be considered experimental

4. **Sync:**
   - Update FEATURES.md to mark verified complete features as `[x]`
   - Add documentation for all confirmed undocumented functionality
   - Create or update test cases for uncovered implementations
   - Update ARCHITECTURE.md with any undocumented components or changes
   - Ensure all working features have proper acceptance criteria validation

**Note:** During execution, mark completed steps with ✅ to track progress.

## Reverse Drift Detection Checklist

### Implementation Without Documentation
- [ ] Code features not documented in FEATURES.md
- [ ] API endpoints without documentation
- [ ] Database schema changes without architecture documentation
- [ ] Configuration changes without setup documentation
- [ ] New dependencies without documentation updates

### Features Marked Incomplete Despite Implementation
- [ ] Features marked `[ ]` that have working implementations
- [ ] Features marked `[~]` that are actually complete and tested
- [ ] Features with passing tests but not marked as `[x]` completed

### Code Without Test Coverage Documentation
- [ ] Implemented functionality without corresponding test cases in TEST-CASES.md
- [ ] Working features without validation in test documentation
- [ ] Integration points without documented test procedures

### Architecture Drift
- [ ] New components not reflected in ARCHITECTURE.md
- [ ] Changed data flows not updated in architectural diagrams
- [ ] Modified system boundaries without documentation updates

## Expected Outcomes
- All implemented functionality is properly documented
- Features marked as `[x]` completed accurately reflect working implementations
- No working features remain marked as `[ ]` pending or `[~]` in-progress
- Complete test case coverage documentation for all implementations
- Updated ARCHITECTURE.md reflecting actual system state
- Eliminated reverse drift between code and documentation
- Accurate project status in DDD-STATUS.md
- Comprehensive feature documentation with verified acceptance criteria

## Integration with Other Passes
- **Complements Synchronization Pass:** While Sync focuses on forward alignment, Reverse focuses on backward alignment
- **Precedes Quality Pass:** Ensures all content exists before quality validation
- **Follows Implementation Pass:** Catches documentation gaps after development work
- **Informs Documentation Pass:** Identifies what documentation needs to be created or updated

## Example Commit Message
`DDD: Reverse Pass - Updated documentation for payment processing features, marked 5 completed features as [x], added missing API documentation`

## Automation Opportunities
- **Code Analysis:** Automated scanning for undocumented functions, classes, or modules
- **API Discovery:** Automated detection of endpoints not in documentation
- **Test Coverage:** Automated identification of code without corresponding test documentation
- **Feature Status Validation:** Automated checking of feature completion status against test results
