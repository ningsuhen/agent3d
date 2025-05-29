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
- **TC ID Mapping:** All test implementations MUST include TC-NNNN references for 1:1 traceability

**Validation Checklist:**
- [ ] `## Groups` / `### Sub-Groups` structure
- [ ] {{placeholders}} replaced, template tags removed
- [ ] Functional links, single-line entries
- [ ] `[x]` only with verifiable evidence
- [ ] 2-space indentation, LLM-friendly language, traceability links
- [ ] **TC ID drift <10%** (run `python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping`)

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

## Date and Timestamp Standards

**CRITICAL**: Always use system commands for dates, never LLM knowledge.

```bash
# Standard Date Formats
date +%Y-%m-%d                    # 2024-01-27 (for creation_date, last_updated)
date +%Y-%m-%d\ %H:%M:%S         # 2024-01-27 14:30:45 (for detailed timestamps)
date +%Y-%m-%d\ %H:%M            # 2024-01-27 14:30 (for progress tracking)

# Usage Examples
echo "Last updated: $(date +%Y-%m-%d)"
echo "Generated on: $(date +%Y-%m-%d\ %H:%M:%S)"
```

**Template Usage:**
- Replace `{{creation_date}}` with output of `date +%Y-%m-%d`
- Replace `{{last_updated}}` with output of `date +%Y-%m-%d`
- Replace `[USE: date +%Y-%m-%d]` with actual command output
- Never use hardcoded dates or LLM knowledge for timestamps

## Pass Configuration

All pass configurations are defined in `.agent3d-config.yml`. Key settings include enabled passes, pass-specific focus areas, and quality thresholds.

## Planning & Status

```bash
# Execution Plans: docs/runs/EXEC-PLAN-{change-name}.md
# Lifecycle: Creation → Validation → Execution → Completion
# Checkpoints: Every 2-4 steps, mark [x] completed, [~] in progress, [ ] not started
# Triggers: Feature implementation, refactoring, migrations, complex changes

# DDD Status: docs/DDD-STATUS.md (after each pass)
# Elements: Pass Status (✅⏸️🔄⏭️), Alignment (0-100%), Drift (🟢🟡🟠🔴), Health Indicators
```

## Directory Structure

```
docs/                    # Main documentation
├── designs/            # Component specifications
├── proposals/          # Unimplemented features
├── runs/              # Development execution plans
└── ux/                # UI/UX specs (UI projects)
passes/simplified/      # Pass documentation
templates/             # Document templates
rules/                # Language rules
```

## Quality & GitHub

**Quality:** Simple language, complete coverage, consistent patterns, requirements→features→tests traceability, current docs.
**Validation:** Functional links, no template tags, consistent formatting, complete placeholders, proper hierarchy.
**GitHub:** See [GitHub CLI Integration Guide](GITHUB-CLI-INTEGRATION.md) - automated PR detection, pending reviews, human-agent workflow.

## Drift Scanning

**Comprehensive drift detection tool for Agent3D framework with multiple analysis modes.**

### Overview

The Multi-Mode Drift Scanner analyzes various types of drift between documentation and implementation across multiple programming languages.

**Analysis Modes:**
- **tc-mapping** - TC ID mapping between TEST-CASES.md and test implementations
- **ft-mapping** - FT ID mapping between FEATURES.md and test implementations
- **ft-tc-mapping** - FT-TC relationship mapping and cross-reference validation
- **code-coverage** - Test coverage analysis and missing test detection
- **feature-impl** - Feature implementation status drift between FEATURES.md and code
- **test-quality** - Test quality validation ensuring tests import and call actual project code
- **all** - Comprehensive analysis running all drift detection modes

