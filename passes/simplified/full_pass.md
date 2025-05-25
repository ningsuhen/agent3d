# Full Pass

**Purpose:** Comprehensive documentation-driven development pass that reduces overall project drift and brings all passes to a similar alignment level, ensuring complete consistency across all project aspects.

**Role:** Assume the role of a **Technical Project Manager** who coordinates and delegates to domain experts. You don't perform the technical work yourself—instead, you orchestrate the execution by handing off each pass to its designated expert role. Focus on ensuring comprehensive coverage, managing dependencies between passes, and maintaining overall project alignment. Think like a project manager who coordinates specialists to achieve complete system consistency.

**Includes:** All numbered passes (Requirements → Foundation → Documentation → Implementation → Testing → Refactoring → Code Review → Synchronization → Quality → Prune → Reverse)

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
1. **Scan (Project Manager Assessment):**
   - **Repository Update**: Ensure `~/.agent3d` repository is current with `git -C ~/.agent3d pull origin main`
   - Assess overall project health and identify which passes need attention
   - Review drift levels and alignment percentages across all passes
   - Identify passes with significantly lower alignment levels
   - Determine the optimal sequence and dependencies between passes
   - Plan resource allocation and coordination strategy

2. **Draft (Delegation Strategy):**
   - **Delegate to Pass Experts**: Hand off each pass to its designated expert role:
     - **Senior Product Manager** → Requirements Pass
     - **Solutions Architect** → Foundation Pass
     - **Technical Writer & Business Analyst** → Documentation Pass
     - **Senior Software Developer** → Implementation Pass
     - **Senior QA Engineer** → Testing Pass
     - **Senior Software Engineer & Code Quality Specialist** → Refactoring Pass
     - **Very Strict Senior Software Engineer** → Code Review Pass
     - **DevOps Engineer & Technical Lead** → Synchronization Pass
     - **Technical Documentation Specialist** → Quality Pass
     - **Technical Debt Specialist** → Prune Pass
     - **Software Architect & Technical Auditor** → Reverse Pass
   - Coordinate handoffs and ensure each expert has necessary context
   - Monitor progress and manage dependencies between passes

3. **Ask (Stakeholder Coordination):**
   - Facilitate communication between pass experts and stakeholders
   - Escalate cross-pass decisions that require management input
   - Coordinate resolution of conflicting recommendations from different experts
   - Ensure alignment on priorities and resource allocation

4. **Sync (Integration and Validation):**
   - Integrate results from all pass experts
   - Verify that all passes achieve similar alignment levels (target: 90%+)
   - Confirm overall drift reduction across the project
   - Coordinate final validation across all domains
   - Update `CHANGELOG.md` with comprehensive Full Pass changes across all categories
   - Update `DDD-STATUS.md` with Full Pass completion and final metrics
   - Ensure seamless handoff between expert domains

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Coordinated execution** of all passes by their respective domain experts
- **Balanced alignment levels across all passes (90%+ target)**
- **Minimized drift indicators throughout the project**
- **Consistent project health metrics across all DDD passes**
- **Seamless integration** of expert contributions from each pass
- **Comprehensive project alignment** achieved through expert delegation
- **Clear accountability** with each domain handled by appropriate specialists

## Example Commit Message
`DDD: Full Pass - Balanced alignment across all passes, reduced drift indicators`

## Execution Strategy

**Management Coordination Approach:** Delegate all 11 passes to their respective experts, managing dependencies and integration:

**Expert Delegation Sequence:**
0. **Senior Product Manager** → Requirements Pass
1. **Solutions Architect** → Foundation Pass
2. **Technical Writer & Business Analyst** → Documentation Pass
3. **Senior Software Developer** → Implementation Pass
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
