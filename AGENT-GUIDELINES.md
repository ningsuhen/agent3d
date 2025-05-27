# Documentation-Driven Development (DDD) for LLM Coding Agents
*"Write the docs, then write the code—keep it lean, test it for real."*

## Configuration

All Agent3D resources are accessed from `~/.agent3d`. This file (`~/.agent3d/AGENT-GUIDELINES.md`) is the main entry point for all operations.

**Project Configuration:** Each project uses `.agent3d-config.yml` in the project root to define project-specific settings, enabled passes, and quality standards.

## Project Root Detection
**CRITICAL**: Before starting any DDD work, establish the project root. See [Common Procedures - Project Root Establishment](docs/COMMON-PROCEDURES.md#project-root-establishment) for complete instructions.

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
**DDD Pass**: Execute Scan → Draft → Ask → Sync, then commit with `DDD: <description>`
**Getting Started**: New users can follow the [Quick Start Guide](docs/QUICK-START.md) for a short introduction.

### DDD Passes

- [Full Pass](~/.agent3d/passes/simplified/full_pass.md) - Comprehensive pass encompassing all aspects
- [0. Requirements Pass](~/.agent3d/passes/simplified/0_requirements_pass.md) - Documenting comprehensive requirements and business objectives
- [1. Foundation Pass](~/.agent3d/passes/simplified/1_foundation_pass.md) - Project configuration and foundational setup
- [2. Documentation Pass](~/.agent3d/passes/simplified/2_documentation_pass.md) - Documenting features, requirements, and priorities
- [3. Planning Pass](~/.agent3d/passes/simplified/3_planning_pass.md) - Creating step-by-step implementation plans with checkpoints for major changes
- [4. Implementation Pass](~/.agent3d/passes/simplified/4_implementation_pass.md) - Implementing features with basic test coverage
- [5. Testing Pass](~/.agent3d/passes/simplified/5_testing_pass.md) - Adding comprehensive tests and verifying edge cases
- [6. Refactoring Pass](~/.agent3d/passes/simplified/6_refactoring_pass.md) - Cleaning up code without changing functionality
- [7. Code Review Pass](~/.agent3d/passes/simplified/7_code_review_pass.md) - Reviewing PR changes and providing feedback
- [8. Synchronization Pass](~/.agent3d/passes/simplified/8_synchronization_pass.md) - Aligning documentation with code at any scale
- [9. Quality Pass](~/.agent3d/passes/simplified/9_quality_pass.md) - Verifying and improving documentation quality
- [10. Prune Pass](~/.agent3d/passes/simplified/10_prune_pass.md) - Removing outdated or redundant content
- [11. Reverse Pass](~/.agent3d/passes/simplified/11_reverse_pass.md) - Detecting and addressing reverse drift (implementation without documentation)

---

## Development Principles

| Principle | Rule |
|-----------|------|
| **Requirements-Driven** | Implement only documented requirements from `docs/REQUIREMENTS.md` |
| **Lean Code** | Build only what is specified in requirements and acceptance criteria |
| **Real Tests** | Use integration tests; avoid mocks except for external APIs |
| **Full Traceability** | Link requirements (`REQ-####`) to features to test cases (`TC-####`) |
| **Requirements Validation** | Ensure all features trace back to business objectives |
| **Fast Feedback** | Run critical tests in CI |
| **Language Rules** | Fetch and memorize language-specific rules from links below, apply consistently |
| **LLM-Friendly Docs** | Use clear, concise language; consistent structure; no legacy references |

### Language-Specific Rules

- [Markdown](~/.agent3d/rules/markdown.md) - Rules for Markdown documentation and LLM optimization
- [Python](~/.agent3d/rules/python.md) - Rules for Python development
- [JavaScript](~/.agent3d/rules/javascript.md) - Rules for JavaScript development
- [Java](~/.agent3d/rules/java.md) - Rules for Java development
- [Go](~/.agent3d/rules/go.md) - Rules for Go development

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
| `docs/DDD-STATUS.md` | DDD Pass Status, Drift and Health tracking | `~/.agent3d/templates/DDD-STATUS.template.md` |
| `docs/designs/*.md` | Component design specifications | `~/.agent3d/templates/DETAILED-DESIGN.template.md` |
| `docs/proposals/*.md` | Design proposals for unimplemented features | `~/.agent3d/templates/PROPOSAL.template.md` |
| `docs/plans/*.md` | Step-by-step implementation plans for major changes | `~/.agent3d/templates/IMPLEMENTATION-PLAN.template.md` |
| `docs/ux/*.md` | UI/UX specifications, wireframes, and user flows (for UI projects) | `~/.agent3d/templates/UX-SPECIFICATIONS.template.md` |
| `CHANGELOG.md` | Chronological record of all project changes | `~/.agent3d/templates/CHANGELOG.template.md` |

**🚨 CRITICAL**: All documentation creation and standards are defined in [Common Procedures](docs/COMMON-PROCEDURES.md). Follow these procedures for all DDD activities.

---

## Operational Standards

**Documentation-Code Alignment:**
- Each commit must update documentation OR include `docs-n/a` tag
- CI/CD pipelines must validate documentation-code alignment
- Agents must reject tasks that violate DDD principles

**All procedures in [Common Procedures](docs/COMMON-PROCEDURES.md):**
- Repository management, templates, documentation standards
- Feature completion, progress tracking, status updates

## Agent Instructions

**Workflow:**
1. **Create Mental Memory Map:** Build comprehensive understanding of Agent3D framework
2. Configure project (`.agent3d-config.yml` in project root)
3. Follow `~/.agent3d/AGENT-GUIDELINES.md`
4. Run DDD pass for missing/outdated documentation
5. Favor integration tests over mocks
6. **Update Guidelines Regularly:** Run `git -C ~/.agent3d pull origin main` to keep cached rules and templates current

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

**DETAILED PROCEDURES:** See [Common Procedures](docs/COMMON-PROCEDURES.md) for all standards and workflows

### Speed Optimization (MEMORIZE)

**CONFIGURATION STRUCTURE:**
```yaml
project: {type, language, quality_level}
enabled_passes: [list]
pass_config: {specific settings}
```

**STATUS PATTERNS:** `[x]` = Complete, `[~]` = In progress, `[ ]` = Not started

**LANGUAGE SHORTCUTS:** See [Common Procedures - Language Rules](docs/COMMON-PROCEDURES.md#language-specific-rules-speed-optimized)

**EXECUTION RULES:**
- **NEVER** look up pass definitions during execution
- **CACHE** language rules in working memory
- **MINIMIZE** template/rule file access
- **FIRST** check .agent3d-config.yml, **THEN** target documents

**DECISION TREE:** Missing requirements→Requirements Pass, No config→Foundation Pass, Features unclear→Documentation Pass, etc.

**References:**
- [Common Procedures](docs/COMMON-PROCEDURES.md) - All standards and procedures
- [Advanced Features Guide](docs/ADVANCED-FEATURES.md) - Sophisticated capabilities and power-user features
- [Configuration Guide](docs/CONFIGURATION-GUIDE.md) - Customization and project-specific settings
- `~/.agent3d/rules/[language].md` - Language-specific rules
- `~/.agent3d/templates/` - Documentation templates