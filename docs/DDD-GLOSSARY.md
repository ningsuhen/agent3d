# DDD Glossary - YAML Format

```yaml
# DDD Glossary - Complete Reference
# Documentation-Driven Development (DDD) Framework Terminology and Commands

metadata:
  title: "DDD Glossary - Complete Reference"
  description: "Documentation-Driven Development (DDD) Framework Terminology and Commands"
  last_updated: "2025-01-27"
  format: "yaml"
  version: "1.0.0"

# Core Concepts
core_concepts:
  ddd:
    name: "DDD (Documentation-Driven Development)"
    definition: "Framework where documentation leads and code follows. Documentation is the single source of truth."
    category: "framework"

  prime_directive:
    name: "Prime Directive"
    definition: "Documentation leads, code follows - Always update docs before implementing code."
    category: "principle"

  agent3d:
    name: "Agent3D"
    definition: "The complete DDD framework ecosystem including passes, tools, templates, and guidelines."
    category: "framework"

  project_root:
    name: "Project Root"
    definition: "Directory containing .agent3d-config.yml - establishes DDD project boundaries."
    category: "structure"

  ddd_root:
    name: "DDD_ROOT"
    definition: "Environment variable pointing to DDD project root directory for tools and MCP servers."
    category: "environment"

# Pass System
pass_system:
  pass:
    name: "Pass"
    definition: "Structured workflow unit following Scan → Draft → Ask → Sync pattern."
    category: "workflow"

  pass_execution_pattern:
    name: "Pass Execution Pattern"
    definition: "Standard 4-phase workflow: SCAN (detect gaps) → DRAFT (create/update) → ASK (clarify) → SYNC (implement)."
    category: "workflow"
    phases:
      - "SCAN: detect gaps"
      - "DRAFT: create/update"
      - "ASK: clarify"
      - "SYNC: implement"

  pass_hooks:
    name: "Pass Hooks"
    definition: "Automated triggers that run before/after passes"
    category: "automation"
    types:
      before_hooks:
        - "Load config"
        - "Validate dependencies"
        - "Setup workspace"
      after_hooks:
        - "Update status"
        - "Cleanup"
        - "Validate completion"
      error_hooks:
        - "Handle failures"
        - "Recovery procedures"

  pass_dependencies:
    name: "Pass Dependencies"
    definition: "Required execution order for passes"
    category: "workflow"
    order:
      - "Requirements"
      - "Foundation"
      - "Documentation"
      - "Development"
      - "Testing"
      - "Refactoring"
      - "Code Review"
      - "Synchronization"
      - "Prune"
      - "Reverse"

  full_pass:
    name: "Full Pass"
    definition: "Comprehensive pass executing all numbered passes (0-10) for complete project alignment."
    category: "workflow"

# Individual Passes
individual_passes:
  requirements_pass:
    number: 0
    name: "Requirements Pass"
    definition: "Document comprehensive requirements and business objectives."
    category: "documentation"

  foundation_pass:
    number: 1
    name: "Foundation Pass"
    definition: "Project configuration, core documentation setup, identifier patterns configuration."
    category: "setup"
    critical: true

  documentation_pass:
    number: 2
    name: "Documentation Pass"
    definition: "Feature documentation, requirements clarification, acceptance criteria."
    category: "documentation"

  development_pass:
    number: 3
    name: "Development Pass"
    definition: "Step-by-step implementation with execution plans and checkpoints."
    category: "implementation"

  testing_pass:
    number: 4
    name: "Testing Pass"
    definition: "Comprehensive test creation and validation with real project code testing."
    category: "quality"

  refactoring_pass:
    number: 5
    name: "Refactoring Pass"
    definition: "Code cleanup without functionality changes, DRY principle application."
    category: "maintenance"

  code_review_pass:
    number: 6
    name: "Code Review Pass"
    definition: "PR review with language-specific standards enforcement."
    category: "quality"

  synchronization_pass:
    number: 7
    name: "Synchronization Pass"
    definition: "Documentation-code alignment at any scale, drift detection."
    category: "alignment"
    critical: true

  prune_pass:
    number: 8
    name: "Prune Pass"
    definition: "Remove outdated or redundant content and documentation."
    category: "maintenance"

  reverse_pass:
    number: 9
    name: "Reverse Pass"
    definition: "Detect and address reverse drift (implementation without documentation)."
    category: "alignment"

# Workflow Concepts
workflow_concepts:
  scan_draft_ask_sync:
    name: "Scan → Draft → Ask → Sync"
    definition: "Core workflow pattern for all DDD operations."
    category: "pattern"

  execution_plan:
    name: "Execution Plan"
    definition: "Detailed step-by-step plan for complex changes stored in docs/runs/EXEC-PLAN-{name}.md."
    category: "planning"
    location: "docs/runs/EXEC-PLAN-{name}.md"

  execution_plan_branch:
    name: "Execution Plan Branch"
    definition: "Git branch (exec-plan/*) for tracking execution steps with auto-commit capability."
    category: "git"
    pattern: "exec-plan/*"

  checkpoint:
    name: "Checkpoint"
    definition: "Milestone in execution plan marked with git tags and status updates."
    category: "tracking"

  drift:
    name: "Drift"
    definition: "Misalignment between documentation and implementation."
    category: "quality"

  alignment:
    name: "Alignment"
    definition: "Percentage measure of documentation-code synchronization (target: 90%+)."
    category: "quality"
    target: "90%+"

  quality_gates:
    name: "Quality Gates"
    definition: "Validation criteria that must be met before pass completion."
    category: "validation"

# Identifier System
identifier_system:
  ft_nnnn:
    name: "FT-NNNN (Feature Tracking)"
    definition: "Feature identifiers (e.g., FT-CORE-001, FT-PASS-002) for tracking features."
    category: "identifier"
    examples:
      - "FT-CORE-001"
      - "FT-PASS-002"

  tc_nnnn:
    name: "TC-NNNN (Test Case)"
    definition: "Test case identifiers (e.g., TC-CORE-001, TC-PASS-002a) for test traceability."
    category: "identifier"
    examples:
      - "TC-CORE-001"
      - "TC-PASS-002a"

  req_nnnn:
    name: "REQ-NNNN (Requirements)"
    definition: "Requirement identifiers linking business objectives to features."
    category: "identifier"

  ft_tc_mapping:
    name: "FT-TC Mapping"
    definition: "Relationship tracking between features and their test cases."
    category: "relationship"

  identifier_patterns:
    name: "Identifier Patterns"
    definition: "Configurable patterns in .agent3d-config.yml for project-specific ID formats."
    category: "configuration"
    location: ".agent3d-config.yml"

# Documentation Structure
documentation_structure:
  core_documentation:
    name: "Core Documentation"
    definition: "Required files for DDD projects"
    category: "structure"
    required_files:
      - "README.md"
      - "BUSINESS-OBJECTIVES.md"
      - "REQUIREMENTS.md"
      - "USER-STORIES.md"
      - "ACCEPTANCE-CRITERIA.md"
      - "FEATURES.md"
      - "HIGH-LEVEL-DESIGN.md"
      - "TASKS.md"
      - "TEST-CASES.md"
      - "DDD-STATUS.md"

  merged_ft_tc_structure:
    name: "Merged FT-TC Structure"
    definition: "New organization where features and test cases are co-located in docs/features/ section files."
    category: "structure"
    location: "docs/features/"

  section_files:
    name: "Section Files"
    definition: "Modular feature organization"
    category: "structure"
    files:
      - "core.md"
      - "implementation.md"
      - "integration.md"
      - "language-rules.md"
      - "passes.md"
      - "proposals.md"
      - "status-tracking.md"
      - "templates.md"

  template_system:
    name: "Template System"
    definition: "Standardized document formats in ~/.agent3d/templates/ with placeholder replacement."
    category: "templating"
    location: "~/.agent3d/templates/"

  template_tags:
    name: "Template Tags"
    definition: "{{placeholder}} markers replaced during document creation, <template> tags removed."
    category: "templating"
    placeholder_format: "{{placeholder}}"
    removal_tags: "<template>"

# Configuration System
configuration_system:
  agent3d_config_yml:
    name: ".agent3d-config.yml"
    definition: "Project configuration file defining enabled passes, quality thresholds, and project settings."
    category: "configuration"
    location: "project_root"

  configuration_memorization:
    name: "Configuration Memorization"
    definition: "Critical requirement: LLM agents must memorize entire config at session start."
    category: "requirement"
    critical: true

  pass_configuration:
    name: "Pass Configuration"
    definition: "Pass-specific settings including enabled status, thresholds, and validation rules."
    category: "configuration"

  git_workflow_configuration:
    name: "Git Workflow Configuration"
    definition: "Settings for commit confirmation, execution plan branches, and automation behavior."
    category: "configuration"

  quality_thresholds:
    name: "Quality Thresholds"
    definition: "Alignment and drift thresholds"
    category: "configuration"
    thresholds:
      excellent: "95%"
      good: "85%"
      acceptable: "70%"
      poor: "50%"
      critical: "0%"

# Tools and Utilities
tools_and_utilities:
  drift_scanner:
    name: "Drift Scanner"
    definition: "Multi-mode analysis tool detecting various types of documentation-code drift."
    category: "tool"
    critical: true

  drift_scanner_modes:
    name: "Drift Scanner Modes"
    definition: "Analysis modes for drift detection"
    category: "tool"
    modes:
      tc_mapping: "Test case to implementation mapping"
      ft_mapping: "Feature to implementation mapping"
      ft_tc_mapping: "Feature-test case relationship validation"
      code_coverage: "Test coverage analysis"
      feature_impl: "Feature implementation status"
      test_quality: "Test quality validation"
      all: "Comprehensive analysis"

  mcp_server:
    name: "MCP Server"
    definition: "Model Context Protocol server for drift scanner integration with AI clients."
    category: "tool"

  migration_manager:
    name: "Migration Manager"
    definition: "Tool for managing DDD framework migrations and updates."
    category: "tool"

  vscode_ddd_navigator:
    name: "VSCode DDD Navigator"
    definition: "Extension for navigating DDD documentation structure."
    category: "tool"

# Status and Tracking
status_and_tracking:
  ddd_status:
    name: "DDD Status"
    definition: "Central tracking document (docs/DDD-STATUS.md) monitoring all pass statuses and health."
    category: "tracking"
    location: "docs/DDD-STATUS.md"

  status_icons:
    name: "Status Icons"
    definition: "Visual indicators for pass status"
    category: "tracking"
    icons:
      complete: "✅"
      paused: "⏸️"
      in_progress: "🔄"
      skipped: "⏭️"
      failed: "❌"

  drift_indicators:
    name: "Drift Indicators"
    definition: "Visual indicators for drift levels"
    category: "tracking"
    indicators:
      low: "🟢 Low drift (<10%)"
      moderate: "🟡 Moderate drift (10-25%)"
      high: "🟠 High drift (25-50%)"
      critical: "🔴 Critical drift (>50%)"

  health_indicators:
    name: "Health Indicators"
    definition: "Overall project health metrics combining alignment, drift, and completion status."
    category: "tracking"

# Testing Concepts
testing_concepts:
  real_testing:
    name: "Real Testing"
    definition: "Critical requirement: Tests must import and call actual project code, not just mock data."
    category: "requirement"
    critical: true

  test_quality_validation:
    name: "Test Quality Validation"
    definition: "Ensuring tests import from git-tracked project directories and call project functions."
    category: "validation"

  tc_id_mapping:
    name: "TC ID Mapping"
    definition: "One-to-one relationship between test cases and test implementations."
    category: "mapping"

  integration_focus:
    name: "Integration Focus"
    definition: "Preference for integration tests over pure unit tests with mocks."
    category: "approach"

  test_coverage_threshold:
    name: "Test Coverage Threshold"
    definition: "Minimum percentage of code covered by tests (typically 80-95%)."
    category: "threshold"
    range: "80-95%"

# Git and Version Control
git_and_version_control:
  commit_confirmation:
    name: "Commit Confirmation"
    definition: "Configurable requirement for human approval before commits."
    category: "workflow"

  ddd_commit_format:
    name: "DDD Commit Format"
    definition: "Standard format for DDD commits"
    category: "format"
    format: "DDD: <Pass Name> - <Description>"

  execution_plan_commits:
    name: "Execution Plan Commits"
    definition: "Auto-commit format for execution steps"
    category: "format"
    format: "EXEC: Step {number} - {description}"

  checkpoint_commits:
    name: "Checkpoint Commits"
    definition: "Milestone format for checkpoints"
    category: "format"
    format: "CHECKPOINT: {number} - {description}"

  branch_patterns:
    name: "Branch Patterns"
    definition: "Standard branch naming conventions"
    category: "convention"
    patterns:
      exec_plan: "exec-plan/*"
      main: "main"
      feature: "feature/*"

# Language Support
language_support:
  language_rules:
    name: "Language Rules"
    definition: "Specific development standards for supported languages stored in ~/.agent3d/rules/."
    category: "standards"
    location: "~/.agent3d/rules/"

  multi_language_support:
    name: "Multi-Language Support"
    definition: "Framework supports multiple programming languages with language-specific configurations."
    category: "capability"

  language_configuration:
    name: "Language Configuration"
    definition: "Language-specific settings in .agent3d-config.yml for tools, testing, and standards."
    category: "configuration"
    supported_languages:
      - "Python"
      - "JavaScript"
      - "TypeScript"
      - "Java"
      - "Go"
      - "Rust"

# Advanced Features
advanced_features:
  horizontal_merging:
    name: "Horizontal Merging"
    definition: "Refactoring technique combining similar components across the codebase."
    category: "technique"

  llm_compression:
    name: "LLM Compression"
    definition: "Optimization technique reducing verbose documentation while preserving essential information."
    category: "optimization"

  change_based_scanning:
    name: "Change-Based Scanning"
    definition: "Fast drift detection analyzing only files changed since last commit/branch."
    category: "optimization"

  pr_focused_scanning:
    name: "PR-Focused Scanning"
    definition: "Drift analysis limited to files in current pull request."
    category: "optimization"

  migration_system:
    name: "Migration System"
    definition: "Structured approach to framework updates with migration tracking."
    category: "system"

  workflow_orchestration:
    name: "Workflow Orchestration"
    definition: "Automated coordination of pass execution with dependency management."
    category: "automation"

# File Locations
file_locations:
  agent3d_repository:
    name: "Agent3D Repository"
    definition: "Central location for all DDD framework resources"
    category: "location"
    path: "~/.agent3d"

  templates_directory:
    name: "Templates Directory"
    definition: "Document templates with placeholders"
    category: "location"
    path: "~/.agent3d/templates/"

  rules_directory:
    name: "Rules Directory"
    definition: "Language-specific development rules"
    category: "location"
    path: "~/.agent3d/rules.yml/ (LLM) | ~/.agent3d/rules/ (human)"

  passes_directory:
    name: "Passes Directory"
    definition: "Pass documentation and procedures"
    category: "location"
    path: "~/.agent3d/passes.yml/ (LLM) | ~/.agent3d/passes/simplified/ (human)"

  tools_directory:
    name: "Tools Directory"
    definition: "Utilities including drift scanner and migration manager"
    category: "location"
    path: "~/.agent3d/tools/"

  temporary_directory:
    name: "Temporary Directory"
    definition: "Project-specific temporary files and reports"
    category: "location"
    path: ".agent3d-tmp/"

  reports_directory:
    name: "Reports Directory"
    definition: "Drift scanner output location"
    category: "location"
    path: ".agent3d-tmp/drift-reports/"

# Commands and Operations
commands_and_operations:
  repository_update:
    name: "Repository Update"
    definition: "Update Agent3D framework"
    category: "command"
    command: "git -C ~/.agent3d pull origin main"

  drift_scanning:
    name: "Drift Scanning"
    definition: "Analyze project drift"
    category: "command"
    command: "python3 ~/.agent3d/tools/drift_scanner.py --mode <mode>"

  migration_check:
    name: "Migration Check"
    definition: "Check for pending migrations"
    category: "command"
    command: "python tools/migration_manager.py status"

  date_commands:
    name: "Date Commands"
    definition: "Standard date format for timestamps"
    category: "command"
    command: "date +%Y-%m-%d"

  configuration_loading:
    name: "Configuration Loading"
    definition: "Load and memorize entire .agent3d-config.yml at session start"
    category: "operation"
    critical: true

  pass_execution:
    name: "Pass Execution"
    definition: "Follow Scan → Draft → Ask → Sync → Confirm workflow for all passes"
    category: "operation"
    workflow: "Scan → Draft → Ask → Sync → Confirm"

# Bootstrap Operations
bootstrap_operations:
  framework_installation:
    name: "Framework Installation"
    definition: "Clone or update Agent3D framework"
    category: "bootstrap"
    commands:
      - "git clone git@github.com:ningsuhen/agent3d.git ~/.agent3d"
      - "cd ~/.agent3d && git pull"

  project_configuration:
    name: "Project Configuration"
    definition: "Create .agent3d-config.yml with project settings"
    category: "bootstrap"
    file: ".agent3d-config.yml"

  directory_structure:
    name: "Directory Structure"
    definition: "Create required DDD directories"
    category: "bootstrap"
    directories:
      - "docs/features"
      - "docs/migrations"
      - "docs/runs"
      - ".agent3d-tmp/drift-reports"

  environment_setup:
    name: "Environment Setup"
    definition: "Set DDD_ROOT environment variable"
    category: "bootstrap"
    command: "export DDD_ROOT=$(pwd)"

# Quick Reference
quick_reference:
  framework_location: "~/.agent3d/"
  project_config: ".agent3d-config.yml (in project root)"
  environment_variable: "DDD_ROOT=$(pwd)"
  entry_point: "~/.agent3d/AGENT-GUIDELINES.md"
  tools: "~/.agent3d/tools/"
  templates: "~/.agent3d/templates/"

# Categories
categories:
  framework: "Core framework concepts and components"
  principle: "Fundamental principles and directives"
  structure: "File and directory organization"
  environment: "Environment variables and setup"
  workflow: "Process and execution patterns"
  automation: "Automated triggers and processes"
  setup: "Initial configuration and setup"
  documentation: "Documentation creation and management"
  implementation: "Code development and implementation"
  quality: "Quality assurance and validation"
  maintenance: "Code and documentation maintenance"
  alignment: "Documentation-code synchronization"
  planning: "Project planning and execution"
  git: "Git and version control operations"
  tracking: "Status and progress tracking"
  identifier: "ID systems and patterns"
  relationship: "Cross-reference and mapping"
  configuration: "Settings and configuration"
  templating: "Template system and processing"
  requirement: "Critical requirements and constraints"
  validation: "Validation and verification"
  mapping: "ID and relationship mapping"
  approach: "Methodological approaches"
  threshold: "Quality and performance thresholds"
  format: "Standard formats and conventions"
  convention: "Naming and organizational conventions"
  standards: "Development standards and rules"
  capability: "Framework capabilities and features"
  technique: "Development techniques and methods"
  optimization: "Performance and efficiency optimizations"
  system: "System-level components and features"
  tool: "Utilities and development tools"
  location: "File and directory locations"
  command: "Executable commands and operations"
  operation: "Operational procedures and workflows"
  bootstrap: "Setup and initialization procedures"
```

---

*This YAML format provides structured, machine-readable access to all DDD framework terminology and commands. For human-readable format, see the original Markdown version.*
