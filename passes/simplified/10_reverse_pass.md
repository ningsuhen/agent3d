# Reverse Pass

**Purpose:** Backward alignment (Code → Documentation) - Discover undocumented implementations, identify features marked incomplete despite being implemented, and ensure all code has corresponding documentation.

## When to Use
- When suspecting undocumented implementations exist in the codebase
- After significant development work without documentation updates
- Before major releases to discover hidden/forgotten implementations
- During onboarding new team members who need complete documentation
- When code reviews reveal undocumented functionality
- As part of regular maintenance to hunt for documentation debt
- When auditing codebase for completeness and accuracy
- After periods of rapid development to catch up documentation

## Process
1. **Scan:**
   - **Repository Update**: Ensure `~/.agent3d` repository is current with `git -C ~/.agent3d pull origin main`
   - **Code Discovery**: Analyze codebase for implemented functionality not reflected in documentation
   - **Feature Status Audit**: Find features marked as `[ ]` or `[~]` that are actually working and complete
   - **API Discovery**: Locate API endpoints, database schemas, or components without documentation
   - **Implementation Hunt**: Search for working code that lacks corresponding documentation
   - **Test Coverage Analysis**: Detect test coverage gaps for existing functionality
   - **Configuration Audit**: Check for configuration changes not reflected in setup documentation

2. **Draft:**
   - **🔍 CRITICAL**: Systematically compare implementation against FEATURES.md status
   - **🔍 CRITICAL**: Identify features marked incomplete that have verifiable working implementations
   - **Discovery Documentation**: Document all discovered undocumented functionality
   - **Status Corrections**: Create list of features that should be marked `[x]` completed
   - **Gap Analysis**: Prepare documentation updates for undocumented implementations
   - **Test Case Planning**: Plan test case additions for uncovered functionality
   - **Implementation Inventory**: Catalog all working code that lacks documentation

3. **Ask:**
   - **Discovery Validation**: Clarify whether undocumented functionality is intentional or oversight
   - **Status Confirmation**: Confirm which implemented features should be marked as completed
   - **Acceptance Verification**: Verify that discovered functionality meets acceptance criteria
   - **Implementation Classification**: Discuss whether some implementations should be considered experimental
   - **Design Clarification**: Clarify complex implementation details or design decisions
   - **Behavior Confirmation**: Confirm intended behavior for ambiguous implementations

4. **Sync:**
   - **Status Updates**: Update FEATURES.md to mark verified complete features as `[x]`
   - **Documentation Creation**: Add documentation for all confirmed undocumented functionality
   - **Architecture Updates**: Update HIGH-LEVEL-DESIGN.md with any undocumented components or changes
   - **Test Documentation**: Create or update test cases for uncovered implementations
   - **Acceptance Validation**: Ensure all working features have proper acceptance criteria validation
   - **Cross-Reference Updates**: Update all documentation files to reflect discovered implementations
   - **Completeness Verification**: Validate that all code now has corresponding documentation

**Note:** During execution, mark completed steps with ✅ to track progress.

## Drift Detection Checklist

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

### Documentation Without Implementation
- [ ] Features marked `[x]` that don't actually work or exist
- [ ] Documented APIs that aren't implemented
- [ ] Architectural components described but not built
- [ ] Test cases for non-existent functionality

### Code Without Test Coverage Documentation
- [ ] Implemented functionality without corresponding test cases in TEST-CASES.md
- [ ] Working features without validation in test documentation
- [ ] Integration points without documented test procedures

### Architecture Drift
- [ ] New components not reflected in HIGH-LEVEL-DESIGN.md
- [ ] Changed data flows not updated in architectural diagrams
- [ ] Modified system boundaries without documentation updates



## Expected Outcomes
- All implemented functionality is properly documented
- Features marked as `[x]` completed accurately reflect working implementations
- No working features remain marked as `[ ]` pending or `[~]` in-progress
- Complete test case coverage documentation for all implementations
- Updated HIGH-LEVEL-DESIGN.md reflecting actual system state
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
