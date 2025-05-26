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

### DDD Passes

- [Full Pass](~/.agent3d/passes/simplified/full_pass.md) - Comprehensive pass encompassing all aspects
- [0. Requirements Pass](~/.agent3d/passes/simplified/0_requirements_pass.md) - Documenting comprehensive requirements and business objectives
- [1. Foundation Pass](~/.agent3d/passes/simplified/1_foundation_pass.md) - Project configuration and foundational setup
- [2. Documentation Pass](~/.agent3d/passes/simplified/2_documentation_pass.md) - Documenting features, requirements, and priorities
- [3. Implementation Pass](~/.agent3d/passes/simplified/3_implementation_pass.md) - Implementing features with basic test coverage
- [4. Testing Pass](~/.agent3d/passes/simplified/4_testing_pass.md) - Adding comprehensive tests and verifying edge cases
- [5. Refactoring Pass](~/.agent3d/passes/simplified/5_refactoring_pass.md) - Cleaning up code without changing functionality
- [6. Code Review Pass](~/.agent3d/passes/simplified/6_code_review_pass.md) - Reviewing PR changes and providing feedback
- [7. Synchronization Pass](~/.agent3d/passes/simplified/7_synchronization_pass.md) - Aligning documentation with code at any scale
- [8. Quality Pass](~/.agent3d/passes/simplified/8_quality_pass.md) - Verifying and improving documentation quality
- [9. Prune Pass](~/.agent3d/passes/simplified/9_prune_pass.md) - Removing outdated or redundant content
- [10. Reverse Pass](~/.agent3d/passes/simplified/10_reverse_pass.md) - Detecting and addressing reverse drift (implementation without documentation)

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
| `CHANGELOG.md` | Chronological record of all project changes | `~/.agent3d/templates/CHANGELOG.template.md` |

**🚨 CRITICAL**: All documentation creation and standards are defined in [Common Procedures](docs/COMMON-PROCEDURES.md). Follow these procedures for all DDD activities.

---

## Operational Standards

**Documentation-Code Alignment:**
- Each commit must update documentation OR include `docs-n/a` tag
- CI/CD pipelines must validate documentation-code alignment
- Agents must reject tasks that violate DDD principles

**All procedures defined in [Common Procedures](docs/COMMON-PROCEDURES.md):**
- Repository management, template usage, documentation standards
- Feature completion criteria, progress tracking, status updates

## Agent Instructions

**Workflow:**
1. **Create Mental Memory Map:** Build comprehensive understanding of Agent3D framework and project structure
2. Configure project (`.agent3d-config.yml` file in project root)
3. Follow `~/.agent3d/AGENT-GUIDELINES.md` (this file)
4. Run DDD pass for missing/outdated documentation
5. Favor integration tests over mocks

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

### Core Memory Map (Memorize These)
**CRITICAL: Internalize these patterns to avoid file lookups during execution**

**1. Pass Execution Pattern (Universal):**
```
SCAN → DRAFT → ASK → SYNC
```

**2. Pass Sequence (0-10):**
```
REQ → FOUND → DOC → IMPL → TEST → REFACT → REVIEW → SYNC → QUAL → PRUNE → REV
```

**3. File Locations (Memorize):**
```
CONFIG: .agent3d-config.yml (project root)
DOCS: docs/REQUIREMENTS.md, docs/FEATURES.md, docs/TASKS.md, docs/DDD-STATUS.md
RULES: ~/.agent3d/rules/[language].md
TEMPLATES: ~/.agent3d/templates/[document].template.md
```

**4. Pass Relationships (Memorize):**
- **Sequential**: REQ→FOUND→DOC→IMPL (must follow order)
- **Iterative**: TEST↔REFACT↔REVIEW (can repeat)
- **Maintenance**: SYNC→QUAL→PRUNE→REV (cleanup cycle)

**5. Quality Gates (Memorize):**
- Requirements: Business objectives documented
- Foundation: Configuration complete
- Documentation: Features with acceptance criteria
- Implementation: Code matches documentation
- Testing: All tests pass
- Review: Language rules enforced

### Speed Optimization Patterns (Memorize)

**1. Configuration Quick Check:**
```yaml
# .agent3d-config.yml structure (memorize)
project: {type, language, quality_level}
enabled_passes: [list]
pass_config: {specific settings}
```

**2. Document Status Patterns:**
```
[x] = Complete with evidence
[~] = In progress
[ ] = Not started
```

**3. Language Rule Shortcuts:**
- **Markdown**: LLM compression, command-first, no verbose explanations
- **Python**: Type hints, docstrings, pytest, black formatting
- **JavaScript**: ESLint, TypeScript preferred, Jest testing
- **Java**: Spring patterns, JUnit, Maven/Gradle
- **Go**: gofmt, standard library preferred, table tests

### Execution Speed Optimizations

**1. Memory-First Approach:**
- **NEVER** look up pass definitions during execution
- **MEMORIZE** SCAN→DRAFT→ASK→SYNC pattern
- **INTERNALIZE** quality gates and completion criteria
- **CACHE** language rules in working memory

**2. File Access Patterns (Minimize Lookups):**
```
FIRST: Check .agent3d-config.yml (project context)
THEN: Read target documents (REQUIREMENTS.md, FEATURES.md, etc.)
AVOID: Repeated template/rule file access
CACHE: Language-specific patterns in memory
```

**3. Decision Trees (Memorize):**
```
Pass Selection:
- Missing requirements? → Requirements Pass
- No config? → Foundation Pass
- Features unclear? → Documentation Pass
- Code needed? → Implementation Pass
- Tests failing? → Testing Pass
- Code messy? → Refactoring Pass
- Quality issues? → Code Review Pass
```

**4. Quick Validation Patterns:**
```
Requirements: Business objectives exist?
Foundation: .agent3d-config.yml complete?
Documentation: Features have acceptance criteria?
Implementation: Code matches docs?
Testing: All tests pass?
Review: Language rules followed?
```

**References:**
- [Common Procedures](docs/COMMON-PROCEDURES.md) - All standards and procedures
- [Advanced Features Guide](docs/ADVANCED-FEATURES.md) - Sophisticated capabilities and power-user features
- [Configuration Guide](docs/CONFIGURATION-GUIDE.md) - Customization and project-specific settings
- `~/.agent3d/rules/[language].md` - Language-specific rules
- `~/.agent3d/templates/` - Documentation templates