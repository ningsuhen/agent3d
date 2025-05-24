# Base Template

**TEMPLATE METADATA:**
```yaml
template:
  id: "base-documentation"
  version: "1.0"
  type: "base"
  description: "Base template for all Agent3D documentation"
  author: "Agent3D Team"
  created: "2024-01-17"
  updated: "2024-01-17"
```

**FORMAT SPECIFICATION:** This is the base template that provides common structure and validation rules for all Agent3D documentation templates. It defines:
- Standard document structure with header, overview, content, and validation sections
- Common variables and placeholders used across templates
- Base validation rules that all templates must follow
- Inheritance patterns for specialized templates

**REQUIRED SECTIONS:**
1. Header - Document title and metadata
2. Overview - Purpose and scope description
3. Content - Main document content (varies by template type)
4. Validation - Quality checks and compliance verification

**COMMON VARIABLES:**
- `{{document_title}}` - The title of the document
- `{{document_purpose}}` - Brief description of document purpose
- `{{project_name}}` - Name of the project
- `{{author}}` - Document author
- `{{creation_date}}` - Document creation date
- `{{last_updated}}` - Last modification date
- `{{version}}` - Document version

**BASE VALIDATION RULES:**
- All required sections must be present
- All variables must be replaced with actual values
- No `<template>` or `<example>` tags in final documentation
- Document must follow CAPS naming convention for files
- Links must be functional and point to existing resources

**TEMPLATE INHERITANCE:**
Templates can extend this base template by:
1. Specifying `extends: "base-documentation"` in metadata
2. Adding specialized sections to the base structure
3. Defining additional variables specific to the template type
4. Adding custom validation rules beyond the base requirements

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

**CONTEXT-AWARE FEATURES:**
- **Project Type Detection**: Automatically suggests appropriate specialized templates
- **Language Integration**: Includes language-specific sections when relevant
- **Framework Awareness**: Adapts content based on detected frameworks
- **Validation Intelligence**: Applies context-specific validation rules

**INHERITANCE EXAMPLES:**

### README Template Inheritance
```yaml
template:
  id: "readme-template"
  extends: "base-documentation"
  specialized_sections:
    - installation
    - usage
    - examples
    - contributing
  additional_variables:
    - installation_command
    - usage_example
```

### FEATURES Template Inheritance
```yaml
template:
  id: "features-template"
  extends: "base-documentation"
  specialized_sections:
    - feature_groups
    - acceptance_criteria
    - status_tracking
  additional_variables:
    - feature_categories
    - completion_status
```

**DYNAMIC CONTENT GENERATION:**
- **Smart Placeholders**: Variables that adapt based on project context
- **Conditional Sections**: Sections that appear only when relevant
- **Auto-Population**: Common fields filled automatically when possible
- **Suggestion Engine**: Provides content suggestions based on project analysis

**QUALITY ASSURANCE:**
- **Automated Validation**: Real-time checking during template generation
- **Consistency Checks**: Ensures consistency across related documents
- **Best Practice Enforcement**: Applies Agent3D documentation standards
- **Error Prevention**: Catches common mistakes before document creation

**INTEGRATION POINTS:**
- **DDD Pass System**: Templates integrate with pass execution workflow
- **Version Control**: Template changes tracked and versioned
- **Agent Workflow**: Seamless integration with agent development process
- **Validation Framework**: Comprehensive quality checking system

**USAGE GUIDELINES:**
1. **Template Selection**: Use context analyzer to recommend appropriate templates
2. **Customization**: Modify templates based on project-specific requirements
3. **Validation**: Always run validation checks before finalizing documents
4. **Inheritance**: Leverage template inheritance to reduce duplication
5. **Evolution**: Update templates based on usage patterns and feedback

**EXAMPLE:** See specialized templates that extend this base in the local repository: `~/.agent3d/templates/`

**VALIDATION CHECKLIST:**
- [ ] Template metadata is complete and accurate
- [ ] All base sections are properly defined
- [ ] Inheritance structure is clear and functional
- [ ] Variables are well-documented and consistently named
- [ ] Validation rules are comprehensive and enforceable
- [ ] Integration points are clearly specified
- [ ] Usage guidelines are clear and actionable
- [ ] Examples demonstrate proper template usage
