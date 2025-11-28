# Agent3D Configuration Guide

Complete guide for configuring Agent3D using `.agent3d-config.yml` in project root.

**CRITICAL:**

## 🎯 Quick Start for Agents

### 1. For New Projects (Foundation Pass)

```bash
# Check if template exists
ls templates/agent3d-config.template.yml

# Copy template to project root
cp templates/agent3d-config.template.yml .agent3d-config.yml

# Edit placeholders manually or use Foundation Pass
# Validate configuration with drift scanner
python3 tools/drift_scanner.py --mode all --quiet
```

### 2. For Existing Projects (Configuration Validation)

```bash
# Validate current configuration
python3 tools/drift_scanner.py --mode all

# Check specific aspects
python3 tools/drift_scanner.py --mode code-coverage
python3 tools/drift_scanner.py --mode ft-tc-mapping

# Run comprehensive analysis
python3 tools/drift_scanner.py --mode all --output .agent3d-tmp/config-analysis.yaml
```

## 📋 Template Structure

The template includes all required sections with placeholder values:

### Core Sections
- **project**: Project metadata and type
- **enabled_passes**: DDD passes to enable
- **pass_config**: Pass-specific configuration
- **quality_gates**: Quality thresholds
- **validation**: Validation settings
- **git_workflow**: Git workflow configuration
- **documentation**: Documentation standards
- **identifier_patterns**: ID pattern definitions
- **drift_detection**: Drift detection settings
- **python_paths**: Python module resolution (for Python projects)
- **mcp_server**: MCP server configuration
- **templates**: Template configuration
- **structure**: Project structure
- **metadata**: Configuration metadata

## 🔍 Configuration Validation

### Drift Scanner Integration

```bash
# Comprehensive configuration analysis
python3 tools/drift_scanner.py --mode all

# Specific validation modes
python3 tools/drift_scanner.py --mode tc-mapping     # Test case mapping
python3 tools/drift_scanner.py --mode ft-mapping     # Feature mapping
python3 tools/drift_scanner.py --mode code-coverage  # Code coverage analysis
python3 tools/drift_scanner.py --mode feature-impl   # Feature implementation
python3 tools/drift_scanner.py --mode test-quality   # Test quality validation
```

### Configuration Health Checks

1. **YAML Syntax**: Validates configuration file syntax
2. **Section Completeness**: Ensures all required sections are present
3. **Path Validation**: Verifies directory and file paths exist
4. **Cross-Reference Integrity**: Validates internal references
5. **Template Compatibility**: Checks template system integration
6. **Drift Detection**: Identifies configuration-implementation misalignment

## Pass Configuration

```yaml
# Foundation Pass
foundation_pass:
  enabled: true
  templates: [README.template.md, FEATURES.template.md, HIGH-LEVEL-DESIGN.template.md]
  validation: strict

# Development Pass
development_pass:
  enabled: true
  type: "documentation_development"
  selection_mode: "auto"
  test_coverage_threshold: 80
  quality_gates: {lint_score: 8.0, complexity: low, security_scan: required}

# Testing Pass
testing_pass:
  enabled: true
  coverage_threshold: 80
  test_types: [unit, integration, edge_cases]
  framework_compliance: strict
```

## Project Configuration
```yaml
# .agent3d-config.yml
project: {name: "MyProject", type: "web_application", language: "python"}

pass_overrides:
  implementation: {test_coverage_threshold: 90, quality_gates: {lint_score: 9.0, complexity: very_low}}
  testing: {coverage_threshold: 95, additional_test_types: [performance, security]}

skip_passes: [prune]
custom_templates: {README: "custom/README.template.md", FEATURES: "custom/FEATURES.template.md"}
```

## Language Configuration

```yaml
# Python
python: {version: ">=3.8", package_manager: "pip", testing: {framework: "pytest", coverage_threshold: 85}, code_style: {formatter: "black", line_length: 88, linter: "flake8"}}

# JavaScript
javascript: {version: ">=16.0.0", package_manager: "npm", testing: {framework: "jest", coverage_threshold: 80}, code_style: {formatter: "prettier", linter: "eslint", typescript: true}}

# Java
java: {version: ">=11", build_tool: "gradle", testing: {framework: "junit5", coverage_threshold: 75}, code_style: {formatter: "spotless", static_analysis: [checkstyle, pmd, spotbugs]}}


```

