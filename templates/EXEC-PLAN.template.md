# Execution Plan: {{CHANGE_NAME}}

**Created:** {{DATE}}  
**Author:** {{AUTHOR}}  
**Status:** {{STATUS}} <!-- Draft | In Progress | Complete | Failed -->  
**Type:** {{TYPE}} <!-- Feature Implementation | Refactoring | Migration | Bug Fix | Enhancement -->  
**Priority:** {{PRIORITY}} <!-- High | Medium | Low -->  
**Estimated Duration:** {{EFFORT_ESTIMATE}} <!-- e.g., 2-3 hours, 1 day, 1 week -->

## Change Overview

{{BRIEF_DESCRIPTION_OF_CHANGE}}

**Scope:** {{SCOPE_DESCRIPTION}}

## Feature Discovery Results

### Analyzed Documents

- [ ] docs/FEATURES.md - {{FEATURES_FOUND}} features found, {{INCOMPLETE_COUNT}} incomplete
- [ ] docs/TASKS.md - {{TASKS_FOUND}} tasks identified
- [ ] docs/DDD-STATUS.md - {{DRIFT_COUNT}} drift indicators found
- [ ] docs/REQUIREMENTS.md - {{REQ_COUNT}} requirements analyzed
- [ ] Other relevant docs: {{OTHER_DOCS}}

### Selected Features for Implementation

{{SELECTION_MODE}} <!-- AUTO MODE | PICKER MODE -->

#### Selected Items

1. **{{FEATURE_1}}** ({{REQ_ID_1}})
   - Priority: {{PRIORITY_1}}
   - Estimated Effort: {{EFFORT_1}}
   - Dependencies: {{DEPENDENCIES_1}}

2. **{{FEATURE_2}}** ({{REQ_ID_2}})
   - Priority: {{PRIORITY_2}}
   - Estimated Effort: {{EFFORT_2}}
   - Dependencies: {{DEPENDENCIES_2}}

## Step-by-Step Execution Plan

### Step 1: {{STEP_1_DESCRIPTION}}

**Status**: [ ] Not Started | [~] In Progress | [x] Complete
**Feature**: {{RELATED_FEATURE_1}}
**Description**: {{DETAILED_STEP_DESCRIPTION}}
**LLM Instructions**:

- {{SPECIFIC_INSTRUCTION_1}}
- {{SPECIFIC_INSTRUCTION_2}}
- {{SPECIFIC_INSTRUCTION_3}}
**Verification Criteria**:
- [ ] {{VERIFICATION_1}}
- [ ] {{VERIFICATION_2}}
- [ ] {{VERIFICATION_3}}
**Estimated Time**: {{TIME_ESTIMATE}}

### Step 2: {{STEP_2_DESCRIPTION}}

**Status**: [ ] Not Started
**Feature**: {{RELATED_FEATURE_2}}
**Description**: {{DETAILED_STEP_DESCRIPTION}}
**LLM Instructions**:

- {{SPECIFIC_INSTRUCTION_1}}
- {{SPECIFIC_INSTRUCTION_2}}
- {{SPECIFIC_INSTRUCTION_3}}
**Verification Criteria**:
- [ ] {{VERIFICATION_1}}
- [ ] {{VERIFICATION_2}}
- [ ] {{VERIFICATION_3}}
**Estimated Time**: {{TIME_ESTIMATE}}

### Step 3: {{STEP_3_DESCRIPTION}}

**Status**: [ ] Not Started
**Feature**: {{RELATED_FEATURE_3}}
**Description**: {{DETAILED_STEP_DESCRIPTION}}
**LLM Instructions**:

- {{SPECIFIC_INSTRUCTION_1}}
- {{SPECIFIC_INSTRUCTION_2}}
- {{SPECIFIC_INSTRUCTION_3}}
**Verification Criteria**:
- [ ] {{VERIFICATION_1}}
- [ ] {{VERIFICATION_2}}
- [ ] {{VERIFICATION_3}}
**Estimated Time**: {{TIME_ESTIMATE}}

