# Architecture

**FORMAT SPECIFICATION:** This document must provide a comprehensive technical overview of the system architecture. It must include:
- System overview with high-level description
- Core components and their responsibilities
- Data flow diagrams (using Mermaid syntax)
- Component interaction patterns
- Directory/file structure
- Technical decisions and rationale
- Integration points and dependencies

**REQUIRED SECTIONS:**
1. System Overview - High-level description
2. Core Components - Main system parts and responsibilities
3. Data Flow - How information moves through the system
4. Component Interactions - How parts work together
5. Directory Structure - File organization
6. Technical Decisions - Key architectural choices
7. Dependencies - External systems and libraries

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Architecture

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
</template>

**EXAMPLE:** See the actual ARCHITECTURE.md file in this project: [docs/ARCHITECTURE.md]({{DDD_REMOTE_BASE}}/docs/ARCHITECTURE.md)

**VALIDATION CHECKLIST:**
- [ ] System overview clearly explains the architecture approach
- [ ] All major components are documented with their responsibilities
- [ ] Data flow diagrams accurately represent information movement
- [ ] Directory structure matches the actual project organization
- [ ] Technical decisions include rationale and trade-offs
- [ ] All external dependencies are documented
- [ ] Diagrams use proper Mermaid syntax and render correctly
