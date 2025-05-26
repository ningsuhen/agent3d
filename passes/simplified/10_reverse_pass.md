# Reverse Pass

**Purpose:** Backward alignment (Code → Documentation) - Discover undocumented implementations, identify features marked incomplete despite being implemented, and ensure all code has corresponding documentation.

**Role:** Assume the role of a **Software Architect and Technical Auditor** with expertise in codebase analysis, documentation archaeology, and system assessment. Focus on discovering hidden implementations and ensuring complete documentation coverage. Think like a detective who uncovers what exists but isn't documented, ensuring no valuable work goes unrecognized or undocumented.

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

   - **Common Setup**: Follow [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management)
   - **Code Discovery**: Analyze codebase for implemented functionality not reflected in documentation
   - **Feature Status Audit**: Find features marked as `[ ]` or `[~]` that are actually working and complete
   - **Implementation Hunt**: Search for working code that lacks corresponding documentation
1. **Draft:**

   - **🔍 CRITICAL**: Systematically compare implementation against FEATURES.md status
   - **🔍 CRITICAL**: Identify features marked incomplete that have verifiable working implementations
   - Document all discovered undocumented functionality
   - Create list of features that should be marked `[x]` completed
1. **Ask:** Validate discovered functionality, confirm feature completion status, verify acceptance criteria
1. **Sync:** Update FEATURES.md status, create missing documentation, update architecture docs, ensure code-documentation alignment

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

## Related Passes

- **Validates:** [Requirements Pass](0_requirements_pass.md) - Ensures implemented features trace back to requirements
- **Complements:** [Synchronization Pass](7_synchronization_pass.md) - Forward alignment (docs→code)
- **Precedes:** [Quality Pass](8_quality_pass.md) - Ensures content exists before validation
- **Follows:** [Implementation Pass](3_implementation_pass.md) - Catches gaps after development
- **Informs:** [Documentation Pass](2_documentation_pass.md) - Identifies missing documentation

## Example Commit Message

`DDD: Reverse Pass - Updated documentation for payment processing features, marked 5 completed features as [x], added missing API documentation`

## Automation Opportunities

- **Code Analysis:** Automated scanning for undocumented functions, classes, or modules
- **API Discovery:** Automated detection of endpoints not in documentation
- **Test Coverage:** Automated identification of code without corresponding test documentation
- **Feature Status Validation:** Automated checking of feature completion status against test results