# [Project Name] - [Brief Project Description]

**FORMAT SPECIFICATION:** This document must serve as the main entry point for the project. It must include:
- Clear project title and one-line description
- Project overview explaining what the project does
- Key features or benefits
- Installation/setup instructions (if applicable)
- Usage examples or getting started guide
- Links to additional documentation
- Contributing guidelines
- License information

**REQUIRED SECTIONS:**
1. Project title and description
2. Overview/What it does
3. Key features or benefits
4. Installation/Setup (if applicable)
5. Usage/Getting Started
6. Documentation links
7. Contributing
8. License

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# {{project_name}} - {{project_description}}

## Overview
{{project_overview}}

## Key Features
- **{{feature_name}}** - {{feature_description}}
- **{{feature_name}}** - {{feature_description}}
- **{{feature_name}}** - {{feature_description}}

## Installation
{{installation_instructions}}
```{{language}}
{{installation_commands}}
```

## Quick Start
{{usage_instructions}}
```{{language}}
{{code_example}}
```

## Documentation
- [{{doc_name}}]({{doc_link}})
- [{{doc_name}}]({{doc_link}})
- [High-Level Design](docs/HIGH-LEVEL-DESIGN.md)
- [Contributing](CONTRIBUTING.md)

## Contributing
{{contributing_instructions}}

## License
{{license_info}}
</template>

**EXAMPLE:** See the actual README.md file in the local repository: `~/.agent3d/README.md`

**CONTEXT-AWARE FEATURES:**
- **Language Detection**: Automatically includes language-specific installation commands
- **Framework Integration**: Adds framework-specific setup instructions when detected
- **Project Type Adaptation**: Adjusts sections based on project type (library, application, documentation)
- **Dependency Management**: Includes appropriate package manager commands

**DYNAMIC CONTENT GENERATION:**
- **Auto-Detection Variables**:
  - `{{detected_language}}` - Primary programming language
  - `{{package_manager}}` - Detected package manager (npm, pip, maven, etc.)
  - `{{framework_name}}` - Main framework if detected
  - `{{project_type}}` - Type of project (library, cli, web-app, etc.)

**INTELLIGENT SUGGESTIONS:**
- Installation commands based on detected package manager
- Usage examples appropriate for project type
- Documentation links relevant to detected technologies
- Contributing guidelines adapted to project structure

**VALIDATION CHECKLIST:**
- [ ] Project name and description are clear and accurate
- [ ] Overview explains the project's purpose and target audience
- [ ] Installation instructions are complete and tested
- [ ] Usage examples are functional and helpful
- [ ] All documentation links are valid
- [ ] Contributing guidelines are clear
- [ ] License information is accurate
- [ ] Context-aware content is relevant and accurate
- [ ] Auto-generated sections are properly customized
