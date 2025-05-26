# Base Template System

**PURPOSE:** Unified template structure and validation system for Agent3D documentation.

## Common Template Structure

**STANDARD SECTIONS:**
1. **Format Specification** - Document purpose and requirements
2. **Template Content** - Placeholder structure with {{variables}}
3. **Validation** - Universal + template-specific rules

**UNIVERSAL VARIABLES:**
- `{{document_title}}`, `{{document_purpose}}`, `{{project_name}}`
- `{{author}}`, `{{creation_date}}`, `{{last_updated}}`, `{{version}}`

## Universal Validation Rules

**ALL TEMPLATES MUST:**
- [ ] Follow [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist)
- [ ] Replace ALL {{placeholders}} with actual content
- [ ] Remove `<template>` and `<example>` tags
- [ ] Use `## Groups` / `### Sub-Groups` structure
- [ ] Include functional links and single-line entries
- [ ] Mark `[x]` only with verifiable evidence

## Template Usage Process

1. **Access**: Templates from `~/.agent3d/templates/`
2. **Replace**: All {{placeholders}} with actual content
3. **Remove**: Template tags before finalizing
4. **Validate**: Against universal + specific rules

**REFERENCE:** See [Common Procedures - Template System](../docs/COMMON-PROCEDURES.md#template-system) for complete usage instructions.
