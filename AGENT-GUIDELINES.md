# Documentation-Driven Development (DDD) for LLM Coding Agents
*"Write the docs, then write the code—keep it lean, test it for real."*

---

## 0  Prime Directive
**Update Docs → Iterate with User → Implement → Validate.** Docs are the single source of truth; code, tests, and deployment scripts must never outpace them.

---

## 1  Agent Workflow

| Phase | Agent Action | Human Role |
|-------|--------------|-----------|
| **Scan** | Detect drift or missing docs by parsing repo. | — |
| **Draft** | Generate/refresh docs (§3) with full content. | — |
| **Ask** | Surface gaps, design options, or clarifications. | Supply answers / edits. |
| **Sync** | Finalize docs, then produce matching code, tests, CI, deploy scripts. | Review & approve. |
| **Guard** | Refuse or fail if docs & code diverge. | — |

> **DDD Pass** – When instructed, perform **Scan → Draft → Ask → Sync**, then commit
> `DDD: <summary>` (or tag `docs-n/a` if no drift).

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

## 2  Lean-Code & Testing Principles

| Principle | Agent Rule |
|-----------|-----------|
| **Keep Code Lean** | Implement only what the current docs require; avoid speculative abstractions. |
| **Real Tests Over Mocks** | Prefer integration & end-to-end tests that exercise concrete components. Use mocks/stubs only when external calls (e.g., payment gateways) make them unavoidable. |
| **Traceability** | Each test references its `TC-####` in `docs/TEST-CASES.md`. |
| **Fast Feedback** | Critical end-to-end paths run in CI; heavier suites may run nightly. |
| **Language-Specific Rules** | Follow the language-specific rules defined in the rules directory. |

### Language-Specific Rules

- [Python](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/python.md) - Rules for Python development
- [JavaScript](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/javascript.md) - Rules for JavaScript development
- [Java](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/java.md) - Rules for Java development
- [Go](https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/go.md) - Rules for Go development

---

## 3  Primary Docs & Generation Rules

| File | Purpose | Full content if **missing** |
|------|---------|-----------------------------|
| `README.md` | Vision & quick-start | Goal, tech stack, install steps, example commands, demo, contributors, license |
| `docs/FEATURES.md` | Checklist | `[ ] Feature-Slug — scope`, grouped by module |
| `docs/ARCHITECTURE.md` | Design & decisions | Mermaid diagrams, data-flow, trade-offs |
| `docs/TASKS.md` | Backlog | `[ ] Task — link/source`, priority from TODOs/issues |
| `docs/TEST-CASES.md` | Canonical tests | `TC-####`, feature, preconditions, steps, expected result, **Automated?** |
| `docs/DEPLOYMENT.md` | Ops runbook | Envs, build scripts, IaC, containers, secrets, health checks, CI/CD, rollback |

**Missing-Doc Protocol** – Generate a full, content-rich version (no placeholders) before coding.

---

## 4  Drift Enforcement
* Each commit updates a doc file **or** tags `docs-n/a`.
* CI fails on doc↔code mismatch or missing artifacts.
* Agent rejects tasks that violate DDD or Lean-Code/Test rules.

---

### Markdown Task Formatting

* Use markdown task lists (`- [ ]`) for all **features, tasks, and test cases**.
* Prefer **single-line entries** for clarity and brevity.
* **Mark completion** using **tick** (`- [x]`) for completed items in markdown task lists.
* **Use ✅ symbol** specifically to indicate **step execution** in processes, workflows, or procedures.
* **Task Status Examples**:
  - `- [ ] Pending task` (not started)
  - `- [x] Completed task` (finished)
  - `✅ Step executed` (indicates a process step has been performed)

---

### Minimal Guideline Prompt (embed in each agent)

> *Follow `.agent-guidelines.md`.
> If docs drift or a primary doc is missing, run a DDD pass (update docs, ask questions, then sync code/tests/deploy).
> Keep code lean; favor integration/end-to-end tests, avoid mocks unless absolutely necessary.
> **Format all features, tasks, and test cases as single-line markdown tasks (`- [ ]`) and tick them when completed. Use ✅ to indicate step execution in processes.***