**Drift Types Detected:**
- **TC ID Mapping Drift:** Test cases without implementations, implementations without TC IDs, orphaned TC IDs
- **FT ID Mapping Drift:** Features without test coverage, tests without feature references, orphaned FT IDs
- **FT-TC Relationship Drift:** Missing FT-TC cross-references, broken relationships, inconsistent mappings
- **Code Coverage Drift:** Missing test files, untested functions, orphaned tests, coverage metrics
- **Feature Implementation Drift:** Status mismatches, missing implementations, undocumented features
- **Test Quality Drift:** Tests without project imports, tests without function calls, mock-only tests, weak assertions

**Supported Languages:** Python, JavaScript/TypeScript, Java, Go, Rust

### Tool Options

**Direct Tool:** `python3 ~/.agent3d/tools/drift_scanner.py` - Run from DDD project root directory. Requires manual path management and working directory setup.

**MCP Server:** `~/.agent3d/tools/drift_scanner_mcp_server.sh` - Full MCP server implementation for client integration with virtual environment support and DDD_ROOT environment variable.

### Usage

**Prerequisites:** Must be run from DDD project root directory (where `.agent3d-config.yaml` is located).

**Basic Usage:**
```bash
# Navigate to your DDD project root first
cd /path/to/your/ddd-project

# TC ID mapping analysis (default)
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping

# FT ID mapping analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode ft-mapping

# FT-TC relationship mapping analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode ft-tc-mapping

# Code coverage analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode code-coverage

# Feature implementation analysis
python3 ~/.agent3d/tools/drift_scanner.py --mode feature-impl

# Test quality validation
python3 ~/.agent3d/tools/drift_scanner.py --mode test-quality

# Comprehensive analysis (all modes)
python3 ~/.agent3d/tools/drift_scanner.py --mode all

# Quiet mode for CI/CD integration
python3 ~/.agent3d/tools/drift_scanner.py --quiet
```

**Change-Based Scanning (Fast Mode):**
```bash
# Only scan files changed since last commit (10x+ faster)
python3 ~/.agent3d/tools/drift_scanner.py --mode all --changed-only

# Only scan files changed since specific branch/commit
python3 ~/.agent3d/tools/drift_scanner.py --mode tc-mapping --changed-since main
python3 ~/.agent3d/tools/drift_scanner.py --mode all --changed-since HEAD~5

# PR-focused scanning (changed vs main branch)
python3 ~/.agent3d/tools/drift_scanner.py --mode all --pr-diff

# Recent changes (last N days)
python3 ~/.agent3d/tools/drift_scanner.py --mode all --recent-days 7

# Combine with quiet mode for fast CI/CD
python3 ~/.agent3d/tools/drift_scanner.py --mode all --changed-only --quiet
```

**MCP Server Configuration:**
```json
{
  "mcpServers": {
    "agent3d-drift-scanner": {
      "command": "/Users/nwaikhom/.agent3d/tools/drift_scanner_mcp_server.sh",
      "args": [],
      "env": {
        "DDD_ROOT": "/path/to/your/ddd-project",
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### Output & Integration

**Exit Codes:**
- `0` - Low drift (<10%) - Excellent TC ID mapping
- `1` - Moderate drift (10-25%) - Some cleanup recommended
- `2` - High drift (>25%) - Significant issues requiring attention

**Output Location:** Reports generated in `.agent3d-tmp/drift-reports/` with consistent naming:
- `tc-mapping-drift-report.yaml`
- `ft-mapping-drift-report.yaml`
- `ft-tc-mapping-drift-report.yaml`
- `code-coverage-drift-report.yaml`
- `feature-impl-drift-report.yaml`
- `test-quality-drift-report.yaml`
- `all-drift-report.yaml`

**DDD Output Principle:** All drift scanner outputs MUST be placed in `.agent3d-tmp/` directory, even when custom output paths are specified. Custom paths are automatically prefixed with `.agent3d-tmp/drift-reports/` to maintain DDD standards.

**DDD Pass Integration:**
```bash
# Foundation Pass - Validate identifier patterns configuration
echo "🔍 Validating identifier patterns configuration..."
python3 ~/.agent3d/tools/drift_scanner.py --mode ft-tc-mapping --quiet

