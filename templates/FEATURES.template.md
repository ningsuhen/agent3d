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

**GROUPING STRATEGY:** Organize features using a two-level hierarchy to make them easy to spot and manage:
- **## Groups (Modules):** Main functional areas or components
- **### Sub-Groups (Sub-modules):** Specific aspects within each module
- **By Component:** Group related features that belong to the same system component
- **By User Journey:** Group features that support the same user workflow or use case
- **By Technical Layer:** Group features by architectural layer (UI, API, Database, etc.)
- **By Priority/Phase:** Group features by development priority or release phase

**EXAMPLES OF GOOD GROUPING:**
- **## Authentication & Security** → ### User Authentication, ### Security & Permissions
- **## User Interface Components** → ### Forms & Input, ### Navigation & Layout
- **## Data Management** → ### Data Storage, ### Data Processing
- **## Integration & APIs** → ### External APIs, ### Internal Services
- **## Monitoring & Analytics** → ### Performance Monitoring, ### User Analytics

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

**EXAMPLE:** See the actual FEATURES.md file in this project: [docs/FEATURES.md]({{DDD_REMOTE_BASE}}/docs/FEATURES.md)

**VALIDATION CHECKLIST:**
- [ ] All features and sub-features are on a SINGLE LINE (no multi-line entries)
- [ ] All features follow the exact format: - {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- [ ] All sub-features use 2-space indentation and follow the same format
- [ ] Each feature and sub-feature includes acceptance criteria in (Criteria: <>) format
- [ ] Acceptance criteria are specific and measurable
- [ ] Features are grouped logically by module/category with clear section headers
- [ ] Section names clearly indicate the functional area or component
- [ ] Sub-features are logically related to their parent feature
- [ ] Status indicators are accurate and up-to-date
- [ ] No duplicate features across sections
- [ ] Related features are grouped together for easy identification
- [ ] Each section has 3-10 features for optimal readability
