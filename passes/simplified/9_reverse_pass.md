# Reverse Pass

**Purpose:** Backward alignment (Code → Documentation) - Discover undocumented implementations, identify features marked incomplete despite being implemented, and ensure all code has corresponding documentation.

**Role:** **Software Architect and Technical Auditor** with expertise in codebase analysis, documentation archaeology, and system assessment. Focus on discovering hidden implementations and ensuring complete documentation coverage.

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

1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), analyze codebase, audit feature status, hunt implementations
2. **Draft:** Compare implementation vs FEATURES.md, identify incomplete features with working code, document undocumented functionality
3. **Ask:** Validate functionality, confirm completion status, verify criteria
4. **Sync:** Update FEATURES.md status, create missing docs, update architecture, ensure alignment

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

- All functionality documented
- Accurate `[x]` completion markers
- No working features marked incomplete
- Complete test coverage documentation
- Updated architecture docs
- Eliminated reverse drift
- Accurate project status

## Related Passes

Implementation → **Reverse** → Prune

## Example Commit Message

`DDD: Reverse Pass - Updated payment processing docs, marked 5 features complete`

## Automation Opportunities

- **Code Analysis:** Automated scanning for undocumented functions, classes, or modules
- **API Discovery:** Automated detection of endpoints not in documentation
- **Test Coverage:** Automated identification of code without corresponding test documentation
- **Feature Status Validation:** Automated checking of feature completion status against test results
