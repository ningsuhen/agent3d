# YAML Templates for LLM Tracking

This directory contains YAML templates specifically designed for LLM processing and automated tracking. These templates are optimized for machine readability and structured data processing.

## Templates in this Directory

### `DDD-STATUS.template.yml`
**Purpose**: Structured status tracking for all DDD passes
**Usage**: LLM agents use this for automated status updates and health monitoring
**Features**:
- Hierarchical pass organization
- Structured metadata and statistics
- Machine-readable status indicators
- Automated validation criteria

### `EXEC-PLAN.template.yml`
**Purpose**: Execution plan templates for complex development tasks
**Usage**: LLM agents use this for planning and tracking multi-step implementations
**Features**:
- Checkpoint-based execution tracking
- Expert role assignments
- Structured validation criteria
- Progress monitoring with status icons

### `migration.template.yml`
**Purpose**: Framework migration templates
**Usage**: LLM agents use this for managing DDD framework updates and migrations
**Features**:
- Step-by-step migration procedures
- Rollback instructions
- Validation and success criteria
- Automated tracking integration

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
| Status tracking | YAML | `templates.yml/` |
| Execution planning | YAML | `templates.yml/` |
| Framework migrations | YAML | `templates.yml/` |
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
