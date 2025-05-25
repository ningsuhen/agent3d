# Features

**FORMAT SPECIFICATION:** Single-line features with status `[x]`/`[ ]`/`[~]`, description, and (Criteria: <>) format. Use `## Groups`/`### Sub-Groups` structure.

**🚨 CRITICAL:** Follow feature completion criteria from [Common Procedures](../docs/COMMON-PROCEDURES.md#feature-completion-criteria).

**SUB-FEATURES:** Use indented bullets (2 spaces) for sub-components. Both features and sub-features must NEVER span multiple lines.

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Features

## Important Note
{{project_special_note}}

## {{module_name}} (e.g., Authentication & Security)

### {{sub_module_name}} (e.g., User Authentication)
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})

### {{sub_module_name}} (e.g., Security & Permissions)
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})

## {{module_name}} (e.g., User Interface Components)

### {{sub_module_name}} (e.g., Forms & Input)
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})

### {{sub_module_name}} (e.g., Navigation & Layout)
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})

## {{module_name}} (e.g., Data Management)

### {{sub_module_name}} (e.g., Data Storage)
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
</template>

**EXAMPLE:** See the actual FEATURES.md file in the local repository: `~/.agent3d/docs/FEATURES.md`

**VALIDATION CHECKLIST:**
- [ ] All universal validation rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist) are met
- [ ] All features follow format: `- [status] feature_name - description (Criteria: <criteria>)`
- [ ] Each feature includes acceptance criteria in (Criteria: <>) format
- [ ] Sub-features are logically related to parent feature
