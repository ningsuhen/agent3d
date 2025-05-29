# DDD Procedures (YAML Format)

This directory contains the YAML-formatted procedures for the Documentation Driven Development (DDD) framework. These procedures have been converted from the original `docs/COMMON-PROCEDURES.md` file and split into logical modules for better organization and LLM processing.

## File Organization

### Core Procedures
- **`core-patterns.yml`** - Essential patterns and LLM speed optimization rules
- **`configuration.yml`** - Configuration memorization and management procedures
- **`repository.yml`** - Repository management and project root detection
- **`templates.yml`** - Template usage and DDD workflow procedures

### Workflow Procedures
- **`git-workflow.yml`** - Git workflow with execution plan branch support
- **`standards.yml`** - Date/timestamp standards and validation procedures
- **`language-rules.yml`** - Language-specific rules and patterns
- **`planning.yml`** - Execution planning and status tracking procedures

### Quality and Analysis
- **`quality.yml`** - Quality standards and validation procedures
- **`drift-scanning.yml`** - Comprehensive drift detection procedures
- **`ft-tc-structure.yml`** - Merged Feature-Test Case structure procedures
- **`prune-pass.yml`** - Safe removal and repository cleanup procedures

## Usage Guidelines

### For LLM Agents
1. **Load at Session Start**: Memorize relevant procedure files based on current task
2. **Reference During Execution**: Use procedures as authoritative guidance
3. **Apply Consistently**: Follow procedures across all passes and operations
4. **Cache in Memory**: Avoid repeated file access during execution

### For Human Developers
1. **Reference Documentation**: Use as comprehensive procedure reference
2. **Onboarding**: Study procedures to understand DDD framework
3. **Troubleshooting**: Consult relevant procedure files for guidance
4. **Updates**: Modify procedures as framework evolves

## Key Features

### YAML Structure Benefits
- **Machine Readable**: Optimized for LLM processing and automation
- **Structured Data**: Hierarchical organization for easy navigation
- **Consistent Format**: Standardized structure across all procedure files
- **Metadata Rich**: Version tracking and update timestamps

### Modular Organization
- **Logical Grouping**: Related procedures grouped in dedicated files
- **Focused Content**: Each file covers specific aspect of DDD framework
- **Easy Maintenance**: Update individual modules without affecting others
- **Scalable Structure**: Add new procedure files as framework grows

## Migration from Markdown

This YAML structure replaces the original `docs/COMMON-PROCEDURES.md` file with the following improvements:

### Advantages
- **Better LLM Processing**: YAML format is more machine-readable
- **Modular Updates**: Change specific procedures without affecting others
- **Structured Validation**: YAML schema validation possible
- **Automation Friendly**: Easy integration with automated tools

### Backward Compatibility
- **Content Preservation**: All original procedures maintained
- **Enhanced Organization**: Better structure and navigation
- **Additional Metadata**: Version tracking and timestamps added
- **Cross-References**: Links between related procedures maintained

## Version Information

- **Format Version**: 1.0.0
- **Migration Date**: 2025-01-27
- **Source**: `docs/COMMON-PROCEDURES.md`
- **Maintenance**: Update individual files as needed

## Integration Points

### DDD Framework Integration
- **Pass Execution**: Referenced by all DDD passes
- **Configuration Management**: Integrated with `.agent3d-config.yml`
- **Tool Integration**: Used by drift scanner and other tools
- **Workflow Automation**: Supports automated DDD workflows

### External Dependencies
- **Agent3D Repository**: `~/.agent3d` for templates and tools
- **Project Configuration**: `.agent3d-config.yml` for project settings
- **Drift Scanner**: Integration with drift detection tools
- **Git Workflow**: Branch management and commit procedures

## Best Practices

### For Procedure Updates
1. **Version Control**: Update version numbers when making changes
2. **Timestamp Updates**: Update `last_updated` field
3. **Cross-Reference Check**: Verify links to other procedures
4. **Validation**: Test procedures after updates

### For Implementation
1. **Memorize Key Procedures**: Load critical procedures at session start
2. **Follow Consistently**: Apply procedures uniformly across operations
3. **Validate Results**: Use drift scanner to verify procedure compliance
4. **Document Deviations**: Record any necessary procedure modifications

## Future Enhancements

### Planned Improvements
- **Schema Validation**: YAML schema for procedure validation
- **Automated Testing**: Test procedure compliance automatically
- **Integration APIs**: Programmatic access to procedure data
- **Dynamic Updates**: Real-time procedure updates from repository

### Extension Points
- **Custom Procedures**: Add project-specific procedures
- **Language Extensions**: Additional language-specific procedures
- **Tool Integration**: Enhanced integration with development tools
- **Workflow Automation**: Automated procedure execution
