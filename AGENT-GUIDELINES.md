# Documentation-Driven Development (DDD) for LLM Coding Agents
*"Write the docs, then write the code—keep it lean, test it for real."*

## Configuration
**AGENT3D_LOCAL_REPO**: `~/.agent3d` (Local clone of Agent3D repository)
**PROJECT_ROOT**: Determined by `.agent3d` file location or current working directory

*Note: All Agent3D resources are accessed from the local repository clone. Agents should clone `git@github.com:ningsuhen/agent3d.git` to `~/.agent3d` and update regularly with `git pull`.*

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

**Project Setup**: Establish project root by finding or creating `.agent3d` file
**DDD Pass**: Execute Scan → Draft → Ask → Sync, then commit with `DDD: <description>`

### DDD Passes

- [Full Pass](~/.agent3d/passes/simplified/full_pass.md) - Comprehensive pass encompassing all aspects
- [0. Requirements Pass](~/.agent3d/passes/simplified/0_requirements_pass.md) - Documenting comprehensive requirements and business objectives
- [1. Foundation Pass](~/.agent3d/passes/simplified/1_foundation_pass.md) - Creating foundational documentation and architecture
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

**Missing Documentation**: Always create complete content using the provided templates before coding. Templates contain format specifications, placeholder structures, and examples - do NOT include the `<template>` or `<example>` tags in actual documentation files.

**🚨 CRITICAL REQUIREMENTS:**
- **Common Procedures**: ALWAYS follow [Common Procedures](docs/COMMON-PROCEDURES.md) for repository management, project root establishment, and template usage.
- **Feature Completion**: NEVER mark features as `[x]` completed based solely on interface definitions, prototypes, or documentation. ONLY mark `[x]` when verifiable evidence exists (tests pass, manual verification).
- **Document Structure**: ALWAYS use `## Groups` and `### Sub-Groups` heading structure in all documentation.
- **Template Compliance**: Replace ALL {{placeholders}} with actual content and remove template tags.

---

## Documentation Enforcement
- Each commit must update documentation OR include `docs-n/a` tag
- CI/CD pipelines must validate documentation-code alignment
- Agents must reject tasks that violate DDD principles

## Task Formatting Guidelines

**For Documentation:**
- **Features**: Follow `~/.agent3d/templates/FEATURES.template.md` - must include acceptance criteria in `(Criteria: <...>)` format. Single-line entries only. Mark `[x]` ONLY with verifiable evidence.
- **Tasks**: Follow `~/.agent3d/templates/TASKS.template.md` - organize by priority levels (High/Medium/Low/Completed) with functional area sub-groups
- **Test Cases**: Follow `~/.agent3d/templates/TEST-CASES.template.md` - use TC-#### format with execution types (Manual/Automated/Partial) and priority
- **DDD Status**: Follow `~/.agent3d/templates/DDD-STATUS.template.md` - track alignment and drift metrics with health indicators

**CRITICAL - Documentation Structure:**
- **Use proper heading hierarchy**: `## Groups` and `### Sub-Groups` for organization
- **Group related items** within appropriate sections for easy identification and navigation

**CRITICAL - Feature Completion Criteria:**
- **NEVER mark features as `[x]` completed** based solely on interface definitions, prototypes, or documentation
- **ONLY mark features as `[x]` completed** when there is verifiable evidence the feature works properly:
  - Automated tests that pass and validate the feature functionality
  - Manual testing results that confirm the feature meets acceptance criteria
  - Demonstrable working implementation that fulfills the specified criteria
- **Use `[~]` for in-progress features** that have partial implementation but lack verification

**For Process Execution:**
- Use ✅ symbol to mark completed steps during DDD pass execution
- Add ✅ next to steps as you complete them for real-time progress tracking
- Update `docs/DDD-STATUS.md` after each pass with phase-specific alignment/drift
- Update `CHANGELOG.md` after significant changes or pass completions with appropriate categorization

## Agent Instructions
**FIRST**: Establish project root by finding or creating `.agent3d` file. Follow `.agent-guidelines.md`. When documentation is missing or outdated, run a DDD pass (update docs, ask questions, then sync code/tests/deploy). Keep code lean and favor integration/end-to-end tests over mocks unless external APIs require them. Format all tasks as single-line markdown tasks and mark execution progress with ✅.

**LLM-Friendly Documentation**: All project documentation must be optimized for LLM processing:
- Use clear, concise language without verbose explanations
- Maintain consistent structure and formatting across all documents
- Avoid legacy references or migration hints
- Focus on actionable, current information only
- Structure content for easy scanning and parsing by LLMs

**Template Usage Guidelines**:
- Create `docs/designs/` directory for component design documents
- Use `~/.agent3d/templates/DETAILED-DESIGN.template.md` for component-specific documentation
- **Naming Convention**: Use `{COMPONENT}.md` for design files and CAPS for all documentation files
- **Folder Structure**: Use `docs/designs/` for component designs

**Template System**: Agent3D provides comprehensive templates for all documentation types. See [Common Procedures](docs/COMMON-PROCEDURES.md#template-system) for complete setup and usage instructions.

**DDD Status Tracking**: After completing any DDD pass, update `docs/DDD-STATUS.md` using procedures from [Common Procedures](docs/COMMON-PROCEDURES.md#ddd-status-management).

**Language-Specific Rules**: At the start of each project, identify the programming language(s) and load the corresponding language-specific rules from `~/.agent3d/rules/`. These rules are available locally in the cloned repository. Memorize these rules and apply them consistently throughout all development activities including implementation, refactoring, and code review.