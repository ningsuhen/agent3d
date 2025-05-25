# Configuration Guide

This document explains how to configure and customize Agent3D for specific project needs using `.agent3d-config.yml` as the primary configuration file.

## Pass Configuration

### Default Pass Settings

Each DDD pass has configurable settings that can be customized:

**Foundation Pass:**
```yaml
foundation_pass:
  enabled: true
  templates:
    - README.template.md
    - FEATURES.template.md
    - HIGH-LEVEL-DESIGN.template.md
  validation: strict
  required_sections: all
```

**Implementation Pass:**
```yaml
implementation_pass:
  enabled: true
  test_coverage_threshold: 80
  quality_gates:
    lint_score: 8.0
    complexity: low
    security_scan: required
```

**Testing Pass:**
```yaml
testing_pass:
  enabled: true
  coverage_threshold: 80
  test_types:
    - unit
    - integration
    - edge_cases
  framework_compliance: strict
```

### Project-Specific Configuration

Each project uses `.agent3d-config.yml` in the project root as the primary configuration file:

**Configuration File Location:**
- **Primary:** `.agent3d-config.yml` in project root (same directory as `.agent3d` file)
- **Alternative:** `docs/.agent3d-config.yml` for documentation-specific settings (legacy)

**Example Configuration:**
```yaml
# .agent3d-config.yml
project:
  name: "MyProject"
  type: "web_application"
  language: "python"

pass_overrides:
  implementation:
    test_coverage_threshold: 90
    quality_gates:
      lint_score: 9.0
      complexity: very_low

  testing:
    coverage_threshold: 95
    additional_test_types:
      - performance
      - security

skip_passes:
  - prune  # Skip prune pass for this project

custom_templates:
  README: "custom/README.template.md"
  FEATURES: "custom/FEATURES.template.md"
```

## Language-Specific Configuration

### Python Configuration
```yaml
python:
  version: ">=3.8"
  package_manager: "pip"  # or "poetry", "pipenv"
  testing:
    framework: "pytest"
    coverage_threshold: 85
  code_style:
    formatter: "black"
    line_length: 88
    linter: "flake8"
  dependencies:
    management: "pyproject.toml"
    lock_file: "requirements-lock.txt"
```

### JavaScript Configuration
```yaml
javascript:
  version: ">=16.0.0"
  package_manager: "npm"  # or "yarn", "pnpm"
  testing:
    framework: "jest"
    coverage_threshold: 80
  code_style:
    formatter: "prettier"
    linter: "eslint"
    typescript: true
```

### Java Configuration
```yaml
java:
  version: ">=11"
  build_tool: "gradle"  # or "maven"
  testing:
    framework: "junit5"
    coverage_threshold: 75
  code_style:
    formatter: "spotless"
    static_analysis:
      - checkstyle
      - pmd
      - spotbugs
```

### Go Configuration
```yaml
go:
  version: ">=1.19"
  testing:
    coverage_threshold: 80
    race_detection: true
  code_style:
    formatter: "gofmt"
    linter: "golangci-lint"
```

## Template Configuration

### Custom Template Paths
Override default templates with project-specific versions:

```yaml
template_overrides:
  base_path: "custom/templates/"
  templates:
    README: "custom-readme.template.md"
    FEATURES: "enhanced-features.template.md"
    TASKS: "agile-tasks.template.md"
```

### Template Variables
Configure default values for template variables:

```yaml
template_defaults:
  author: "Development Team"
  license: "MIT"
  contributing_guidelines: "See CONTRIBUTING.md"
  documentation_style: "google"  # or "numpy", "sphinx"
```

### Template Validation
Configure validation strictness:

```yaml
template_validation:
  mode: "strict"  # or "relaxed", "custom"
  required_sections: "all"  # or list of specific sections
  allow_empty_sections: false
  enforce_format_compliance: true
```

## Metrics and Thresholds

### Alignment Thresholds
Configure when passes are considered complete:

```yaml
alignment_thresholds:
  excellent: 95  # 95%+ alignment
  good: 85       # 85-94% alignment
  acceptable: 70 # 70-84% alignment
  poor: 50       # 50-69% alignment
  critical: 0    # <50% alignment
```

### Drift Indicators
Configure drift level calculations:

```yaml
drift_thresholds:
  none: 10       # 0-10% drift
  low: 25        # 11-25% drift
  medium: 50     # 26-50% drift
  high: 100      # 51%+ drift
```

### Quality Gates
Configure quality score calculations:

```yaml
quality_gates:
  documentation_completeness: 30  # 30% weight
  test_coverage: 25               # 25% weight
  code_quality: 25                # 25% weight
  alignment_consistency: 20       # 20% weight

  minimum_scores:
    documentation: 80
    testing: 75
    implementation: 85
    overall: 80
```