### Checkpoint 1: {{CHECKPOINT_1_NAME}}

**Steps Included**: 1-3
**Status**: [ ] Pending | [x] Passed | [!] Failed
**Verification**:

- [ ] {{CHECKPOINT_VERIFICATION_1}}
- [ ] {{CHECKPOINT_VERIFICATION_2}}
- [ ] {{CHECKPOINT_VERIFICATION_3}}
**Rollback Instructions**: {{ROLLBACK_INSTRUCTIONS_1}}

### Step 4: {{STEP_4_DESCRIPTION}}

**Status**: [ ] Not Started
**Feature**: {{RELATED_FEATURE_4}}
**Description**: {{DETAILED_STEP_DESCRIPTION}}
**LLM Instructions**:

- {{SPECIFIC_INSTRUCTION_1}}
- {{SPECIFIC_INSTRUCTION_2}}
**Verification Criteria**:
- [ ] {{VERIFICATION_1}}
- [ ] {{VERIFICATION_2}}
**Estimated Time**: {{TIME_ESTIMATE}}

### Step 5: {{STEP_5_DESCRIPTION}}

**Status**: [ ] Not Started
**Feature**: {{RELATED_FEATURE_5}}
**Description**: {{DETAILED_STEP_DESCRIPTION}}
**LLM Instructions**:

- {{SPECIFIC_INSTRUCTION_1}}
- {{SPECIFIC_INSTRUCTION_2}}
**Verification Criteria**:
- [ ] {{VERIFICATION_1}}
- [ ] {{VERIFICATION_2}}
**Estimated Time**: {{TIME_ESTIMATE}}

### Checkpoint 2: {{CHECKPOINT_2_NAME}}

**Steps Included**: 4-5
**Status**: [ ] Pending
**Verification**:

- [ ] {{CHECKPOINT_VERIFICATION_1}}
- [ ] {{CHECKPOINT_VERIFICATION_2}}
**Rollback Instructions**: {{ROLLBACK_INSTRUCTIONS_2}}

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| {{RISK_1}} | {{HIGH/MEDIUM/LOW}} | {{HIGH/MEDIUM/LOW}} | {{MITIGATION_1}} |
| {{RISK_2}} | {{HIGH/MEDIUM/LOW}} | {{HIGH/MEDIUM/LOW}} | {{MITIGATION_2}} |

## Dependencies

### Internal Dependencies

- {{INTERNAL_DEPENDENCY_1}}
- {{INTERNAL_DEPENDENCY_2}}

### External Dependencies

- {{EXTERNAL_DEPENDENCY_1}}
- {{EXTERNAL_DEPENDENCY_2}}

### Prerequisites

- {{PREREQUISITE_1}}
- {{PREREQUISITE_2}}

## Execution Summary

**Total Steps**: {{TOTAL_STEPS}}
**Completed**: {{COMPLETED_COUNT}}
**In Progress**: {{IN_PROGRESS_COUNT}}
**Remaining**: {{REMAINING_COUNT}}
**Current Phase**: {{CURRENT_PHASE}}
**Next Milestone**: {{NEXT_MILESTONE}}

## Loop Execution Status

**Loop Iteration**: {{CURRENT_ITERATION}}
**Next Step to Execute**: Step {{NEXT_STEP_NUMBER}}
**Last Completed**: {{LAST_COMPLETED_STEP}}
**Estimated Completion**: {{ESTIMATED_COMPLETION_DATE}}

## Quality Gates

- [ ] All steps completed successfully
- [ ] All verification criteria met
- [ ] All checkpoints passed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Standards compliance verified
- [ ] No regressions introduced

---

**Template Usage:**

1. Replace all {{PLACEHOLDER}} values with actual content
2. Add or remove steps as needed for your specific change
3. Update status markers as work progresses: [ ] → [~] → [x]
4. Use checkpoint frequency of 2-4 steps
5. Remove this template usage section when complete
