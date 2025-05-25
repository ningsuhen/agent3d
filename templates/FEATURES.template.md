# Features

**FORMAT:** `- [status] feature_name - description (Criteria: <criteria>)`

**CRITICAL:** Follow completion criteria from [Common Procedures](../docs/COMMON-PROCEDURES.md#feature-completion-criteria).

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

**VALIDATION:**
- [ ] Universal rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist)
- [ ] Format: `- [status] feature_name - description (Criteria: <criteria>)`
- [ ] Acceptance criteria included for all features
