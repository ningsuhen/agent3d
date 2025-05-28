# Implementation Plan: {{FEATURE_NAME}}

**Created:** {{DATE}}
**Author:** {{AUTHOR}}
**Status:** {{STATUS}} <!-- Draft | Approved | In Progress | Completed | Cancelled -->
**Priority:** {{PRIORITY}} <!-- High | Medium | Low -->
**Estimated Effort:** {{EFFORT_ESTIMATE}} <!-- e.g., 2-3 days, 1 week -->

## Executive Summary

{{BRIEF_DESCRIPTION_OF_CHANGE}}

**Objectives:**
- {{OBJECTIVE_1}}
- {{OBJECTIVE_2}}
- {{OBJECTIVE_3}}

**Success Criteria:**
- {{SUCCESS_CRITERION_1}}
- {{SUCCESS_CRITERION_2}}
- {{SUCCESS_CRITERION_3}}

## Scope and Dependencies

### In Scope
- {{SCOPE_ITEM_1}}
- {{SCOPE_ITEM_2}}
- {{SCOPE_ITEM_3}}

### Out of Scope
- {{OUT_OF_SCOPE_ITEM_1}}
- {{OUT_OF_SCOPE_ITEM_2}}

### Dependencies
- **Internal:** {{INTERNAL_DEPENDENCY_1}}, {{INTERNAL_DEPENDENCY_2}}
- **External:** {{EXTERNAL_DEPENDENCY_1}}, {{EXTERNAL_DEPENDENCY_2}}
- **Prerequisites:** {{PREREQUISITE_1}}, {{PREREQUISITE_2}}

### Affected Components
- {{COMPONENT_1}} - {{IMPACT_DESCRIPTION}}
- {{COMPONENT_2}} - {{IMPACT_DESCRIPTION}}
- {{COMPONENT_3}} - {{IMPACT_DESCRIPTION}}

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| {{RISK_1}} | {{HIGH/MEDIUM/LOW}} | {{HIGH/MEDIUM/LOW}} | {{MITIGATION_1}} |
| {{RISK_2}} | {{HIGH/MEDIUM/LOW}} | {{HIGH/MEDIUM/LOW}} | {{MITIGATION_2}} |
| {{RISK_3}} | {{HIGH/MEDIUM/LOW}} | {{HIGH/MEDIUM/LOW}} | {{MITIGATION_3}} |

### Rollback Complexity
**Level:** {{LOW/MEDIUM/HIGH}}
**Reason:** {{ROLLBACK_COMPLEXITY_EXPLANATION}}

## Step-by-Step Execution Plan

### Phase 1: {{PHASE_1_NAME}}
**Objective:** {{PHASE_1_OBJECTIVE}}

#### Step 1.1: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

#### Step 1.2: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

#### Step 1.3: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

**🔄 CHECKPOINT 1:** {{CHECKPOINT_DESCRIPTION}}
- **Validation Criteria:** {{CHECKPOINT_VALIDATION}}
- **Rollback Instructions:** {{HOW_TO_ROLLBACK_TO_THIS_POINT}}
- **Status:** [ ] Not Reached | [x] Passed

### Phase 2: {{PHASE_2_NAME}}
**Objective:** {{PHASE_2_OBJECTIVE}}

#### Step 2.1: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

#### Step 2.2: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

**🔄 CHECKPOINT 2:** {{CHECKPOINT_DESCRIPTION}}
- **Validation Criteria:** {{CHECKPOINT_VALIDATION}}
- **Rollback Instructions:** {{HOW_TO_ROLLBACK_TO_THIS_POINT}}
- **Status:** [ ] Not Reached | [x] Passed

### Phase 3: {{PHASE_3_NAME}}
**Objective:** {{PHASE_3_OBJECTIVE}}

#### Step 3.1: {{STEP_DESCRIPTION}}
- **Action:** {{DETAILED_ACTION}}
- **Expected Outcome:** {{EXPECTED_RESULT}}
- **Validation:** {{HOW_TO_VERIFY_SUCCESS}}
- **Estimated Time:** {{TIME_ESTIMATE}}
- **Status:** [ ] Not Started | [~] In Progress | [x] Completed

