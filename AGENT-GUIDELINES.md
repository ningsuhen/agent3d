# Documentation-Driven Development (DDD) for LLM Coding Agents
*"Write the docs, then write the code—keep it lean, test it for real."*

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

- [Full Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/full_pass.md) - Comprehensive pass encompassing all aspects
- [1. Foundation Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/1_foundation_pass.md) - Creating foundational documentation and architecture
- [2. Documentation Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/2_documentation_pass.md) - Documenting features, requirements, and priorities
- [3. Implementation Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/3_implementation_pass.md) - Implementing features with basic test coverage
- [4. Testing Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/4_testing_pass.md) - Adding comprehensive tests and verifying edge cases
- [5. Refactoring Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/5_refactoring_pass.md) - Cleaning up code without changing functionality
- [6. Code Review Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/6_code_review_pass.md) - Reviewing PR changes and providing feedback
- [7. Synchronization Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/7_synchronization_pass.md) - Aligning documentation with code at any scale
- [8. Quality Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/8_quality_pass.md) - Verifying and improving documentation quality
- [9. Prune Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/9_prune_pass.md) - Removing outdated or redundant content

---

## Development Principles

| Principle | Rule |
|-----------|------|
| **Lean Code** | Implement only documented requirements |
| **Real Tests** | Use integration tests; avoid mocks except for external APIs |
| **Traceability** | Reference test cases as `TC-####` from `docs/TEST-CASES.md` |
| **Fast Feedback** | Run critical tests in CI |
| **Language Rules** | Follow language-specific rules from `/rules/` directory |

### Language-Specific Rules

- [Python](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/python.md) - Rules for Python development
- [JavaScript](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/javascript.md) - Rules for JavaScript development
- [Java](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/java.md) - Rules for Java development
- [Go](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/go.md) - Rules for Go development

---

## Required Documentation

| File | Purpose | Content When Missing |
|------|---------|---------------------|
| `README.md` | Project overview | Goal, tech stack, setup, examples |
| `docs/FEATURES.md` | Feature checklist | `- [ ] Feature-Name — description` |
| `docs/ARCHITECTURE.md` | System design | Diagrams, data flow, decisions |
| `docs/TASKS.md` | Work backlog | `- [ ] Task — priority/source` |
| `docs/TEST-CASES.md` | Test specifications | `TC-####`, steps, expected results |
| `docs/DEPLOYMENT.md` | Operations guide | Environments, CI/CD, monitoring |

**Missing Documentation**: Always create complete content before coding.

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

**For Process Execution:**
- Use ✅ symbol to mark completed steps during DDD pass execution
- Add ✅ next to steps as you complete them for real-time progress tracking

**Examples:**
- `- [ ] Implement user authentication` (pending task)
- `- [x] Add login validation` (completed task)
- `✅ Review feature documentation` (step completed during execution)

## Agent Instructions
Follow `.agent-guidelines.md`. When documentation is missing or outdated, run a DDD pass (update docs, ask questions, then sync code/tests/deploy). Keep code lean and favor integration/end-to-end tests over mocks unless external APIs require them. Format all tasks as single-line markdown tasks and mark execution progress with ✅.
