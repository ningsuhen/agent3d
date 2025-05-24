# Base Template

**FORMAT SPECIFICATION:** Common structure for Agent3D documentation templates.

**REQUIRED SECTIONS:** Header, Overview, Content, Validation

**COMMON VARIABLES:** {{document_title}}, {{document_purpose}}, {{project_name}}, {{author}}, {{creation_date}}, {{last_updated}}, {{version}}

**BASE VALIDATION RULES:**
- All required sections must be present
- All variables must be replaced with actual values
- No `<template>` or `<example>` tags in final documentation
- Document must follow CAPS naming convention for files
- Links must be functional and point to existing resources

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

**Base Requirements:**
- [ ] Document title is descriptive and follows naming conventions
- [ ] All required sections are present and complete
- [ ] All template variables have been replaced with actual values
- [ ] No template tags (`<template>`, `<example>`) remain in final document
- [ ] Document follows CAPS naming convention if it's a documentation file
- [ ] All links are functional and point to existing resources
- [ ] Content is clear, concise, and serves the document purpose

**Template-Specific Requirements:**
{{additional_validation_rules}}
</template>

**EXAMPLE:** See specialized templates that extend this base in the local repository: `~/.agent3d/templates/`

**VALIDATION:** Template metadata complete, base sections defined, inheritance clear, variables documented, rules enforceable
