# Development Pass

**Purpose:** Step-by-step feature implementation with checkpoints and execution plans.

**Role:** **Development Lead** - feature discovery, planning, implementation, checkpoint-based execution.

## When to Use

**Required:** Migrations, refactoring, complex features, infrastructure changes, breaking changes
**Suitable:** Feature implementation, bug fixes, documentation-driven development, proof-of-concept conversion
**Auto-Triggers:** >3 components, external dependencies, Medium/High risk, >1 day effort, complex rollback

## Process

1. **Scan:** Repository update, scan docs/, identify features/drift needing development
2. **Draft:** Feature selection (AUTO/PICKER mode), create EXEC-PLAN-{change-name}.md with documented steps, create exec-plan/{change-name} branch
3. **Ask:** Validate selection and execution plan, confirm approach/priorities
4. **Sync:** Execute steps in loop on exec-plan branch, auto-commit steps/checkpoints, update progress (mark ✅)
5. **Merge:** Complete execution, confirm merge to main branch, delete exec-plan branch

## Feature Discovery & Selection

**Scans:** docs/FEATURES.md, docs/TASKS.md, docs/DDD-STATUS.md, docs/REQUIREMENTS.md, docs/ACCEPTANCE-CRITERIA.md, docs/designs/*.md, docs/proposals/*.md

**AUTO MODE:** Automatically picks features/drift by priority, respects dependencies/effort limits, includes drift fixes/blockers
**PICKER MODE:** Human selection with priorities/dependencies/estimates shown

## Outcomes

- Execution plan (`docs/runs/EXEC-PLAN-{change-name}.md`)
- Working implementation with basic tests
- Checkpoint strategy with rollback points
- Risk assessment with mitigation strategies
- Progress tracking, standards compliance, updated documentation

**Related:** Requirements → Foundation → Documentation → **Development** → Testing
**Commit:** `DDD: Development Pass - Implemented user authentication and security features`

## Execution Plan & Loop

**Required Sections:** Change overview, feature discovery results, step-by-step plan with LLM instructions, checkpoint strategy (every 2-4 steps), risk assessment, dependencies, quality gates

**Step Format:** Status ([ ] [~] [x]), Feature, Description, LLM Instructions, Verification Criteria, Estimated Time
**Checkpoints:** Every 2-4 steps, rollback points, validation gates, progress tracking

**Loop Model:**
```
1. Create execution plan with documented steps
2. While (incomplete steps exist): Read step → Execute → Update status → Verify checkpoints → Continue
3. Archive plan, update documentation
```

**Quality Standards:**
- Plan: Step-by-step sequence, checkpoint markers, rollback instructions, risk assessment, dependencies, validation criteria, LLM instructions, success criteria
- Implementation: Language-specific rules, documented requirements only, lean/maintainable code, technical decisions documented, readability/standards compliance, basic tests
- Validation: Dependencies documented, rollback strategy tested, atomic steps, safe resumption, actionable mitigation, realistic timelines, measurable criteria

**Testing:** Happy path, basic validation, core functionality, comprehensive foundation, existing suite integration, checkpoint verification

## Configuration & Management

See [Common Procedures - Development Pass Configuration](../docs/COMMON-PROCEDURES.md#development-pass-configuration) for complete configuration options.

**Checkpoint Management:**
- Before: Validate criteria, run tests, verify no regressions, update status
- Failure: Follow rollback instructions, document issues/blockers, assess continue/abort, update risk assessment
- Progress: Mark [x] completed, update percentage, track time estimates vs actual, document deviations

**Integration:** Prepares Testing Pass (working implementation, basic tests, test scenarios, foundation, updates TEST-CASES.md), Updates documentation (FEATURES.md, TASKS.md, DDD-STATUS.md, design docs)
