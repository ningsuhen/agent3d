# Drift Tracker

**FORMAT SPECIFICATION:** This document tracks drift between documentation and actual project state, focusing on areas not covered by DDD-STATUS. It monitors gaps, inconsistencies, and quality issues across any project type.

**REQUIRED SECTIONS:**
1. Drift Summary
2. Documentation Drift
3. Implementation Drift
4. Critical Issues
5. Recommended Actions

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# {{project_name}} - Drift Tracker

## 📊 Drift Summary

**Overall Drift Status:** {{overall_status_icon}} {{overall_status}}
- **Last Assessment:** {{assessment_date}}
- **Critical Drift:** {{critical_count}} 🚨
- **Drift Score:** {{drift_score}}/100

### Drift Overview
| Area | Status | Drift Level | Issues | Priority |
|------|--------|-------------|--------|----------|
| Documentation | {{doc_status_icon}} | {{doc_drift}} | {{doc_issues}} | {{doc_priority}} |
| Implementation | {{impl_status_icon}} | {{impl_drift}} | {{impl_issues}} | {{impl_priority}} |
| Quality | {{quality_status_icon}} | {{quality_drift}} | {{quality_issues}} | {{quality_priority}} |

**Drift Status:**
- 🟢 **Low** (0-25 drift, well-aligned)
- 🟡 **Medium** (26-50 drift, some issues)
- 🟠 **High** (51-75 drift, significant issues)
- 🔴 **Critical** (76-100 drift, major problems)

---

## 📝 Documentation Drift

### Current Status: {{doc_status_icon}} {{doc_status}}
- **Drift Score:** {{doc_drift_score}}/100
- **Last Updated:** {{doc_last_update}}

### Documentation Issues
| Component | Status | Issue | Impact | Priority |
|-----------|--------|-------|--------|----------|
| {{doc_component_1}} | {{doc_comp1_status}} | {{doc_comp1_issue}} | {{doc_comp1_impact}} | {{doc_comp1_priority}} |
| {{doc_component_2}} | {{doc_comp2_status}} | {{doc_comp2_issue}} | {{doc_comp2_impact}} | {{doc_comp2_priority}} |
| {{doc_component_3}} | {{doc_comp3_status}} | {{doc_comp3_issue}} | {{doc_comp3_impact}} | {{doc_comp3_priority}} |

### Common Documentation Drift
- [ ] **Outdated Information**: {{outdated_count}} sections need updates
- [ ] **Missing Documentation**: {{missing_count}} components lack docs
- [ ] **Broken References**: {{broken_count}} links or references broken
- [ ] **Format Inconsistencies**: {{format_count}} files need standardization

---

## 🔧 Implementation Drift

### Current Status: {{impl_status_icon}} {{impl_status}}
- **Drift Score:** {{impl_drift_score}}/100
- **Last Updated:** {{impl_last_update}}

### Implementation Issues
| Component | Status | Issue | Impact | Priority |
|-----------|--------|-------|--------|----------|
| {{impl_component_1}} | {{impl_comp1_status}} | {{impl_comp1_issue}} | {{impl_comp1_impact}} | {{impl_comp1_priority}} |
| {{impl_component_2}} | {{impl_comp2_status}} | {{impl_comp2_issue}} | {{impl_comp2_impact}} | {{impl_comp2_priority}} |
| {{impl_component_3}} | {{impl_comp3_status}} | {{impl_comp3_issue}} | {{impl_comp3_impact}} | {{impl_comp3_priority}} |

### Common Implementation Drift
- [ ] **Undocumented Changes**: {{undoc_changes}} changes without documentation
- [ ] **Feature Creep**: {{feature_creep}} unplanned features added
- [ ] **Technical Debt**: {{tech_debt}} areas need refactoring
- [ ] **Configuration Drift**: {{config_drift}} settings not documented

---

## 🚨 Critical Issues

### High Priority Drift
{{#critical_issues}}
- **{{issue_type}}** 🚨 {{issue_severity}}
  - **Component:** {{issue_component}}
  - **Description:** {{issue_description}}
  - **Impact:** {{issue_impact}}
  - **Action Required:** {{issue_action}}
  - **Deadline:** {{issue_deadline}}
{{/critical_issues}}

### Escalation Triggers
- [ ] **Major Feature Undocumented**: Core functionality lacks documentation
- [ ] **Breaking Changes**: Undocumented changes affecting users
- [ ] **Quality Degradation**: Significant quality issues detected
- [ ] **Compliance Issues**: Regulatory or policy violations

---

## 🎯 Recommended Actions

### Immediate Actions (Next 24-48 hours)
{{#immediate_actions}}
- [ ] **{{action_type}}**: {{action_description}} (Priority: {{action_priority}})
{{/immediate_actions}}

### Short-term Actions (Next 1-2 weeks)
{{#short_term_actions}}
- [ ] **{{action_type}}**: {{action_description}} (Priority: {{action_priority}})
{{/short_term_actions}}

### Long-term Actions (Next month)
{{#long_term_actions}}
- [ ] **{{action_type}}**: {{action_description}} (Priority: {{action_priority}})
{{/long_term_actions}}

### Prevention Strategies
- [ ] **Regular Reviews**: Schedule weekly drift assessments
- [ ] **Documentation Gates**: Require docs for all changes
- [ ] **Automated Monitoring**: Set up drift detection tools
- [ ] **Quality Checks**: Implement quality gates in workflow

---

## 📈 Drift Trends

### Historical Drift Levels
- **Current Period:** {{current_drift}} ({{drift_trend_icon}} {{drift_trend}})
- **Previous Period:** {{previous_drift}}
- **Best Performance:** {{best_drift}} ({{best_drift_date}})
- **Worst Performance:** {{worst_drift}} ({{worst_drift_date}})

### Drift Patterns
- **Most Common Drift:** {{common_drift_type}}
- **Average Resolution Time:** {{avg_resolution_time}}
- **Recurring Issues:** {{recurring_count}}

**Trend Icons:**
- ⬇️ **Improving** - Drift decreasing
- ➡️ **Stable** - Drift maintained
- ⬆️ **Worsening** - Drift increasing

---

*Last updated: {{last_update_date}} | Next assessment: {{next_assessment_date}}*
</template>

**EXAMPLE:** See drift tracking examples in project documentation

**VALIDATION CHECKLIST:**
- [ ] All drift areas are tracked with specific metrics
- [ ] Status icons provide clear visual indicators
- [ ] Critical issues are properly prioritized and actionable
- [ ] Recommended actions have clear timelines and priorities
- [ ] Drift trends show historical context
- [ ] Prevention strategies are included
- [ ] Template is generic enough for any project type
- [ ] No overlap with DDD-STATUS pass tracking
