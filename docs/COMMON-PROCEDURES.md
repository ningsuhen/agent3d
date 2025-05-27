# Common DDD Procedures

## LLM Speed Optimization

**MEMORIZE Core Patterns:**
1. **Pass Execution:** SCAN → DRAFT → ASK → SYNC → CONFIRM (if required by config)
2. **Pass Sequence:** REQ → FOUND → DOC → DEV → TEST → REFACT → REVIEW → SYNC → PRUNE → REV
3. **File Locations:** CONFIG(.agent3d-config.yml), DOCS(docs/), RULES(~/.agent3d/rules/), TEMPLATES(~/.agent3d/templates/)
4. **Quality Gates:** Requirements(objectives), Foundation(config), Documentation(criteria), Implementation(matches), Testing(passes), Review(rules)
5. **COMPLETE CONFIG:** ALWAYS load and memorize ENTIRE .agent3d-config.yml at session start

**Speed Rules:** Cache language rules, minimize file access, internalize validation patterns, memorize decision trees, **MEMORIZE ENTIRE .agent3d-config.yml**.

## Configuration Memorization (CRITICAL)

**STEP 1: ALWAYS MEMORIZE ENTIRE .agent3d-config.yml AT SESSION START**

```bash
# Configuration Loading Process (MEMORIZE THIS PATTERN)
1. git -C ~/.agent3d pull origin main
2. Locate .agent3d-config.yml in project root
3. LOAD AND MEMORIZE ENTIRE configuration file contents
4. Cache ALL settings in working memory for session duration
5. Apply memorized config throughout all passes

# MEMORIZE ALL THESE SECTIONS:
# - project: {name, type, description, language, quality_level}
# - enabled_passes: [list of enabled passes]
# - disabled_passes: [list of disabled passes]
# - pass_config: {pass-specific configurations}
# - git_workflow: {commit confirmation settings}
# - validation: {validation mode and rules}
# - documentation: {format and standards}
# - quality_gates: {thresholds and weights}
# - template_overrides: {custom template paths}
# - language_config: {language-specific settings}
```

**MEMORIZATION RULES:**
- Load config ONCE per session, use from memory thereafter
- NEVER re-read .agent3d-config.yml during pass execution
- Apply memorized settings consistently across all operations
- Check memorized config before every major decision (commits, pass selection, validation)
- **CRITICAL:** When config is updated, IMMEDIATELY refresh memory with new config

**CONFIG UPDATE PROTOCOL:**
```bash
# When .agent3d-config.yml is modified:
1. Save changes to .agent3d-config.yml
2. IMMEDIATELY re-load and memorize ENTIRE updated configuration
3. Replace old memorized config with new config in working memory
4. Apply new memorized config to all subsequent operations
5. Verify memory update by checking key settings (git_workflow, enabled_passes, etc.)
```

## Repository Management

```bash
# Repository Update (start of every pass)
git -C ~/.agent3d pull origin main

# Project Root: Look for .agent3d-config.yml, MEMORIZE entire config, cache location
# If no config: Run Foundation Pass immediately
```

## Templates & Workflow

```bash
# Template Usage: ~/.agent3d/templates/{DOCUMENT-NAME}.template.md
# Process: git pull → access templates → replace {{placeholders}} → remove template tags → validate
```

## DDD Workflow

**Process:** SCAN → DRAFT → ASK → SYNC → **CONFIRM BEFORE COMMIT** (mark steps with ✅)

**Standards:**
- Structure: `## Groups` / `### Sub-Groups`, single-line entries, 2-space indentation
- Completion: Mark `[x]` only with verifiable evidence, `[~]` for in-progress
- Templates: Replace ALL {{placeholders}}, remove `<template>` tags
- Quality: Functional links, LLM-friendly language, requirements-to-features-to-tests traceability
- Code: Exception handling, memory efficiency, test coverage, security, performance, documentation, zero technical debt

