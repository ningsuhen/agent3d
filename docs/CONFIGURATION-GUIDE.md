# Configuration Guide

Configure Agent3D using `.agent3d-config.yml` in project root.

**CRITICAL FOR LLM AGENTS:** MEMORIZE the ENTIRE .agent3d-config.yml file at session start. Load once, use from memory throughout all passes.

## Pass Configuration

```yaml
# Foundation Pass
foundation_pass:
  enabled: true
  templates: [README.template.md, FEATURES.template.md, HIGH-LEVEL-DESIGN.template.md]
  validation: strict

# Implementation Pass
implementation_pass:
  enabled: true
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

# Go
go: {version: ">=1.19", testing: {coverage_threshold: 80, race_detection: true}, code_style: {formatter: "gofmt", linter: "golangci-lint"}}
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
AGENT3D_LOCAL_PATH="~/.agent3d"
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

**CRITICAL FOR LLM AGENTS:** When updating .agent3d-config.yml, ALWAYS refresh memorized configuration.

---

**Usage:** Place `.agent3d-config.yml` in project root. Use Foundation Pass to create initial configuration. ALWAYS refresh memory when config is updated.
