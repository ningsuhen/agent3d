# Documentation-Driven Development (DDD) for LLM Coding Agents
*"Write the docs, then write the code—keep it lean, test it for real."*

## Configuration
**DDD_REMOTE_BASE**: `https://raw.githubusercontent.com/ningsuhen/agent3d/main`

*Note: When fetching remote resources, replace `{{DDD_REMOTE_BASE}}` with the actual URL base above.*

## Prime Directive
**Documentation leads, code follows.** Always update docs before implementing code. Documentation is the single source of truth.

## Core Workflow

| Phase | Action | Human Role |
|-------|--------|-----------|
| **Scan** | Detect missing/outdated docs | — |
| **Draft** | Create/update documentation | — |
| **Ask** | Clarify gaps and decisions | Provide input |
| **Sync** | Implement code matching docs | Review & approve |

**DDD Pass**: Execute Scan → Draft → Ask → Sync, then commit with `DDD: <description>`

### DDD Passes

- [Full Pass]({{DDD_REMOTE_BASE}}/passes/simplified/full_pass.md) - Comprehensive pass encompassing all aspects
- [1. Foundation Pass]({{DDD_REMOTE_BASE}}/passes/simplified/1_foundation_pass.md) - Creating foundational documentation and architecture
- [2. Documentation Pass]({{DDD_REMOTE_BASE}}/passes/simplified/2_documentation_pass.md) - Documenting features, requirements, and priorities
- [3. Implementation Pass]({{DDD_REMOTE_BASE}}/passes/simplified/3_implementation_pass.md) - Implementing features with basic test coverage
- [4. Testing Pass]({{DDD_REMOTE_BASE}}/passes/simplified/4_testing_pass.md) - Adding comprehensive tests and verifying edge cases
- [5. Refactoring Pass]({{DDD_REMOTE_BASE}}/passes/simplified/5_refactoring_pass.md) - Cleaning up code without changing functionality
- [6. Code Review Pass]({{DDD_REMOTE_BASE}}/passes/simplified/6_code_review_pass.md) - Reviewing PR changes and providing feedback
- [7. Synchronization Pass]({{DDD_REMOTE_BASE}}/passes/simplified/7_synchronization_pass.md) - Aligning documentation with code at any scale
- [8. Quality Pass]({{DDD_REMOTE_BASE}}/passes/simplified/8_quality_pass.md) - Verifying and improving documentation quality
- [9. Prune Pass]({{DDD_REMOTE_BASE}}/passes/simplified/9_prune_pass.md) - Removing outdated or redundant content

---

## Development Principles

| Principle | Rule |
|-----------|------|
| **Lean Code** | Implement only documented requirements |
| **Real Tests** | Use integration tests; avoid mocks except for external APIs |
| **Traceability** | Reference test cases as `TC-####` from `docs/TEST-CASES.md` |
| **Fast Feedback** | Run critical tests in CI |
| **Language Rules** | Fetch and memorize language-specific rules from links below, apply consistently |

### Language-Specific Rules

- [Python]({{DDD_REMOTE_BASE}}/rules/python.md) - Rules for Python development
- [JavaScript]({{DDD_REMOTE_BASE}}/rules/javascript.md) - Rules for JavaScript development
- [Java]({{DDD_REMOTE_BASE}}/rules/java.md) - Rules for Java development
- [Go]({{DDD_REMOTE_BASE}}/rules/go.md) - Rules for Go development

---

## Required Documentation

| File | Purpose | Template |
|------|---------|----------|
| `README.md` | Project overview | [README Template]({{DDD_REMOTE_BASE}}/templates/README.template.md) |
| `docs/FEATURES.md` | Feature checklist with acceptance criteria | [FEATURES Template]({{DDD_REMOTE_BASE}}/templates/FEATURES.template.md) |
| `docs/ARCHITECTURE.md` | System design with diagrams and decisions | [ARCHITECTURE Template]({{DDD_REMOTE_BASE}}/templates/ARCHITECTURE.template.md) |
| `docs/TASKS.md` | Work backlog organized by priority | [TASKS Template]({{DDD_REMOTE_BASE}}/templates/TASKS.template.md) |
| `docs/TEST-CASES.md` | Test specifications with TC-#### format | [TEST-CASES Template]({{DDD_REMOTE_BASE}}/templates/TEST-CASES.template.md) |
| `docs/DDD-STATUS.md` | DDD pass status and alignment tracking | [DDD-STATUS Template]({{DDD_REMOTE_BASE}}/templates/DDD-STATUS.template.md) |