**Validation Checklist:**
- [ ] `## Groups` / `### Sub-Groups` structure
- [ ] {{placeholders}} replaced, template tags removed
- [ ] Functional links, single-line entries
- [ ] `[x]` only with verifiable evidence
- [ ] 2-space indentation, LLM-friendly language, traceability links

## Language Rules (MEMORIZE)

| Language | Key Patterns |
|----------|-------------|
| **Markdown** | LLM compression, command-first, no verbose explanations |
| **Python** | Type hints, docstrings, pytest, pyproject.toml, black formatting |
| **JavaScript** | ESLint, TypeScript preferred, Jest testing, modern ES6+ |
| **Java** | Spring patterns, JUnit, Maven/Gradle, SOLID principles |
| **Go** | gofmt, standard library preferred, table tests, idioms |

**Speed:** Cache on first use, apply from memory, no repeated lookups.

## Git Workflow & Commit Confirmation

**CRITICAL REQUIREMENT:** Use memorized git_workflow configuration for all commit operations.

### Execution Plan Branch Workflow (USE MEMORIZED CONFIG)
```bash
# STEP 1: Check current branch and memorized exec_plan_branches config
CURRENT_BRANCH=$(git branch --show-current)
EXEC_PLAN_ENABLED=$(MEMORIZED_CONFIG.git_workflow.exec_plan_branches.enabled)

# STEP 2: Apply branch-specific commit behavior
if [[ "$CURRENT_BRANCH" == exec-plan/* ]] && [[ "$EXEC_PLAN_ENABLED" == "true" ]]; then
  # ON EXECUTION PLAN BRANCH: Auto-commit allowed during execution
  git add .
  git commit -m "EXEC: Step {step_number} - {step_description}"

  # Tag checkpoints
  if [[ "$IS_CHECKPOINT" == "true" ]]; then
    git tag "checkpoint-{checkpoint_number}-$(date +%Y%m%d-%H%M%S)"
    git commit -m "CHECKPOINT: {checkpoint_number} - {checkpoint_description}"
  fi

elif [[ "$CURRENT_BRANCH" == exec-plan/* ]] && [[ "$ACTION" == "merge" ]]; then
  # MERGING EXECUTION PLAN: Require confirmation
  echo "Ready to merge exec plan branch to main. Please review:"
  git log --oneline main..HEAD
  echo "Proceed with merge? (y/n)"
  read confirmation
  if [ "$confirmation" = "y" ]; then
    git checkout main
    git merge "$CURRENT_BRANCH"
    git branch -d "$CURRENT_BRANCH"
  else
    echo "Merge cancelled by user"
  fi

else:
  # REGULAR BRANCH: Use standard confirmation behavior
  if MEMORIZED_CONFIG.git_workflow.require_commit_confirmation=true:
    echo "Ready to commit changes. Please review:"
    git status
    echo "Proceed with commit? (y/n)"
    read confirmation
    if [ "$confirmation" = "y" ]; then
      git commit -m "DDD: {Pass Name} - {Description}"
    fi
  else:
    git commit -m "DDD: {Pass Name} - {Description}"
  fi
fi
```

### Execution Plan Branch Examples
```bash
# Create execution plan branch
git checkout -b exec-plan/horizontal-compression-pass

# During execution: Auto-commit steps
git add .
git commit -m "EXEC: Step 1 - Compress Configuration Guide"
git commit -m "EXEC: Step 2 - Compress GitHub CLI Integration"

# Tag checkpoints
git tag "checkpoint-1-20250127-1430"
git commit -m "CHECKPOINT: 1 - Core Documentation Compressed"

# Complete execution and merge (requires confirmation)
git checkout main
echo "Ready to merge exec-plan/horizontal-compression-pass. Proceed? (y/n)"
git merge exec-plan/horizontal-compression-pass
git branch -d exec-plan/horizontal-compression-pass
```

