# Language Rules - YAML Format

This directory contains language-specific development rules converted to YAML format for optimal LLM agent processing and automated code review.

## Available Language Rules

- `python.yml` - Python development standards and best practices
- `javascript.yml` - JavaScript/TypeScript development rules
- `java.yml` - Java development standards
- `markdown.yml` - Markdown documentation rules and LLM optimization

## YAML Structure

Each language rule file contains:

```yaml
metadata:
  language: "language_name"
  version: "supported_versions"
  description: "Language-specific rules for DDD framework"
  last_updated: "2025-01-27"

environment:
  setup: "development environment configuration"
  dependencies: "dependency management rules"
  configuration: "project configuration standards"

code_style:
  formatting: "code formatting standards"
  naming_conventions: "naming rules and patterns"
  data_structures: "preferred data structure patterns"
  imports: "import organization rules"

documentation:
  docstrings: "documentation requirements"
  type_hints: "type annotation standards"
  comments: "commenting guidelines"

testing:
  framework: "preferred testing framework"
  structure: "test organization patterns"
  implementation_requirements: "critical testing rules"
  quality_standards: "test quality validation"

error_handling:
  exceptions: "error handling patterns"
  logging: "logging standards"

performance:
  optimization: "performance best practices"
  concurrency: "concurrent programming rules"

security:
  standards: "security requirements"
  prohibited: "security anti-patterns"

code_review:
  role: "reviewer expertise level"
  critical_areas: "focus areas for review"
  severity_levels: "issue classification"

quality_gates:
  language_specific: "language-specific quality checks"
  universal: "cross-language quality standards"
```

## Benefits of YAML Format

### For LLM Agents
- **Structured Rules**: Hierarchical organization for easy rule lookup
- **Automated Review**: Direct integration with code review automation
- **Decision Support**: Clear severity levels and quality gates
- **Context Awareness**: Language-specific vs universal rules
- **Validation**: Automated quality gate checking

### For Development Tools
- **IDE Integration**: Language server integration possibilities
- **CI/CD Integration**: Automated quality checking in pipelines
- **Linting Configuration**: Generate linter configs from rules
- **Documentation Generation**: Auto-generate coding standards docs

## Usage Examples

### Loading Language Rules
```python
import yaml

# Load Python rules
with open('rules.yml/python.yml') as f:
    python_rules = yaml.safe_load(f)

# Access testing requirements
testing_rules = python_rules['testing']['implementation_requirements']
for rule in testing_rules['critical_rules']:
    print(f"Critical: {rule['name']} - {rule['description']}")
```

### Code Review Automation
```python
def get_review_criteria(language):
    with open(f'rules.yml/{language}.yml') as f:
        rules = yaml.safe_load(f)

    return {
        'role': rules['code_review']['role'],
        'critical_areas': rules['code_review']['critical_areas'],
        'severity_levels': rules['code_review']['severity_levels']
    }

def classify_issue_severity(issue, language_rules):
    severity_levels = language_rules['code_review']['severity_levels']

    for level, issues in severity_levels.items():
        if issue in issues['issues']:
            return level

    return 'low'
```

### Quality Gate Validation
```python
def validate_quality_gates(code_analysis, language):
    with open(f'rules.yml/{language}.yml') as f:
        rules = yaml.safe_load(f)

    quality_gates = rules['quality_gates']
    results = {}

    for gate_name, gate_config in quality_gates.items():
        if isinstance(gate_config, list):
            for gate in gate_config:
                check_name = gate['name']
                validation = gate['check']
                results[check_name] = validate_check(code_analysis, validation)

    return results
```

### Language-Specific Configuration
```python
def generate_project_config(language, project_type):
    with open(f'rules.yml/{language}.yml') as f:
        rules = yaml.safe_load(f)

    config = {
        'environment': rules['environment'],
        'code_style': rules['code_style'],
        'testing': rules['testing']['framework']
    }

    # Customize based on project type
    if project_type == 'library':
        config['documentation'] = rules['documentation']

    return config
```

