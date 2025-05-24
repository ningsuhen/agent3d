# Features

**FORMAT SPECIFICATION:** This document must list all project features organized by logical modules. Each feature must be on a SINGLE LINE and include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Feature name: Clear, concise description
- Brief explanation: One-line description of what the feature does
- Acceptance criteria: Specific, measurable criteria in format (Criteria: <criteria description>)

**🚨 CRITICAL - Feature Completion Criteria:**
- **NEVER mark features as `[x]` completed** based solely on interface definitions, prototypes, or documentation
- **ONLY mark features as `[x]` completed** when there is verifiable evidence the feature works properly:
  - Automated tests that pass and validate the feature functionality
  - Manual testing results that confirm the feature meets acceptance criteria
  - Demonstrable working implementation that fulfills the specified criteria
- **Use `[~]` for in-progress features** that have partial implementation but lack verification

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

**🔗 CRITICAL - Documentation Structure:**
- **ALWAYS use `## Groups (Modules)` for main functional areas**
- **ALWAYS use `### Sub-Groups (Sub-modules)` for specific aspects within each module**

**GROUPING STRATEGY:** Organize features using a two-level hierarchy to make them easy to spot and manage:
- **## Groups (Modules):** Main functional areas or components
- **### Sub-Groups (Sub-modules):** Specific aspects within each module
- **By Component:** Group related features that belong to the same system component
- **By User Journey:** Group features that support the same user workflow or use case
- **By Technical Layer:** Group features by architectural layer (UI, API, Database, etc.)
- **By Priority/Phase:** Group features by development priority or release phase

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
- [ ] All features follow the exact format: - {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- [ ] All sub-features use 2-space indentation and follow the same format
- [ ] Each feature and sub-feature includes acceptance criteria in (Criteria: <>) format
- [ ] Acceptance criteria are specific and measurable
- [ ] **CRITICAL**: Uses `## Groups (Modules)` and `### Sub-Groups (Sub-modules)` heading structure
- [ ] Features are grouped logically by module/category with clear section headers
- [ ] Section names clearly indicate the functional area or component
- [ ] Sub-features are logically related to their parent feature
- [ ] **CRITICAL**: Features marked `[x]` have verifiable evidence of working implementation (tests or manual verification)
- [ ] **CRITICAL**: Features marked `[~]` are used for partial implementations without verification
- [ ] **CRITICAL**: No features marked `[x]` based solely on interface definitions or prototypes
- [ ] Status indicators are accurate and up-to-date
- [ ] No duplicate features across sections
- [ ] Related features are grouped together for easy identification
- [ ] Each section has 3-10 features for optimal readability
