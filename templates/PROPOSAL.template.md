# {{proposal_name}} - Proposal

**STATUS:** {{status}} (Draft | Under Review | Approved | Rejected | Implemented)
**CREATED:** {{date}}
**LAST UPDATED:** {{date}}
**AUTHOR(S):** {{author_names}}
**REVIEWERS:** {{reviewer_names}}

**FORMAT SPECIFICATION:** This document must provide a comprehensive proposal for unimplemented features, modules, or system changes. It must include:
- Clear problem statement and motivation
- Proposed solution with detailed design
- Implementation approach and timeline
- Risk assessment and mitigation strategies
- Success criteria and acceptance criteria
- Integration plan with existing systems
- Resource requirements and dependencies
- Alternative approaches considered

**REQUIRED SECTIONS:**
1. Problem Statement - What problem this proposal solves
2. Motivation - Why this solution is needed now
3. Proposed Solution - Detailed design and approach
4. Implementation Plan - Timeline, phases, and milestones
5. Risk Assessment - Potential risks and mitigation strategies
6. Success Criteria - How success will be measured
7. Integration Plan - How this fits with existing systems
8. Resource Requirements - People, time, and infrastructure needed
9. Alternatives Considered - Other approaches evaluated
10. Decision Points - Key decisions that need to be made

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# {{proposal_name}} - Proposal

**STATUS:** {{status}}
**CREATED:** {{creation_date}}
**LAST UPDATED:** {{last_updated}}
**AUTHOR(S):** {{author_names}}
**REVIEWERS:** {{reviewer_names}}

## Problem Statement

{{problem_description}}

### Current State
{{current_state_description}}

### Pain Points
- {{pain_point_1}}
- {{pain_point_2}}
- {{pain_point_3}}

## Motivation

{{motivation_description}}

### Business Value
- {{business_value_1}}
- {{business_value_2}}
- {{business_value_3}}

### Technical Benefits
- {{technical_benefit_1}}
- {{technical_benefit_2}}
- {{technical_benefit_3}}

### User Impact
{{user_impact_description}}

## Proposed Solution

### Overview
{{solution_overview}}

### Architecture
```mermaid
{{architecture_diagram}}
```

### Key Components
#### {{component_name}}
- **Purpose**: {{component_purpose}}
- **Responsibilities**: {{component_responsibilities}}
- **Interface**: {{component_interface}}

#### {{component_name}}
- **Purpose**: {{component_purpose}}
- **Responsibilities**: {{component_responsibilities}}
- **Interface**: {{component_interface}}

### Data Flow
```mermaid
{{data_flow_diagram}}
```

{{data_flow_description}}

### API Design
```{{language}}
{{api_specification}}
```

### Configuration
```{{format}}
{{configuration_schema}}
```

## Implementation Plan

### Phase 1: {{phase_name}} ({{timeline}})
- {{milestone_1}}
- {{milestone_2}}
- {{milestone_3}}

### Phase 2: {{phase_name}} ({{timeline}})
- {{milestone_1}}
- {{milestone_2}}
- {{milestone_3}}

### Phase 3: {{phase_name}} ({{timeline}})
- {{milestone_1}}
- {{milestone_2}}
- {{milestone_3}}

### Dependencies
- **{{dependency_name}}**: {{dependency_description}}
- **{{dependency_name}}**: {{dependency_description}}

### Deliverables
- {{deliverable_1}}
- {{deliverable_2}}
- {{deliverable_3}}

## Risk Assessment

### High Risk
- **{{risk_name}}**: {{risk_description}}
  - **Probability**: {{probability}}
  - **Impact**: {{impact}}
  - **Mitigation**: {{mitigation_strategy}}

### Medium Risk
- **{{risk_name}}**: {{risk_description}}
  - **Probability**: {{probability}}
  - **Impact**: {{impact}}
  - **Mitigation**: {{mitigation_strategy}}

### Low Risk
- **{{risk_name}}**: {{risk_description}}
  - **Probability**: {{probability}}
  - **Impact**: {{impact}}
  - **Mitigation**: {{mitigation_strategy}}

## Success Criteria

### Functional Requirements
- {{functional_requirement_1}}
- {{functional_requirement_2}}
- {{functional_requirement_3}}

### Non-Functional Requirements
- **Performance**: {{performance_criteria}}
- **Scalability**: {{scalability_criteria}}
- **Reliability**: {{reliability_criteria}}
- **Security**: {{security_criteria}}

### Acceptance Criteria
- {{acceptance_criteria_1}}
- {{acceptance_criteria_2}}
- {{acceptance_criteria_3}}

