# Base Template

**FORMAT SPECIFICATION:** Common structure for Agent3D documentation templates.

**REQUIRED SECTIONS:** Header, Overview, Content, Validation

**COMMON VARIABLES:** {{document_title}}, {{document_purpose}}, {{project_name}}, {{author}}, {{creation_date}}, {{last_updated}}, {{version}}

**UNIVERSAL VALIDATION RULES:**
All templates inherit these base requirements from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist):
- Follow `## Groups` and `### Sub-Groups` heading structure
- Replace all {{placeholders}} with actual content
- Remove all `<template>` and `<example>` tags
- Ensure all links are functional and point to existing resources
- Use single-line entries for features, tasks, and test cases
- Mark `[x]` completed ONLY with verifiable evidence
- Use 2-space indentation for sub-items
- Maintain clear, concise, LLM-friendly language

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
- [ ] All universal validation rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist) are met
- [ ] Document title is descriptive and follows naming conventions
- [ ] All required sections are present and complete
- [ ] Content is clear, concise, and serves the document purpose

**Template-Specific Requirements:**
{{additional_validation_rules}}
</template>

**EXAMPLE:** See specialized templates that extend this base in the local repository: `~/.agent3d/templates/`

**VALIDATION:** Template metadata complete, base sections defined, inheritance clear, variables documented, rules enforceable
