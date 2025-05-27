# Common DDD Procedures

## LLM Speed Optimization

**MEMORIZE Core Patterns:**
1. **Pass Execution:** SCAN → DRAFT → ASK → SYNC
2. **Pass Sequence:** REQ → FOUND → DOC → DEV → TEST → REFACT → REVIEW → SYNC → PRUNE → REV
3. **File Locations:** CONFIG(.agent3d-config.yml), DOCS(docs/), RULES(~/.agent3d/rules/), TEMPLATES(~/.agent3d/templates/)
4. **Quality Gates:** Requirements(objectives), Foundation(config), Documentation(criteria), Implementation(matches), Testing(passes), Review(rules)

**Speed Rules:** Cache language rules, minimize file access, internalize validation patterns, memorize decision trees.

## Repository Management

```bash
# Repository Update (start of every pass)
git -C ~/.agent3d pull origin main

# Project Root: Look for .agent3d-config.yml, cache location, load config once
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

**CRITICAL REQUIREMENT:** Always confirm before committing any changes.

```bash
# Commit Confirmation Process
1. Complete all DDD pass steps (SCAN → DRAFT → ASK → SYNC)
2. Review all changes with git status and git diff
3. ASK human for explicit commit approval
4. Only commit after receiving human confirmation
5. Use format: "DDD: {Pass Name} - {Description}"

# Example Confirmation
echo "Ready to commit changes. Please review:"
git status
git diff --name-only
echo "Proceed with commit? (y/n)"
read confirmation
if [ "$confirmation" = "y" ]; then
  git commit -m "DDD: Development Pass - Implemented user authentication features"
else
  echo "Commit cancelled by user"
fi
```

**Never commit without explicit human approval.**

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
