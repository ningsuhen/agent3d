# Features

**FORMAT SPECIFICATION:** This document must list all project features organized by logical modules. Each feature must be on a SINGLE LINE and include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Feature name: Clear, concise description
- Brief explanation: One-line description of what the feature does
- Acceptance criteria: Specific, measurable criteria in format (Criteria: <criteria description>)

**SUB-FEATURES:** Features can have sub-features using indented bullets (2 spaces):
- Main feature with sub-components can be broken down
  - Sub-feature 1 - Specific component (Criteria: <sub-criteria>)
  - Sub-feature 2 - Another component (Criteria: <sub-criteria>)

**CRITICAL:** Both features and sub-features must NEVER span multiple lines. All information must fit on one line.

**REQUIRED SECTIONS:**
1. Important Note (if project has special characteristics)
2. Core Features (main functionality modules)
3. Additional feature categories as needed for your project
4. Each section must have 3-10 features listed

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Features

## Important Note
{{project_special_note}}

## Core {{module_name}}
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})

## {{additional_module_name}}
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
  - {{status}} {{sub_feature_name}} - {{sub_component_description}} (Criteria: {{sub_criteria}})
</template>

**EXAMPLE:** See the actual FEATURES.md file in this project: [docs/FEATURES.md]({{DDD_REMOTE_BASE}}/docs/FEATURES.md)

**VALIDATION CHECKLIST:**
- [ ] All features and sub-features are on a SINGLE LINE (no multi-line entries)
- [ ] All features follow the exact format: - {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- [ ] All sub-features use 2-space indentation and follow the same format
- [ ] Each feature and sub-feature includes acceptance criteria in (Criteria: <>) format
- [ ] Acceptance criteria are specific and measurable
- [ ] Features are grouped logically by module/category
- [ ] Sub-features are logically related to their parent feature
- [ ] Status indicators are accurate and up-to-date
- [ ] No duplicate features across sections
