# Agent3D Templates System

This directory contains the standardized templates for the Agent3D Documentation-Driven Development framework.

## 📁 Directory Structure

```
templates/
├── index.yml                           # Template system index and configuration
├── agent3d-config.template.yml         # Main project configuration template
├── README.md                           # This file
└── [future templates]                  # Additional templates as needed
```

## 🎯 Purpose

The templates.yml directory provides:

1. **Standardized Configuration Templates**: Consistent project setup across all Agent3D projects
2. **Migration Support**: Tools and templates for upgrading existing configurations
3. **Placeholder System**: Structured approach to customizing templates for specific projects
4. **Version Management**: Template versioning and compatibility tracking

## 📋 Available Templates

### Configuration Templates

#### `agent3d-config.template.yml`
- **Purpose**: Main Agent3D project configuration
- **Target File**: `.agent3d-config.yml`
- **Version**: 2.0
- **Usage**: Foundation Pass configuration setup
- **Features**:
  - Comprehensive project configuration
  - Python path resolution support
  - Custom settings accommodation
  - Pass-specific configurations
  - Migration compatibility

## Key Differences from Markdown Templates

### YAML Templates (this directory)
- **Target**: LLM agents and automation tools
- **Format**: Structured YAML with hierarchical data
- **Processing**: Machine-readable, API-friendly
- **Validation**: Schema-based validation possible
- **Usage**: Automated tracking, status updates, planning

### Markdown Templates (`../templates/`)
- **Target**: Human developers and documentation
- **Format**: Human-readable Markdown with placeholders
- **Processing**: Manual editing and reading
- **Validation**: Visual inspection and guidelines
- **Usage**: Creating documentation, user-facing content

## Usage Guidelines

### For LLM Agents
1. Use YAML templates for automated tracking and status updates
2. Process structured data programmatically
3. Validate against schema definitions
4. Generate reports and analytics from structured data

### For Human Developers
1. Use Markdown templates in `../templates/` for documentation
2. Create user-facing content with Markdown templates
3. Use YAML templates only when integrating with automation tools

## Template Selection Guide

| Use Case | Template Type | Directory |
|----------|---------------|-----------|
| Status tracking | YAML | `templates/` |
| Execution planning | YAML | `templates/` |
| Framework migrations | YAML | `templates/` |
| Feature documentation | Markdown | `../templates/` |
| Requirements documentation | Markdown | `../templates/` |
| User stories | Markdown | `../templates/` |
| Design documents | Markdown | `../templates/` |
| Project README | Markdown | `../templates/` |

## Integration with DDD Framework

These YAML templates integrate with:
- **Drift Scanner**: Automated analysis and reporting
- **Migration Manager**: Framework update tracking
- **Status Monitoring**: Real-time project health tracking
- **MCP Servers**: AI client integration
- **CI/CD Pipelines**: Automated validation and reporting

## Best Practices

1. **Consistency**: Always use YAML templates for machine processing
2. **Validation**: Validate YAML syntax before committing
3. **Documentation**: Keep both YAML and Markdown versions when needed
4. **Automation**: Leverage structured data for automated workflows
5. **Human Review**: Use Markdown templates for human-readable documentation

---

*This separation ensures optimal formats for both machine processing and human consumption in the DDD framework.*
