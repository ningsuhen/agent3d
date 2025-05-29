# Features Template

**NEW STRUCTURE:** As of 2025-01-27, Agent3D uses merged FT-TC structure in `docs/features/` directory.

**USAGE:**
- **Individual features:** Use this template for adding features to existing section files
- **New modules:** Use `FEATURE-module.template.md` for creating new section files

**FORMAT:** Merged FT-TC structure with features and test cases together
**CRITICAL:** Follow completion criteria from [Common Procedures](../docs/COMMON-PROCEDURES.md#merged-ft-tc-structure-new).

<template>
## {{ft_id}} - {{feature_name}}
- **Description:** {{brief_description}}
- **Criteria:** {{acceptance_criteria}}
- **Dependencies:** {{related_features_or_requirements}}
- **Impact:** {{high_medium_low}} - {{impact_description}}
- **Test Coverage:** {{test_count}} test cases, {{subtest_count}} sub-tests
- **Related Features:** [{{related_ft_id}}]({{section_file}}#{{anchor}}) ({{relationship_description}})
- **Test Cases:**
    - [{{status}}] **{{tc_id}}** - {{test_name}} ({{test_type}}, {{priority}}) {{production_status}}
        - [{{status}}] **{{tc_sub_id}}** - {{sub_test_name}} - {{detailed_test_description}}
        - [{{status}}] **{{tc_sub_id}}** - {{sub_test_name}} - {{detailed_test_description}}
    - [{{status}}] **{{tc_id}}** - {{test_name}} ({{test_type}}, {{priority}}) {{production_status}}
</template>

**EXAMPLE VALUES:**
- `{{ft_id}}`: FT-CORE-001, FT-IMPL-005, FT-LANG-002
- `{{tc_id}}`: TC-CORE-001, TC-IMPL-005, TC-LANG-002
- `{{tc_sub_id}}`: TC-CORE-001a, TC-IMPL-005b, TC-LANG-002c
- `{{status}}`: [x] (completed), [~] (in progress), [ ] (not started)
- `{{test_type}}`: Automated, Manual, Integration
- `{{priority}}`: High, Medium, Low
- `{{production_status}}`: ✅ **PRODUCTION**, 🚧 **DEVELOPMENT**, 📋 **PLANNED**

**VALIDATION:** See [Base Template System](BASE.template.md#universal-validation-rules) + [Documentation Templates](BASE.template.md#documentation-templates-features-requirements-tasks-etc)
