# DDD Passes - YAML Format

This directory contains all DDD passes converted to YAML format for optimal LLM agent processing and automation.

## Available Passes

### Core Passes
- `0_requirements_pass.yml` - Requirements Pass (Step 0)
- `1_foundation_pass.yml` - Foundation Pass (Step 1)
- `2_documentation_pass.yml` - Documentation Pass (Step 2)
- `3_development_pass.yml` - Development Pass (Step 3)
- `4_testing_pass.yml` - Testing Pass (Step 4)
- `5_refactoring_pass.yml` - Refactoring Pass (Step 5)
- `6_code_review_pass.yml` - Code Review Pass (Step 6)
- `7_prune_pass.yml` - Prune Pass (Step 7)
- `8_synchronization_pass.yml` - Synchronization Pass (Step 8)
- `9_reverse_pass.yml` - Reverse Pass (Step 9)

### Comprehensive Pass
- `full_pass.yml` - Full Pass (all passes in sequence)

## YAML Structure

Each pass YAML file contains:

```yaml
metadata:
  name: "Pass Name"
  number: 1
  purpose: "Pass purpose and objectives"
  role: "Expert role for execution"
  description: "Detailed description"

when_to_use:
  conditions: ["list of conditions"]
  prerequisites: ["required previous passes"]

process:
  workflow_pattern: "SCAN → DRAFT → ASK → SYNC → CONFIRM"
  phases:
    scan:
      description: "Phase description"
      actions: ["list of actions"]
    draft:
      description: "Phase description"
      actions: ["list of actions"]
    ask:
      description: "Phase description"
      protocol: ["interaction guidelines"]
    sync:
      description: "Phase description"
      actions: ["list of actions"]
    confirm:
      description: "Phase description"
      actions: ["list of actions"]

expected_outcomes: ["list of deliverables"]

quality_gates:
  - name: "gate_name"
    validation: "validation_method"
```

## Benefits of YAML Format

### For LLM Agents
- **Structured Data**: Hierarchical organization for easy parsing
- **Machine Readable**: Direct programmatic access to pass information
- **Conditional Logic**: Easy to implement decision trees
- **Validation**: Schema-based validation possible
- **Automation**: Perfect for automated workflow execution

### For Development Tools
- **API Integration**: Easy REST/GraphQL integration
- **Configuration Management**: Version-controlled pass definitions
- **Tooling Support**: IDE support for YAML editing and validation
- **Scripting**: Easy to process with automation scripts

## Usage Examples

### Loading Pass Configuration
```python
import yaml

# Load a specific pass
with open('passes.yml/1_foundation_pass.yml') as f:
    foundation_pass = yaml.safe_load(f)

# Access pass metadata
print(foundation_pass['metadata']['purpose'])

# Get workflow phases
phases = foundation_pass['process']['phases']
for phase_name, phase_config in phases.items():
    print(f"{phase_name}: {phase_config['description']}")
```

### Pass Selection Logic
```python
def select_pass_for_condition(condition):
    pass_mappings = {
        'missing_config': '1_foundation_pass.yml',
        'unclear_requirements': '0_requirements_pass.yml',
        'missing_documentation': '2_documentation_pass.yml',
        'implementation_needed': '3_development_pass.yml',
        'tests_failing': '5_testing_pass.yml',
        'code_quality_issues': '6_refactoring_pass.yml',
        'review_needed': '7_code_review_pass.yml',
        'docs_outdated': '9_synchronization_pass.yml',
        'cleanup_needed': '8_prune_pass.yml',
        'undocumented_code': '10_reverse_pass.yml'
    }
    return pass_mappings.get(condition, 'full_pass.yml')
```

### Workflow Automation
```python
def execute_pass_workflow(pass_config):
    phases = pass_config['process']['phases']

    for phase_name, phase_config in phases.items():
        print(f"Executing {phase_name}: {phase_config['description']}")

        for action in phase_config.get('actions', []):
            print(f"  - {action}")
            # Execute action logic here
```

## Integration with DDD Framework

### Decision Tree Integration
These YAML passes integrate with the `AGENT-DECISION-TREE.yml` for automated pass selection and execution.

### Status Tracking
Pass execution status is tracked in `DDD-STATUS.template.yml` with structured metadata.

### Quality Validation
Each pass includes quality gates that can be automatically validated during execution.

## YAML-First Approach

**As of 2025-01-27**, the DDD framework has migrated to a YAML-first approach for LLM agents:

- **Primary Format**: YAML versions are the authoritative source for LLM processing
- **Enhanced Structure**: Optimized organization for machine processing and automation
- **Metadata Enrichment**: Comprehensive fields for decision-making and validation
- **Validation Support**: Schema-based validation capabilities
- **Tool Integration**: Superior integration with development tools and CI/CD pipelines

**Note**: Markdown versions have been removed after validation confirmed YAML completeness. For human-readable documentation, refer to the main `AGENT-GUIDELINES.md` and `docs/` directory.

## Best Practices

### For LLM Agents
1. **Load Once**: Cache pass configurations at session start
2. **Validate Structure**: Ensure YAML is valid before processing
3. **Follow Workflow**: Execute phases in order (SCAN → DRAFT → ASK → SYNC → CONFIRM)
4. **Check Prerequisites**: Verify previous passes completed before starting
5. **Update Status**: Track progress in DDD-STATUS.yml

### For Development Teams
1. **Version Control**: Track changes to pass definitions
2. **Schema Validation**: Use YAML schemas for validation
3. **Documentation**: Keep both YAML and human-readable docs in sync
4. **Testing**: Test pass automation with sample projects
5. **Feedback**: Collect feedback on pass effectiveness and improve

## Schema Validation

A JSON schema for pass validation is available at `../schemas/pass.schema.json` (when created).

## Contributing

When modifying passes:
1. Update YAML versions (primary format)
2. Validate YAML syntax and structure
3. Test with sample projects and LLM agents
4. Update related documentation in `docs/`
5. Run quality gates validation
6. Ensure backward compatibility for existing automations

---

*These YAML passes enable sophisticated automation and decision-making for LLM agents while maintaining the comprehensive guidance of the original DDD framework.*