### Key Performance Indicators (KPIs)
- {{kpi_1}}: {{target_value}}
- {{kpi_2}}: {{target_value}}
- {{kpi_3}}: {{target_value}}

## Integration Plan

### Existing System Integration
{{integration_description}}

### Migration Strategy
{{migration_strategy}}

### Rollback Plan
{{rollback_plan}}

### Testing Strategy
- **Unit Testing**: {{unit_testing_approach}}
- **Integration Testing**: {{integration_testing_approach}}
- **Performance Testing**: {{performance_testing_approach}}
- **User Acceptance Testing**: {{uat_approach}}

## Resource Requirements

### Team Structure
- **{{role_name}}**: {{role_description}} ({{time_commitment}})
- **{{role_name}}**: {{role_description}} ({{time_commitment}})
- **{{role_name}}**: {{role_description}} ({{time_commitment}})

### Infrastructure
- {{infrastructure_requirement_1}}
- {{infrastructure_requirement_2}}
- {{infrastructure_requirement_3}}

### Budget Estimate
- **Development**: {{development_cost}}
- **Infrastructure**: {{infrastructure_cost}}
- **Maintenance**: {{maintenance_cost}}
- **Total**: {{total_cost}}

### Timeline
- **Total Duration**: {{total_duration}}
- **Start Date**: {{start_date}}
- **Target Completion**: {{completion_date}}

## Alternatives Considered

### Alternative 1: {{alternative_name}}
- **Description**: {{alternative_description}}
- **Pros**: {{alternative_pros}}
- **Cons**: {{alternative_cons}}
- **Why Not Chosen**: {{rejection_reason}}

### Alternative 2: {{alternative_name}}
- **Description**: {{alternative_description}}
- **Pros**: {{alternative_pros}}
- **Cons**: {{alternative_cons}}
- **Why Not Chosen**: {{rejection_reason}}

### Do Nothing
- **Impact**: {{do_nothing_impact}}
- **Cost**: {{do_nothing_cost}}
- **Why Not Acceptable**: {{do_nothing_rejection}}

## Decision Points

### Technical Decisions
- **{{decision_name}}**: {{decision_description}}
  - **Options**: {{decision_options}}
  - **Recommendation**: {{recommendation}}
  - **Rationale**: {{decision_rationale}}

### Business Decisions
- **{{decision_name}}**: {{decision_description}}
  - **Options**: {{decision_options}}
  - **Recommendation**: {{recommendation}}
  - **Rationale**: {{decision_rationale}}

## Next Steps

### Immediate Actions
- [ ] {{action_item_1}}
- [ ] {{action_item_2}}
- [ ] {{action_item_3}}

### Review Process
- {{review_step_1}}
- {{review_step_2}}
- {{review_step_3}}

### Approval Requirements
- {{approval_requirement_1}}
- {{approval_requirement_2}}
- {{approval_requirement_3}}

## Appendices

### Appendix A: {{appendix_title}}
{{appendix_content}}

### Appendix B: {{appendix_title}}
{{appendix_content}}
</template>

**EXAMPLE:** See proposal examples in the local repository: `~/.agent3d/docs/proposals/`

**PROPOSAL LIFECYCLE:**
1. **Draft**: Initial proposal creation using this template
2. **Under Review**: Proposal is being evaluated by stakeholders
3. **Approved**: Proposal has been approved for implementation
4. **Rejected**: Proposal has been rejected with documented reasons
5. **Implemented**: Proposal has been implemented and integrated into main documentation

**INTEGRATION WORKFLOW:**
- **Approved Proposals**: Move detailed design content to `docs/designs/` using DETAILED-DESIGN template with {COMPONENT}.md naming
- **Architecture Changes**: Update `docs/HIGH-LEVEL-DESIGN.md` with new components and relationships
- **Feature Implementation**: Update `docs/FEATURES.md` with new features and acceptance criteria
- **Archive Proposals**: Move implemented proposals to `docs/proposals/archive/` for historical reference

**VALIDATION CHECKLIST:**
- [ ] Problem statement clearly defines the issue being solved
- [ ] Motivation explains why this solution is needed now
- [ ] Proposed solution includes detailed architecture and design
- [ ] Implementation plan has realistic timeline and milestones
- [ ] Risk assessment covers major potential issues with mitigation strategies
- [ ] Success criteria are specific and measurable
- [ ] Integration plan addresses existing system compatibility
- [ ] Resource requirements are realistic and justified
- [ ] Alternative approaches have been considered and documented
- [ ] Decision points are clearly identified with recommendations
- [ ] Status and metadata are properly maintained
