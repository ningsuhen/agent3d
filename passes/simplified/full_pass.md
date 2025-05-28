# Full Pass

**Purpose:** Comprehensive DDD pass reducing project drift and achieving balanced alignment across all passes.

**Role:** **Technical Project Manager** coordinating domain experts. Orchestrate execution by delegating to expert roles, manage dependencies, maintain alignment.

**Includes:** All numbered passes (Requirements → Foundation → Documentation → Development → Testing → Refactoring → Code Review → Synchronization → Quality → Prune → Reverse)

**Goal:** Minimize drift indicators across all passes and achieve balanced alignment levels (ideally 90%+ for all passes) to maintain project health and consistency.

## When to Use
- For major project milestones or releases
- When onboarding a new codebase or project
- During significant overhauls of existing systems
- For annual or semi-annual documentation health checks
- When preparing for external audits or reviews
- When drift indicators show significant imbalance across passes
- When multiple passes have alignment levels below 85%

## Process
1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), assess project health, review drift levels, identify low alignment passes
2. **Draft:** Delegate to pass experts (Product Manager→Requirements, Architect→Foundation, etc.), coordinate handoffs, monitor progress
3. **Ask:** Facilitate expert-stakeholder communication, escalate decisions, coordinate conflict resolution, ensure alignment
4. **Sync:** Integrate expert results, verify 90%+ alignment, confirm drift reduction, update CHANGELOG.md and DDD-STATUS.md

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Coordinated execution by domain experts
- Balanced alignment levels (90%+ target)
- Minimized drift indicators
- Consistent project health metrics
- Seamless expert integration
- Comprehensive project alignment
- Clear specialist accountability

## Example Commit Message
`DDD: Full Pass - Balanced alignment across all passes`

## Execution Strategy

**Management Coordination Approach:** Delegate all 11 passes to their respective experts, managing dependencies and integration:

**Expert Delegation Sequence:**
0. **Senior Product Manager** → Requirements Pass
1. **Solutions Architect** → Foundation Pass
2. **Technical Writer & Business Analyst** → Documentation Pass
3. **Senior Software Developer** → Development Pass
4. **Senior QA Engineer** → Testing Pass
5. **Senior Software Engineer & Code Quality Specialist** → Refactoring Pass
6. **Very Strict Senior Software Engineer** → Code Review Pass
7. **DevOps Engineer & Technical Lead** → Synchronization Pass
8. **Technical Documentation Specialist** → Quality Pass
9. **Technical Debt Specialist** → Prune Pass
10. **Software Architect & Technical Auditor** → Reverse Pass

**Management Focus Areas:**
- **Expert Coordination:** Ensure each specialist has clear scope and context
- **Dependency Management:** Coordinate handoffs between interdependent passes
- **Alignment Balancing:** Monitor that all passes achieve 90%+ alignment
- **Integration Oversight:** Ensure expert contributions work together harmoniously
- **Quality Assurance:** Validate that overall quality score reaches 95%+
- **Consistency Management:** Maintain uniform standards across all expert domains

**Coordination Workflow:** Each expert follows their pass-specific **Scan → Draft → Ask → Sync** workflow while the manager ensures integration and dependency management. **Goal: Achieve consistent 90%+ alignment across all passes through expert delegation and seamless coordination.**
