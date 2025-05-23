# Documentation-Driven Development (DDD) for LLM Coding Agents
*“Write the docs, then write the code—keep it lean, test it for real.”*

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
- [Foundation Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/foundation_pass.md) - Creating foundational documentation and architecture
- [Documentation Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/documentation_pass.md) - Documenting features, requirements, and priorities
- [Synchronization Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/synchronization_pass.md) - Aligning documentation with code at any scale
- [Quality Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/quality_pass.md) - Verifying and improving documentation quality
- [Prune Pass](https://raw.githubusercontent.com/ningsuhen/agent3d/main/passes/simplified/prune_pass.md) - Removing outdated or redundant content

### DDD Rules

1. **Docs First, Always** - Documentation is the source of truth. Code, tests, and deployment scripts must never outpace documentation.
2. **Comprehensive Coverage** - Ensure all features, requirements, and priorities are fully documented.
3. **Clarity Above All** - Documentation should be clear, concise, and accessible to all stakeholders.
4. **Consistency is Key** - Maintain consistent formatting, terminology, and structure across all documentation.

---

## 2  Lean-Code & Testing Principles

| Principle | Agent Rule |
|-----------|-----------|
| **Keep Code Lean** | Implement only what the current docs require; avoid speculative abstractions. |
| **Real Tests Over Mocks** | Prefer integration & end-to-end tests that exercise concrete components. Use mocks/stubs only when external calls (e.g., payment gateways) make them unavoidable. |
| **Traceability** | Each test references its `TC-####` in `docs/TEST-CASES.md`. |
| **Fast Feedback** | Critical end-to-end paths run in CI; heavier suites may run nightly. |

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
* **Tick** (`- [x]`) completed items to mark their status.

---

### Minimal Guideline Prompt (embed in each agent)

> *Follow `.agent-guidelines.md`.
> If docs drift or a primary doc is missing, run a DDD pass (update docs, ask questions, then sync code/tests/deploy).
> Keep code lean; favor integration/end-to-end tests, avoid mocks unless absolutely necessary.
> **Format all features, tasks, and test cases as single-line markdown tasks (`- [ ]`) and tick them when completed.***