**Missing Documentation**: Always create complete content using the provided templates before coding. Templates contain format specifications, placeholder structures, and examples - do NOT include the `<template>` or `<example>` tags in actual documentation files.

---

## Documentation Enforcement
- Each commit must update documentation OR include `docs-n/a` tag
- CI/CD pipelines must validate documentation-code alignment
- Agents must reject tasks that violate DDD principles

## Task Formatting Guidelines

**For Features, Tasks, and Test Cases:**
- Use markdown task lists: `- [ ]` for pending, `- [x]` for completed
- Keep entries single-line for clarity
- Group related items logically
- **Features must include acceptance criteria**: Use format `(Criteria: <specific measurable criteria>)` as specified in [FEATURES Template]({{DDD_REMOTE_BASE}}/templates/FEATURES.template.md)
- **Follow template structures**: Use [TASKS Template]({{DDD_REMOTE_BASE}}/templates/TASKS.template.md) and [TEST-CASES Template]({{DDD_REMOTE_BASE}}/templates/TEST-CASES.template.md) for proper formatting

**For Process Execution:**
- Use ✅ symbol to mark completed steps during DDD pass execution
- Add ✅ next to steps as you complete them for real-time progress tracking
- Update `docs/DDD-STATUS.md` after each pass with phase-specific progress/drift

**Examples:**
- `- [ ] Implement user authentication` (pending task)
- `- [x] Add login validation` (completed task)
- `✅ Review feature documentation` (step completed during execution)

**Document Structure Example (following TEST-CASES.md pattern):**
```
## 📊 Summary
- **Total Items:** X
- **Completed:** Y ✅
- **Pending:** Z ⏸️
- **Skipped:** W ⏭️

## 📚 Section Name
- [ ] **Item-ID** - Description (Type, Priority)
```

**DDD Status Format (for docs/DDD-STATUS.md updates):**
Follow the [DDD-STATUS Template]({{DDD_REMOTE_BASE}}/templates/DDD-STATUS.template.md) format:
```
## 1️⃣ Pass Name
- **Status:** Completed ✅ / In Progress ⏸️ / Pending ⏸️
- **Alignment:** XX% ████████░░ (phase-specific completion)
- **Drift:** None 🟢 / Low 🟡 / Medium 🟠 / High 🔴 (domain-specific gaps)
- **Priority:** High/Medium/Low
- **Notes:** Context about current state
```

## Agent Instructions
Follow `.agent-guidelines.md`. When documentation is missing or outdated, run a DDD pass (update docs, ask questions, then sync code/tests/deploy). Keep code lean and favor integration/end-to-end tests over mocks unless external APIs require them. Format all tasks as single-line markdown tasks and mark execution progress with ✅.

**Template Usage**: When creating foundation documentation, always fetch and use the provided templates from the Required Documentation section. Follow these steps:
1. Fetch the appropriate template using the provided links
2. Follow the format specification exactly as described in the template
3. Replace all {{placeholders}} with actual project content
4. Do NOT include `<template>` or `<example>` tags in actual documentation files
5. Ensure all validation checklist items are met before considering documentation complete

**DDD Status Tracking**: After completing any DDD pass, update `docs/DDD-STATUS.md` with phase-specific alignment and drift indicators. Use the [DDD-STATUS Template]({{DDD_REMOTE_BASE}}/templates/DDD-STATUS.template.md) for consistent tracking.

**Language-Specific Rules**: At the start of each project, identify the programming language(s) and fetch the corresponding language-specific rules using the links provided in the Language-Specific Rules section. These rules are stored remotely and must be retrieved via web-fetch. Memorize these rules and apply them consistently throughout all development activities including implementation, refactoring, and code review.
