# {{component_name}} - Design

**FORMAT SPECIFICATION:** This document must provide comprehensive design specifications for a specific component or system part. It must include:
- Component overview and purpose
- Component architecture with detailed specifications
- API specifications and interfaces
- Data flow diagrams and sequence diagrams
- Error handling and recovery strategies
- Configuration and customization options
- Performance requirements and constraints
- Security considerations
- Testing strategy and validation
- Integration points with other components
- Monitoring and logging specifications
- Future enhancements and scalability considerations

**REQUIRED SECTIONS:**
1. Overview - Component purpose and scope
2. Component Architecture - Detailed component breakdown
3. API Specifications - Interfaces, methods, and data structures
4. Data Flow - Detailed data movement and processing
5. Error Handling - Error scenarios and recovery mechanisms
6. Configuration - Settings, parameters, and customization
7. Performance Requirements - Response times, throughput, resource usage
8. Security Considerations - Security measures and validation
9. Testing Strategy - Unit, integration, and performance testing
10. Integration Points - Connections with other components/systems
11. Monitoring and Logging - Observability and diagnostics
12. Future Enhancements - Planned features and scalability

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# {{component_name}} - Design

## Overview

This document provides the design specifications for the {{component_name}}, which {{component_purpose}}.

## Component Architecture

### Core Components

#### 1. {{component_name}}
- **Purpose**: {{component_purpose}}
- **Interface**: {{component_interface}}
- **Responsibilities**: {{component_responsibilities}}

#### 2. {{component_name}}
- **Purpose**: {{component_purpose}}
- **Interface**: {{component_interface}}
- **Responsibilities**: {{component_responsibilities}}

### Component Relationships

```mermaid
{{component_diagram}}
```

## API Specifications

### {{api_name}} API

```{{language}}
{{api_specification}}
```

### Data Structures

```{{language}}
{{data_structures}}
```

## Data Flow

### {{flow_name}} Flow

```mermaid
{{data_flow_diagram}}
```

{{data_flow_description}}

## Error Handling

### Error Categories

1. **{{error_category}}**
   - {{error_description}}
   - **Recovery Strategy**: {{recovery_strategy}}

2. **{{error_category}}**
   - {{error_description}}
   - **Recovery Strategy**: {{recovery_strategy}}

### Error Recovery Mechanisms

- **{{mechanism_name}}**: {{mechanism_description}}
- **{{mechanism_name}}**: {{mechanism_description}}

## Configuration

### Default Settings
- **{{setting_name}}**: {{setting_value}} - {{setting_description}}
- **{{setting_name}}**: {{setting_value}} - {{setting_description}}

### Environment Variables
- `{{ENV_VAR_NAME}}`: {{env_var_description}}
- `{{ENV_VAR_NAME}}`: {{env_var_description}}

### Configuration Schema

```{{format}}
{{configuration_schema}}
```

## Performance Requirements

### Response Times
- {{operation_name}}: < {{time_limit}}
- {{operation_name}}: < {{time_limit}}

### Resource Usage
- Memory: < {{memory_limit}}
- CPU: < {{cpu_limit}}
- Network: {{network_requirements}}

### Throughput
- {{metric_name}}: {{throughput_requirement}}
- {{metric_name}}: {{throughput_requirement}}

## Security Considerations

### {{security_aspect}}
- {{security_requirement}}
- {{security_implementation}}

### {{security_aspect}}
- {{security_requirement}}
- {{security_implementation}}

## Testing Strategy

### Unit Tests
- {{test_category}}: {{test_description}}
- {{test_category}}: {{test_description}}

### Integration Tests
- {{integration_scenario}}: {{test_description}}
- {{integration_scenario}}: {{test_description}}

### Performance Tests
- {{performance_scenario}}: {{test_description}}
- {{performance_scenario}}: {{test_description}}

## Integration Points

### External Dependencies
- **{{dependency_name}}**: {{dependency_description}}
- **{{dependency_name}}**: {{dependency_description}}

### Internal Module Connections
- **{{module_name}}**: {{connection_description}}
- **{{module_name}}**: {{connection_description}}

## Monitoring and Logging

### Log Levels
- **{{log_level}}**: {{log_description}}
- **{{log_level}}**: {{log_description}}

### Metrics
- {{metric_name}}: {{metric_description}}
- {{metric_name}}: {{metric_description}}

### Health Checks
- {{health_check_name}}: {{health_check_description}}
- {{health_check_name}}: {{health_check_description}}

## Future Enhancements

### Planned Features
- {{feature_name}}: {{feature_description}}
- {{feature_name}}: {{feature_description}}

### Scalability Considerations
- {{scalability_aspect}}: {{scalability_plan}}
- {{scalability_aspect}}: {{scalability_plan}}

### Technical Debt
- {{debt_item}}: {{debt_description}}
- {{debt_item}}: {{debt_description}}
</template>

**EXAMPLE:** See the actual component design files in the local repository: `~/.agent3d/docs/designs/`

**MIGRATION CHECKLIST (for existing projects):**
- [ ] Check if project has `ARCHITECTURE.md` that should be renamed to `HIGH-LEVEL-DESIGN.md`
- [ ] Search codebase for references to `ARCHITECTURE.md` and update to `HIGH-LEVEL-DESIGN.md`
- [ ] Update any documentation links pointing to architecture documentation
- [ ] Create `docs/designs/` directory if it doesn't exist (not `docs/modules/`)
- [ ] Move detailed component specifications from high-level design to component designs using {COMPONENT}.md naming
- [ ] Ensure all documentation files use CAPS naming convention
- [ ] Update build scripts, CI/CD configurations that reference architecture documentation
- [ ] Update README and other documentation that mentions architecture files
- [ ] Update any references from "modules" to "designs" for component documentation

**VALIDATION CHECKLIST:**
- [ ] Module overview clearly explains purpose and scope
- [ ] All major components are documented with detailed specifications
- [ ] API specifications include complete interface definitions
- [ ] Data flow diagrams accurately represent information movement
- [ ] Error handling covers all failure scenarios with recovery strategies
- [ ] Configuration options are comprehensive and well-documented
- [ ] Performance requirements are specific and measurable
- [ ] Security considerations address all relevant threats
- [ ] Testing strategy covers unit, integration, and performance testing
- [ ] Integration points with other modules are clearly defined
- [ ] Monitoring and logging provide adequate observability
- [ ] Future enhancements and scalability plans are realistic
- [ ] Diagrams use proper Mermaid syntax and render correctly
