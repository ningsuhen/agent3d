# Features

**FORMAT SPECIFICATION:** This document must list all project features organized by logical modules. Each feature must be on a SINGLE LINE and include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Feature name: Clear, concise description
- Brief explanation: One-line description of what the feature does
- Acceptance criteria: Specific, measurable criteria in format (Criteria: <criteria description>)

**CRITICAL:** Features must NEVER span multiple lines. All information must fit on one line.

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
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})

## {{additional_module_name}}
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
</template>

**EXAMPLE:** See the actual FEATURES.md file in this project: [docs/FEATURES.md]({{DDD_REMOTE_BASE}}/docs/FEATURES.md)

**VALIDATION CHECKLIST:**
- [ ] All features are on a SINGLE LINE (no multi-line entries)
- [ ] All features follow the exact format: - {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- [ ] Each feature includes acceptance criteria in (Criteria: <>) format
- [ ] Acceptance criteria are specific and measurable
- [ ] Features are grouped logically by module/category
- [ ] Status indicators are accurate and up-to-date
- [ ] No duplicate features across sections