**🔄 FINAL CHECKPOINT:** {{FINAL_CHECKPOINT_DESCRIPTION}}
- **Validation Criteria:** {{FINAL_VALIDATION}}
- **Completion Criteria:** {{COMPLETION_CRITERIA}}
- **Status:** [ ] Not Reached | [x] Passed

## Rollback Strategy

### Emergency Rollback
**Trigger Conditions:** {{WHEN_TO_ROLLBACK}}
**Quick Rollback Steps:**
1. {{EMERGENCY_STEP_1}}
2. {{EMERGENCY_STEP_2}}
3. {{EMERGENCY_STEP_3}}

### Checkpoint-Based Rollback
**From Checkpoint 2 to Checkpoint 1:**
1. {{ROLLBACK_STEP_1}}
2. {{ROLLBACK_STEP_2}}

**From Checkpoint 1 to Initial State:**
1. {{ROLLBACK_STEP_1}}
2. {{ROLLBACK_STEP_2}}

## Validation Criteria

### Per-Step Validation
- Each step includes specific validation criteria
- Automated tests where applicable
- Manual verification procedures documented

### Checkpoint Validation
- **Checkpoint 1:** {{CHECKPOINT_1_CRITERIA}}
- **Checkpoint 2:** {{CHECKPOINT_2_CRITERIA}}
- **Final Checkpoint:** {{FINAL_CRITERIA}}

### Overall Success Criteria
- [ ] All planned steps completed successfully
- [ ] All validation criteria met
- [ ] No regression in existing functionality
- [ ] Documentation updated
- [ ] Tests passing
- [ ] Stakeholder approval received

## Timeline and Effort

| Phase | Estimated Duration | Dependencies | Notes |
|-------|-------------------|--------------|-------|
| Phase 1 | {{DURATION_1}} | {{DEPENDENCIES_1}} | {{NOTES_1}} |
| Phase 2 | {{DURATION_2}} | {{DEPENDENCIES_2}} | {{NOTES_2}} |
| Phase 3 | {{DURATION_3}} | {{DEPENDENCIES_3}} | {{NOTES_3}} |
| **Total** | **{{TOTAL_DURATION}}** | | |

### Resource Requirements
- **Development Time:** {{DEV_TIME}}
- **Testing Time:** {{TEST_TIME}}
- **Review Time:** {{REVIEW_TIME}}
- **External Dependencies:** {{EXTERNAL_TIME}}

## Progress Tracking

### Current Status
- **Overall Progress:** {{PERCENTAGE}}% complete
- **Current Phase:** {{CURRENT_PHASE}}
- **Current Step:** {{CURRENT_STEP}}
- **Last Updated:** {{LAST_UPDATE_DATE}}

### Completed Checkpoints
- [x] Checkpoint 1: {{CHECKPOINT_1_COMPLETION_DATE}}
- [ ] Checkpoint 2: Pending
- [ ] Final Checkpoint: Pending

### Issues and Blockers
| Issue | Severity | Status | Resolution |
|-------|----------|--------|------------|
| {{ISSUE_1}} | {{HIGH/MEDIUM/LOW}} | {{OPEN/RESOLVED}} | {{RESOLUTION_1}} |

## Notes and Decisions

### Key Decisions Made
- **{{DATE}}:** {{DECISION_1}}
- **{{DATE}}:** {{DECISION_2}}

### Lessons Learned
- {{LESSON_1}}
- {{LESSON_2}}

### Future Considerations
- {{FUTURE_CONSIDERATION_1}}
- {{FUTURE_CONSIDERATION_2}}

---

**Template Usage:**
1. Replace all {{PLACEHOLDER}} values with actual content
2. Remove unused sections if not applicable
3. Add additional phases/steps as needed
4. Update status markers as work progresses
5. Remove this template usage section when complete