# Testing Pass - Fast TC ID mapping, test quality, and code coverage (change-based)
echo "🔍 Checking TC ID drift, test quality, and code coverage (changed files only)..."
python3 ~/.agent3d/tools/drift_scanner.py --mode all --changed-only --quiet
DRIFT_LEVEL=$?
if [ $DRIFT_LEVEL -eq 2 ]; then
    echo "❌ HIGH DRIFT: Must fix drift issues before proceeding"
    exit 1
fi

# Test Quality Pass - Validate tests actually test project code
echo "🔍 Validating test quality (tests must import and call project code)..."
python3 ~/.agent3d/tools/drift_scanner.py --mode test-quality --quiet
QUALITY_LEVEL=$?
if [ $QUALITY_LEVEL -eq 2 ]; then
    echo "❌ POOR TEST QUALITY: Tests must import and call actual project code"
    exit 1
fi

# Synchronization Pass - comprehensive FT-TC relationship validation
echo "🔍 Comprehensive FT-TC relationship and drift analysis..."
python3 ~/.agent3d/tools/drift_scanner.py --mode all
echo "📄 Comprehensive drift report generated in .agent3d-tmp/drift-reports/"

# PR Review - only scan files in current PR
python3 ~/.agent3d/tools/drift_scanner.py --mode all --pr-diff --quiet

# Development workflow - FT-TC mapping for recent changes
python3 ~/.agent3d/tools/drift_scanner.py --mode ft-tc-mapping --recent-days 3 --quiet
```

**CI/CD Integration:**
```yaml
# GitHub Actions example - Fast PR validation
- name: Check TC ID Drift (PR Changes Only)
  run: |
    python3 ~/.agent3d/tools/drift_scanner.py --mode all --pr-diff --quiet
    if [ $? -eq 2 ]; then
      echo "❌ High drift detected in PR changes"
      exit 1
    fi

# Full validation on main branch
- name: Comprehensive Drift Check (Main Branch)
  if: github.ref == 'refs/heads/main'
  run: |
    python3 ~/.agent3d/tools/drift_scanner.py --mode all --quiet
```

**Identifier Pattern Recognition:**
- **TC IDs:** `TC-0001`, `TC-ENV-007`, `TC-0001a`, `TC-ABC-123b`
- **FT IDs:** `FT-CORE-001`, `FT-LANG-002a`, `FT-IMPL-005`

**Best Practices:**

- **TC ID Mapping:** Always include TC IDs in test function names or nearby comments
- **FT ID Mapping:** Reference FT IDs in test files and feature implementation comments
- **Cross-References:** Maintain FT-TC relationships in FEATURES.md and TEST-CASES.md
- **Naming Consistency:** Use `test_feature_tc_0001` format for TC mapping
- **One-to-One Mapping:** One TC ID per test function, clear FT-TC relationships
- **Appropriate TC Description Length:** **CRITICAL** - Keep TC descriptions as short as possible when linked features provide sufficient detail for LLM understanding. Add detailed descriptions only when features lack clarity
- **Test Quality:** **CRITICAL** - Every test MUST import project code and call project functions
- **Real Testing:** Tests must validate actual behavior, not just assert against hardcoded values
- **Integration Focus:** Prefer integration tests over pure mock scenarios
- **Pass Integration:** Run FT-TC mapping during Foundation and Synchronization passes
- **Performance:** Use `--changed-only` for fast development workflow (10x+ speed improvement)
- **CI/CD:** Use `--pr-diff` for efficient validation of pull requests
- **Comprehensive Analysis:** Reserve full scans for main branch validation and synchronization
- **Drift Thresholds:** Set appropriate thresholds for your project (recommend <10%)

---

**Usage:** Reference from all DDD passes for consistency.
