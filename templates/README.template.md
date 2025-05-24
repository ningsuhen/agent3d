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
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)

## Contributing
{{contributing_instructions}}

## License
{{license_info}}
</template>

**EXAMPLE:** (Do NOT include `<example>` tags in actual documentation)
<example>
# Agent3D - Documentation-Driven Development Guidelines for LLM Coding Agents

## Overview
Agent3D is a documentation-only framework that defines Documentation-Driven Development (DDD) principles specifically for Large Language Model (LLM) coding agents. It provides a structured approach to ensure documentation remains the single source of truth throughout the development process.

## Key Features
- **Remote Guideline Reference** - Designed to be referenced by LLM agents during coding tasks
- **Structured Development Process** - Clear, numbered passes from foundation to maintenance
- **Documentation as Source of Truth** - Ensures code never outpaces documentation

## Installation
This is a documentation-only project. No installation required.
```bash
# Reference the guidelines remotely
curl https://raw.githubusercontent.com/ningsuhen/agent3d/main/AGENT-GUIDELINES.md
```

## Quick Start
Implement the Agent Guideline Protocol to reference these guidelines remotely.
```markdown
**Agent Guideline Protocol**
1. Retrieve guidelines from remote URL
2. Cache locally as .agent-guidelines.md
3. Follow DDD passes in sequence
```

## Documentation
- [Agent Guidelines](AGENT-GUIDELINES.md)
- [DDD Passes](passes/simplified/)
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)

## Contributing
Contributions to improve the documentation are welcome! Please submit a Pull Request.

## License
MIT License
</example>

**VALIDATION CHECKLIST:**
- [ ] Project name and description are clear and accurate
- [ ] Overview explains the project's purpose and target audience
- [ ] Installation instructions are complete and tested
- [ ] Usage examples are functional and helpful
- [ ] All documentation links are valid
- [ ] Contributing guidelines are clear
- [ ] License information is accurate