## Language-Specific Features

### Python (`python.yml`)
- **Testing Framework**: pytest with golden file testing
- **Critical Requirements**: Real project code testing, TC ID mapping
- **Type Safety**: Comprehensive type hints and validation
- **Import Rules**: Strict import organization and project code imports

### JavaScript (`javascript.yml`)
- **Modern Standards**: ES6+, TypeScript support
- **Testing**: Jest/Vitest with component testing
- **Build Tools**: Modern bundling and tooling standards
- **Framework Integration**: React, Vue, Angular specific rules

### Java (`java.yml`)
- **Enterprise Standards**: Spring Boot, Maven/Gradle
- **Testing**: JUnit 5 with comprehensive test strategies
- **Code Quality**: SonarQube integration, PMD rules
- **Performance**: JVM optimization and memory management

### Go (`go.yml`)
- **Idiomatic Go**: Go-specific patterns and conventions
- **Testing**: Built-in testing with table-driven tests
- **Performance**: Goroutines and channel best practices
- **Tooling**: Go modules, gofmt, golint integration

### Markdown (`markdown.yml`)
- **LLM Optimization**: Structure for AI processing
- **Documentation Standards**: Consistent formatting rules
- **Link Management**: Reference and validation rules
- **Template Integration**: DDD template compliance

## Integration with DDD Framework

### Pass Integration
Language rules integrate with DDD passes for:
- **Code Review Pass**: Automated review criteria
- **Testing Pass**: Language-specific testing requirements
- **Refactoring Pass**: Language-specific optimization patterns

### Quality Validation
Rules provide quality gates for:
- **Synchronization Pass**: Code-documentation alignment
- **Development Pass**: Implementation standards
- **Foundation Pass**: Project setup standards

### Tool Integration
- **Drift Scanner**: Language-aware drift detection
- **MCP Servers**: Real-time rule validation
- **VSCode Extension**: IDE integration for rule enforcement

## YAML-First Approach

**As of 2025-01-27**, the DDD framework has migrated to a YAML-first approach for language rules:

- **Primary Format**: YAML versions are the authoritative source for LLM processing
- **Machine Processing**: Optimized automation and tool integration
- **Structured Validation**: Programmatic quality gate checking and rule enforcement
- **Enhanced Metadata**: Comprehensive fields for automated decision-making
- **Conditional Logic**: Context-aware rule application and severity classification

**Note**: Markdown versions have been removed after validation confirmed YAML completeness. For human-readable documentation, refer to the main `AGENT-GUIDELINES.md` and language-specific sections in `docs/`.

## Best Practices

### For LLM Agents
1. **Cache Rules**: Load language rules once per session
2. **Context Awareness**: Apply rules based on file types and project context
3. **Severity Handling**: Prioritize critical issues over style issues
4. **Progressive Enhancement**: Start with critical rules, add others gradually
5. **Feedback Integration**: Learn from code review outcomes

### For Development Teams
1. **Consistency**: Ensure rules align with team practices
2. **Tool Integration**: Configure linters and IDEs based on rules
3. **Training**: Use rules for onboarding and code review training
4. **Evolution**: Update rules based on team experience and industry changes
5. **Documentation**: Keep rules synchronized with team documentation

## Schema Validation

JSON schemas for rule validation are available at `../schemas/rules.schema.json` (when created).

## Contributing

When modifying language rules:
1. Update YAML versions (primary format)
2. Validate YAML syntax and structure
3. Test with real projects in the target language
4. Ensure quality gates are testable and measurable
5. Update integration documentation in `docs/`
6. Verify LLM agent compatibility and performance

## Custom Rules

Teams can extend rules by:
1. Adding custom sections to existing language files
2. Creating new language rule files
3. Overriding specific rules in project `.agent3d-config.yml`
4. Contributing improvements back to the framework

---

*These YAML language rules enable sophisticated automated code review and quality validation while maintaining the comprehensive guidance of the original DDD framework.*
