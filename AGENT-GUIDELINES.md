# Documentation-Driven Development (DDD) for LLM Coding Agents

*"Write the docs, then write the code—keep it lean, test it for real."*

## Configuration

All Agent3D resources are accessed from `~/.agent3d`. This file (`~/.agent3d/AGENT-GUIDELINES.md`) is the main entry point for all operations.

**Project Configuration:** Each project uses `.agent3d-config.yml` in the project root to define project-specific settings, enabled passes, and quality standards.

## Project Root Detection

**CRITICAL**: Before starting any DDD work, establish the project root. See [DDD Procedures - Repository Management](procedures.yml/repository.yml#project-root-establishment) for complete instructions.

## Prime Directive

**Documentation leads, code follows.** Always update docs before implementing code. Documentation is the single source of truth.

## Core Workflow

| Phase | Action | Human Role |
|-------|--------|-----------|
| **Scan** | Detect missing/outdated docs | — |
| **Draft** | Create/update documentation | — |
| **Ask** | Clarify gaps and decisions | Provide input |
| **Sync** | Implement code matching docs | Review & approve |

**Project Setup**: Configure project with `.agent3d-config.yml` in project root
**DDD Pass**: Execute Scan → Draft → Ask → Sync → Confirm (if git_workflow.require_commit_confirmation=true), commit with `DDD: <description>`
**Getting Started**: New users can follow the [Quick Start Guide](docs/QUICK-START.md) for a short introduction.

### DDD Passes

- [Full Pass](~/.agent3d/passes.yml/full_pass.yml) - Comprehensive pass encompassing all aspects
- [0. Requirements Pass](~/.agent3d/passes.yml/0_requirements_pass.yml) - Documenting comprehensive requirements and business objectives
- [1. Foundation Pass](~/.agent3d/passes.yml/1_foundation_pass.yml) - Project configuration and foundational setup
- [2. Documentation Pass](~/.agent3d/passes.yml/2_documentation_pass.yml) - Documenting features, requirements, and priorities
- [3. Development Pass](~/.agent3d/passes.yml/3_development_pass.yml) - Step-by-step feature implementation with checkpoints and execution plans
- [4. Testing Pass](~/.agent3d/passes.yml/4_testing_pass.yml) - Adding comprehensive tests and verifying edge cases
- [5. Refactoring Pass](~/.agent3d/passes.yml/5_refactoring_pass.yml) - Cleaning up code without changing functionality
- [6. Code Review Pass](~/.agent3d/passes.yml/6_code_review_pass.yml) - Reviewing PR changes and providing feedback
- [7. Prune Pass](~/.agent3d/passes.yml/7_prune_pass.yml) - Removing outdated or redundant content
- [8. Synchronization Pass](~/.agent3d/passes.yml/8_synchronization_pass.yml) - Aligning documentation with code at any scale
- [9. Reverse Pass](~/.agent3d/passes.yml/9_reverse_pass.yml) - Detecting and addressing reverse drift (implementation without documentation)

---

## Development Principles

| Principle | Rule |
|-----------|------|
| **Requirements-Driven** | Implement only documented requirements from `docs/REQUIREMENTS.md` |
| **Lean Code** | Build only what is specified in requirements and acceptance criteria |
| **Real Tests** | **CRITICAL**: Tests MUST import and call actual project code - never test only mock data |
| **Project Code Testing** | **CRITICAL**: Every test must import from project source and call project functions |
| **Integration Focus** | Prefer integration tests over pure unit tests; avoid mocks except for external APIs |
| **Judicious Testing** | **CRITICAL**: Select test cases based on feature needs and risk - quality over quantity |
| **Full Traceability** | Link requirements (`REQ-####`) to features to test cases (`TC-####`) |
| **Requirements Validation** | Ensure all features trace back to business objectives |
| **Fast Feedback** | Run critical tests in CI |
| **Language Rules** | Fetch and memorize language-specific rules from links below, apply consistently |
| **LLM-Friendly Docs** | Use clear, concise language; consistent structure; no legacy references |



---

## Required Documentation

| File | Purpose | Local Template Path |
|------|---------|----------|
| `README.md` | Project overview | `~/.agent3d/templates/README.template.md` |
| `docs/BUSINESS-OBJECTIVES.md` | Business goals, metrics, and success criteria | `~/.agent3d/templates/BUSINESS-OBJECTIVES.template.md` |
| `docs/REQUIREMENTS.md` | Comprehensive functional and non-functional requirements | `~/.agent3d/templates/REQUIREMENTS.template.md` |
| `docs/USER-STORIES.md` | User personas, stories, and use cases | `~/.agent3d/templates/USER-STORIES.template.md` |
| `docs/ACCEPTANCE-CRITERIA.md` | Testable acceptance criteria for all requirements | `~/.agent3d/templates/ACCEPTANCE-CRITERIA.template.md` |
| `docs/FEATURES.md` | Feature checklist with acceptance criteria | `~/.agent3d/templates/FEATURES.template.md` |
| `docs/HIGH-LEVEL-DESIGN.md` | System design with diagrams and decisions | `~/.agent3d/templates/HIGH-LEVEL-DESIGN.template.md` |
| `docs/TASKS.md` | Work backlog organized by priority | `~/.agent3d/templates/TASKS.template.md` |
| `docs/TEST-CASES.md` | Test specifications with TC-#### format | `~/.agent3d/templates/TEST-CASES.template.md` |
| `docs/DDD-STATUS.yml` | DDD Pass Status, Drift and Health tracking | `~/.agent3d/templates/DDD-STATUS.template.yml` |
| `docs/designs/*.md` | Component design specifications | `~/.agent3d/templates/DETAILED-DESIGN.template.md` |
| `docs/proposals/*.md` | Design proposals for unimplemented features | `~/.agent3d/templates/PROPOSAL.template.md` |
| `docs/migrations/*.yml` | Migration workflows and execution tracking | `~/.agent3d/docs/migrations/` |
| `docs/ux/*.md` | UI/UX specifications, wireframes, and user flows (for UI projects) | `~/.agent3d/templates/UX-SPECIFICATIONS.template.md` |
| `CHANGELOG.md` | Chronological record of all project changes | `~/.agent3d/templates/CHANGELOG.template.md` |

**🚨 CRITICAL**: All documentation creation and standards are defined in [DDD Procedures](procedures.yml/). Follow these procedures for all DDD activities.

---

## Operational Standards

**Documentation-Code Alignment:**

- Each commit must update documentation OR include `docs-n/a` tag
- **MEMORIZE ENTIRE .agent3d-config.yml** at session start, refresh when config updated
- **Use memorized git_workflow settings** for commit confirmation behavior
- CI/CD pipelines must validate documentation-code alignment
- Agents must reject tasks that violate DDD principles

**All procedures in [DDD Procedures](procedures.yml/):**

- Repository management, templates, documentation standards
- Feature completion, progress tracking, status updates

## Agent Instructions

**Workflow:**

1. **Create Mental Memory Map:** Build comprehensive understanding of Agent3D framework
2. **Check Migration Status:** Run `python tools/migration_manager.py status` to identify applicable migrations
3. **Execute Required Migrations:** Apply any pending migrations before proceeding with development
4. Configure project (`.agent3d-config.yml` in project root)
5. Follow `~/.agent3d/AGENT-GUIDELINES.md`
6. Run DDD pass for missing/outdated documentation
7. **Write Real Tests:** Every test MUST import project code and call project functions
8. **Update Guidelines Regularly:** Run `git -C ~/.agent3d pull origin main` to keep cached rules and templates current
9. **Use System Date Commands:** Always use `date +%Y-%m-%d` or `date +%Y-%m-%d\ %H:%M:%S` for timestamps instead of LLM knowledge

**Test Quality Requirements:**

**CRITICAL**: All tests must meet these quality standards:

1. **Import Project Code**: Every test file MUST import modules/classes/functions from actual project source directories (parent/subdirectories checked into git)
2. **Call Project Functions**: Tests MUST call actual project functions from imported modules, not just assert against hardcoded values
3. **Meaningful Assertions**: Tests MUST validate actual behavior, not trivial comparisons like `assert 1 == 1`
4. **Integration Focus**: Prefer testing real data flows over pure mock scenarios
5. **TC ID Mapping**: Include TC-NNNN identifier in test function name or docstring for traceability
6. **FT-TC Validation**: **CRITICAL** - When TC is linked to an FT, the test MUST actually use and validate that specific feature functionality
7. **Appropriate TC Description Length**: **CRITICAL** - Keep TC descriptions as short as possible when linked features provide sufficient detail for LLM understanding. Add detailed descriptions only when features lack clarity

**Prohibited Test Patterns:**
- Tests that only use mock data without calling actual project code from git-tracked directories
- Tests that only assert against hardcoded expected values without importing project modules
- Tests that import only test libraries (pytest, unittest, mock) without importing from project source directories
- Tests with trivial assertions like `assert True` or `assert "expected" == "expected"`
- Tests that don't import any modules from the actual project codebase (parent/subdirectories in git)
- Tests that use try-except blocks around imports (let import failures cause test failures)
- Tests linked to an FT that don't actually use or validate the specific feature functionality

**Mental Memory Map Creation:**

- **CRITICAL**: Before starting any work, create a comprehensive mental map of the Agent3D framework and project structure
- **Framework Understanding**: Map out DDD passes, their relationships, and when to use each
- **Project Context**: Understand project type, configuration, enabled passes, and documentation structure
- **Resource Mapping**: Know locations of templates, rules, procedures, and key documentation
- **Workflow Integration**: Understand how framework components work together for effective project execution

**Question Protocol:**

- **CRITICAL**: When asking user questions, ask ONE question at a time
- Wait for user response before asking the next question
- Do not present multiple questions in a single interaction
- This applies to all passes, especially Foundation Pass configuration

## LLM Memory Optimization Framework

### Core Memory Map (MEMORIZE)

**CRITICAL:** Internalize these patterns to avoid file lookups during execution

| Component | Pattern |
|-----------|---------|
| **Execution** | SCAN → DRAFT → ASK → SYNC |
| **Sequence** | REQ → FOUND → DOC → PLAN → IMPL → TEST → REFACT → REVIEW → SYNC → QUAL → PRUNE → REV |
| **Files** | CONFIG(.agent3d-config.yml), DOCS(docs/), RULES(~/.agent3d/rules/), TEMPLATES(~/.agent3d/templates/) |
| **Quality Gates** | Requirements(objectives), Foundation(config), Documentation(criteria), Planning(checkpoints), Implementation(matches), Testing(passes), Review(rules) |

**DETAILED PROCEDURES:** See [DDD Procedures](procedures.yml/) for all standards and workflows

### Speed Optimization (MEMORIZE)

**CONFIGURATION STRUCTURE:**

```yaml
project: {type, language, quality_level}
enabled_passes: [list]
pass_config: {specific settings}
```

**STATUS PATTERNS:** `[x]` = Complete, `[~]` = In progress, `[ ]` = Not started

**LANGUAGE SHORTCUTS:** See [DDD Procedures - Language Rules](procedures.yml/language-rules.yml#language-specific-rules-speed-optimized)

**EXECUTION RULES:**

- **NEVER** look up pass definitions during execution
- **CACHE** language rules in working memory
- **MINIMIZE** template/rule file access
- **FIRST** check .agent3d-config.yml, **THEN** target documents

**DECISION TREE:** Missing requirements→Requirements Pass, No config→Foundation Pass, Features unclear→Documentation Pass, etc.

**References:**

- [DDD Procedures](procedures.yml/) - All standards and procedures
- [Advanced Features Guide](docs/ADVANCED-FEATURES.md) - Sophisticated capabilities and power-user features
- [Configuration Guide](docs/CONFIGURATION-GUIDE.md) - Customization and project-specific settings
- `~/.agent3d/rules/[language].md` - Language-specific rules
- `~/.agent3d/templates/` - Documentation templates