## GitHub Integration Configuration

### PR Review Settings
Configure automated PR review behavior:

```yaml
github_integration:
  pr_review:
    enabled: true
    mode: "pending"  # Submit reviews in pending mode
    language_rules: true
    fallback_manual: true

  comment_format:
    severity_levels:
      - critical
      - high
      - medium
      - low
    include_line_numbers: true
    include_suggestions: true
```

### Authentication
Configure GitHub CLI authentication:

```yaml
github_auth:
  method: "token"  # or "oauth", "ssh"
  token_env_var: "GITHUB_TOKEN"
  fallback_manual: true
```

## Environment Variables

### Core Configuration
```bash
# Repository configuration
AGENT3D_REPO="git@github.com:ningsuhen/agent3d.git"
AGENT3D_LOCAL_PATH="~/.agent3d"

# Pass configuration
DDD_UPDATE_INTERVAL="6h"  # Update interval
DDD_CONFIG_PATH=".agent3d-config.yml"

# GitHub integration
GITHUB_TOKEN="your_token_here"
GH_DEBUG="1"  # Enable debug mode

# Language-specific
PYTHON_VERSION="3.9"
NODE_VERSION="16.0.0"
JAVA_VERSION="11"
GO_VERSION="1.19"
```

### Performance Tuning
```bash
# Performance optimization
DDD_CACHE_ENABLED="true"
DDD_PARALLEL_PROCESSING="true"
DDD_MAX_WORKERS="4"

# Resource limits
DDD_MAX_MEMORY="512MB"
DDD_TIMEOUT="300s"
```

## Validation Configuration

### Strict Mode
Maximum validation and compliance checking:

```yaml
validation:
  mode: "strict"
  enforce_all_rules: true
  fail_on_warnings: true
  require_all_sections: true
  validate_links: true
  check_formatting: true
```

### Relaxed Mode
Flexible validation for rapid development:

```yaml
validation:
  mode: "relaxed"
  enforce_critical_only: true
  allow_warnings: true
  optional_sections: true
  skip_link_validation: true
```

### Custom Validation Rules
Define project-specific validation:

```yaml
custom_validation:
  required_sections:
    - "Overview"
    - "Installation"
    - "Usage"
  optional_sections:
    - "Contributing"
    - "License"
  custom_rules:
    - name: "require_examples"
      pattern: "## Examples"
      required: true
    - name: "limit_line_length"
      max_length: 120
```

## LLM-Specific Configuration

### Documentation Compression for LLMs
Configure refactoring pass to compress documentation for LLM consumption:

```yaml
refactoring:
  type: "documentation"
  scope: "markdown_only"
  focus:
    - structure_optimization
    - content_consolidation
    - duplicate_removal
    - clarity_improvement
    - llm_focused_compression  # Remove verbose explanations of basic tasks

llm_compression:
  enabled: true
  compression_level: "aggressive"  # or "moderate", "conservative"
  preserve_commands: true
  preserve_project_specifics: true
  remove_basic_explanations: true

  # Tasks to compress (remove verbose explanations)
  compress_tasks:
    - git_operations
    - github_cli_usage
    - package_management
    - file_operations
    - standard_development_tools
```

### LLM Compression Examples
```yaml
# Example compression rules
compression_rules:
  github_cli:
    before: "To leave a PR comment using GitHub CLI, first install gh, then authenticate, then use gh pr comment"
    after: "Leave PR comment with gh pr comment"

  git_operations:
    before: "Create a new branch by running git checkout -b feature-name where feature-name should be descriptive"
    after: "Create feature branch with git checkout -b feature-name"
```

## Advanced Configuration

### Multi-Language Projects
Configure for projects using multiple languages:

```yaml
multi_language:
  primary: "python"
  secondary:
    - "javascript"
    - "go"

  language_specific_rules:
    apply_all: true
    merge_conflicts: "primary_wins"
```

### Monorepo Configuration
Configure for monorepo structures:

```yaml
monorepo:
  enabled: true
  subprojects:
    - path: "backend/"
      language: "python"
      config: "backend/.agent3d-config.yml"
    - path: "frontend/"
      language: "javascript"
      config: "frontend/.agent3d-config.yml"
```

### CI/CD Integration
Configure for automated pipeline integration:

```yaml
cicd:
  enabled: true
  trigger_on:
    - "pull_request"
    - "push_to_main"

  pipeline_steps:
    - "foundation_pass"
    - "documentation_pass"
    - "quality_pass"

  failure_handling:
    mode: "fail_fast"  # or "continue", "warn"
    notify: true
```

---

**Usage:** Place `.agent3d-config.yml` in project root (same directory as `.agent3d` file). Configuration is loaded automatically when running DDD passes. Use Foundation Pass to create initial configuration through interactive setup.