### Configuration Examples (MEMORIZE THESE PATTERNS)
- **Exec Plan Branch** (exec-plan/*): Auto-commit during execution, confirm for merge
- **Regular Branch** (main, feature/*): Use standard confirmation behavior
- **Strict Mode** (require_commit_confirmation=true): Always ask human before committing
- **Automated Mode** (require_commit_confirmation=false): Auto-commit allowed

**MEMORIZATION RULE:** Use memorized config throughout session, check branch type for commit behavior.

## Pass Configuration Examples

### Foundation Pass Configuration
```yaml
foundation_pass:
  enabled: true
  templates: [README.template.md, FEATURES.template.md, HIGH-LEVEL-DESIGN.template.md]
  validation: strict
```

### Development Pass Configuration
```yaml
development_pass:
  enabled: true
  selection_mode: "auto"  # "auto" | "picker"
  runs_directory: "docs/runs/"
  auto_selection: {priority_threshold: "high", max_features_per_run: 3, include_drift_fixes: true, include_blockers: true, respect_dependencies: true, max_estimated_effort: "3 days"}
  execution_settings: {checkpoint_frequency: 3, auto_test_after_step: true, archive_completed_plans: true}
  auto_trigger_thresholds: {file_count: 3, estimated_effort_hours: 8, risk_level: "medium", complexity: "high"}
  required_for: [migrations, refactoring, breaking_changes]
  optional_for: [bug_fixes, documentation]
```

### Planning Pass Configuration
```yaml
planning_pass:
  enabled: true
  auto_trigger_thresholds:
    file_count: 3
    estimated_effort_hours: 8
    risk_level: "medium"
    complexity: "high"
  required_for: [migrations, refactoring, breaking_changes]
  optional_for: [bug_fixes, documentation]
  checkpoint_frequency: 3  # steps between checkpoints
```

### Testing Pass Configuration
```yaml
testing_pass:
  enabled: true
  coverage_threshold: 80
  test_types: [unit, integration, edge_cases]
  framework_compliance: strict
```

### Project Type Examples
```yaml
# Web Application Example
project:
  type: "web_application"
  language: "python"
  framework: "django"
  quality_level: "balanced"
enabled_passes: [foundation, requirements, documentation, planning, implementation, testing, code_review, synchronization, quality]
skip_passes: [prune, reverse]

# Documentation Project Example
project:
  type: "documentation"
  language: "markdown"
  quality_level: "strict"
enabled_passes: [foundation, requirements, documentation, quality]
skip_passes: [planning, implementation, testing, code_review, refactoring]
```

## Planning & Status

```bash
# Implementation Plans: docs/plans/IMPLEMENTATION-PLAN-{feature-name}.md
# Lifecycle: Creation → Validation → Execution → Completion → Archive
# Checkpoints: Every 2-4 steps, mark [x] completed, [~] in progress, [ ] not started
# Triggers: >3 components, >8 hours, Medium/High risk, external dependencies, breaking changes

# DDD Status: docs/DDD-STATUS.md (after each pass)
# Elements: Pass Status (✅⏸️🔄⏭️), Alignment (0-100%), Drift (🟢🟡🟠🔴), Health Indicators
```

## Directory Structure

```
docs/                    # Main documentation
├── designs/            # Component specifications
├── proposals/          # Unimplemented features
├── plans/             # Implementation plans
└── ux/                # UI/UX specs (UI projects)
passes/simplified/      # Pass documentation
templates/             # Document templates
rules/                # Language rules
```

## Quality & GitHub

**Quality:** Simple language, complete coverage, consistent patterns, requirements→features→tests traceability, current docs.
**Validation:** Functional links, no template tags, consistent formatting, complete placeholders, proper hierarchy.
**GitHub:** See [GitHub CLI Integration Guide](GITHUB-CLI-INTEGRATION.md) - automated PR detection, pending reviews, human-agent workflow.

---

**Usage:** Reference from all DDD passes for consistency.
