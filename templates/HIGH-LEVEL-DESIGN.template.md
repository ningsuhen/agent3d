# High-Level Design

**FORMAT SPECIFICATION:** This document must provide a comprehensive technical overview of the system high-level architecture. It must include:
- System overview with high-level description
- Core components and their responsibilities
- Data flow diagrams (using Mermaid syntax)
- Component interaction patterns
- Directory/file structure
- Technical decisions and rationale
- Integration points and dependencies
- Links to module detailed designs

**REQUIRED SECTIONS:**
1. System Overview - High-level description
2. Core Components - Main system parts and responsibilities
3. Data Flow - How information moves through the system
4. Component Interactions - How parts work together
5. Directory Structure - File organization
6. Technical Decisions - Key architectural choices
7. Dependencies - External systems and libraries
8. Module Detailed Designs - Links to detailed component specifications

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# High-Level Design

## System Overview
{{system_description}}

```mermaid
{{high_level_diagram}}
```

## Core Components

### {{component_name}}
{{component_description}}

### {{component_name}}
{{component_description}}

## Data Flow
{{data_flow_description}}

```mermaid
{{data_flow_diagram}}
```

## Component Interactions
{{interaction_description}}

## Directory Structure
```
{{directory_structure}}
```

## Technical Decisions

### {{decision_name}}
**Rationale:** {{decision_rationale}}
**Alternatives Considered:** {{alternatives}}
**Trade-offs:** {{trade_offs}}

## Dependencies
- **{{dependency_name}}** - {{dependency_description}}
- **{{dependency_name}}** - {{dependency_description}}

## Module Detailed Designs

For detailed implementation specifications of individual components, refer to the module detailed design documents:

- **[{{module_name}}](modules/{{module_file}}.md)** - {{module_description}}
- **[{{module_name}}](modules/{{module_file}}.md)** - {{module_description}}

These detailed designs provide implementation details, API specifications, and technical constraints that complement this high-level architectural overview.
</template>

**EXAMPLE:** See the actual HIGH-LEVEL-DESIGN.md file in this project: [docs/HIGH-LEVEL-DESIGN.md]({{DDD_REMOTE_BASE}}/docs/HIGH-LEVEL-DESIGN.md)

**VALIDATION CHECKLIST:**
- [ ] System overview clearly explains the architecture approach
- [ ] All major components are documented with their responsibilities
- [ ] Data flow diagrams accurately represent information movement
- [ ] Directory structure matches the actual project organization
- [ ] Technical decisions include rationale and trade-offs
- [ ] All external dependencies are documented
- [ ] Diagrams use proper Mermaid syntax and render correctly
- [ ] Links to module detailed designs are provided and functional
