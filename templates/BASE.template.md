# Base Template

**FORMAT:** Common structure for Agent3D documentation templates.

**SECTIONS:** Header, Overview, Content, Validation

**VARIABLES:** {{document_title}}, {{document_purpose}}, {{project_name}}, {{author}}, {{creation_date}}, {{last_updated}}, {{version}}

**VALIDATION:** All templates inherit base requirements from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist)

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# {{document_title}}

**DOCUMENT METADATA:**
- **Purpose**: {{document_purpose}}
- **Author**: {{author}}
- **Created**: {{creation_date}}
- **Last Updated**: {{last_updated}}
- **Version**: {{version}}

## Overview

{{overview_content}}

## {{content_section_title}}

{{main_content}}

## Validation Checklist

**Validation:**
- [ ] Universal rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist)
- [ ] Descriptive title and complete sections
- [ ] Clear, concise content

**Template-Specific:** {{additional_validation_rules}}
</template>

**EXAMPLE:** See specialized templates that extend this base in the local repository: `~/.agent3d/templates/`

**VALIDATION:** Template metadata complete, base sections defined, inheritance clear, variables documented, rules enforceable
