# Features

**FORMAT SPECIFICATION:** Single-line features with status `[x]`/`[ ]`/`[~]`, description, and (Criteria: <>) format. Use `## Groups`/`### Sub-Groups` structure.

**🚨 CRITICAL - Feature Completion Criteria:**
- **NEVER mark features as `[x]` completed** based solely on interface definitions, prototypes, or documentation
- **ONLY mark features as `[x]` completed** when there is verifiable evidence the feature works properly:
  - Automated tests that pass and validate the feature functionality
  - Manual testing results that confirm the feature meets acceptance criteria
  - Demonstrable working implementation that fulfills the specified criteria
- **Use `[~]` for in-progress features** that have partial implementation but lack verification

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
- [ ] All features and sub-features are on a SINGLE LINE (no multi-line entries)
- [ ] All features follow format: `- [status] feature_name - description (Criteria: <criteria>)`
- [ ] Each feature includes acceptance criteria in (Criteria: <>) format
- [ ] **CRITICAL**: Uses `## Groups (Modules)` and `### Sub-Groups (Sub-modules)` heading structure
- [ ] **CRITICAL**: Features marked `[x]` have verifiable evidence of working implementation
- [ ] **CRITICAL**: No features marked `[x]` based solely on interface definitions or prototypes
- [ ] Sub-features use 2-space indentation and are logically related to parent feature