## Templates & Thresholds

```yaml
# Template Configuration
template_overrides: {base_path: "custom/templates/", templates: {README: "custom-readme.template.md", FEATURES: "enhanced-features.template.md"}}
template_defaults: {author: "Development Team", license: "MIT", documentation_style: "google"}
template_validation: {mode: "strict", required_sections: "all", allow_empty_sections: false}

# Alignment Thresholds
alignment_thresholds: {excellent: 95, good: 85, acceptable: 70, poor: 50, critical: 0}
drift_thresholds: {none: 10, low: 25, medium: 50, high: 100}

# Quality Gates
quality_gates:
  weights: {documentation_completeness: 30, test_coverage: 25, code_quality: 25, alignment_consistency: 20}
  minimum_scores: {documentation: 80, testing: 75, implementation: 85, overall: 80}
```

## GitHub & Environment

```yaml
# GitHub Integration
github_integration:
  pr_review: {enabled: true, mode: "pending", language_rules: true, fallback_manual: true}
  comment_format: {severity_levels: [critical, high, medium, low], include_line_numbers: true, include_suggestions: true}
  auth: {method: "token", token_env_var: "GITHUB_TOKEN", fallback_manual: true}
```

```bash
# Environment Variables
AGENT3D_REPO="git@github.com:ningsuhen/agent3d.git"
AGENT3D_LOCAL_PATH=".agent3d"
DDD_UPDATE_INTERVAL="6h"
GITHUB_TOKEN="your_token_here"
DDD_CACHE_ENABLED="true"
DDD_MAX_WORKERS="4"
```

## Validation & Advanced

```yaml
# Validation Modes
validation:
  strict: {mode: "strict", enforce_all_rules: true, fail_on_warnings: true, require_all_sections: true, validate_links: true}
  relaxed: {mode: "relaxed", enforce_critical_only: true, allow_warnings: true, optional_sections: true, skip_link_validation: true}

# Git Workflow (CRITICAL - MEMORIZE THESE SETTINGS)
git_workflow:
  require_commit_confirmation: true      # true=ask before commit, false=no confirmation
  always_confirm_before_commit: true     # true=always ask, false=auto-commit allowed
  human_approval_required: true          # true=human approval needed, false=automated OK
  commit_message_format: "DDD: {pass_name} - {description}"

# Git Workflow Examples
git_workflow_examples:
  strict_mode: {require_commit_confirmation: true, always_confirm_before_commit: true, human_approval_required: true}
  automated_mode: {require_commit_confirmation: false, always_confirm_before_commit: false, human_approval_required: false}
  hybrid_mode: {require_commit_confirmation: true, always_confirm_before_commit: false, human_approval_required: true}

# Custom Validation
custom_validation:
  required_sections: ["Overview", "Installation", "Usage"]
  optional_sections: ["Contributing", "License"]
  custom_rules: [{name: "require_examples", pattern: "## Examples", required: true}, {name: "limit_line_length", max_length: 120}]

# LLM Compression
llm_compression: {enabled: true, compression_level: "aggressive", preserve_commands: true, preserve_project_specifics: true, remove_basic_explanations: true, compress_tasks: [git_operations, github_cli_usage, package_management, file_operations, standard_development_tools]}

# Advanced
multi_language: {primary: "python", secondary: ["javascript", "go"]}
monorepo: {enabled: true, subprojects: [{path: "backend/", language: "python"}]}
cicd: {enabled: true, trigger_on: ["pull_request", "push_to_main"], pipeline_steps: ["foundation_pass", "documentation_pass", "quality_pass"]}
```

## Configuration Update Protocol

**CRITICAL:** When updating .agent3d-config.yml, refresh memorized configuration.

**Usage:** Place `.agent3d-config.yml` in project root. Use Foundation Pass for initial setup.
