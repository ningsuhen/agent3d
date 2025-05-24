# Full Pass

**Purpose:** Comprehensive documentation-driven development pass that reduces overall project drift and brings all passes to a similar alignment level, ensuring complete consistency across all project aspects.

**Includes:** All numbered passes (Foundation → Documentation → Implementation → Testing → Refactoring → Code Review → Synchronization → Quality → Prune → Reverse)

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
1. **Scan:**
   - **Repository Update**: Ensure `~/.agent3d` repository is current with `git -C ~/.agent3d pull origin main`
   - Comprehensively review the entire codebase and documentation
   - Identify all gaps, inconsistencies, and areas for improvement
   - Map the current state of documentation against code
   - Identify outdated or redundant documentation
   - Assess drift levels and alignment percentages across all passes
   - Identify passes with significantly lower alignment levels

2. **Draft:**
   - Create or update foundational documentation (architecture, features)
   - Document all requirements, features, and priorities
   - Clarify ambiguities and resolve inconsistencies
   - Align documentation with current implementation
   - Improve quality and mark outdated content for removal
   - Focus on passes with lower alignment levels to bring them up to standard
   - Address high-drift areas to reduce overall project drift

3. **Ask:**
   - Engage stakeholders for clarification on all aspects
   - Validate assumptions and decisions
   - Seek feedback on documentation quality and completeness
   - Confirm which documentation is safe to remove

4. **Sync:**
   - Ensure complete alignment between documentation and code
   - Refine documentation for clarity and relevance
   - Validate all documentation against implementation
   - Remove outdated content
   - Verify that all passes achieve similar alignment levels (target: 90%+)
   - Confirm overall drift reduction across the project
   - Update `CHANGELOG.md` with comprehensive Full Pass changes across all categories
   - Update `DDD-STATUS.md` with Full Pass completion and final metrics

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Balanced alignment levels across all passes (90%+ target)**
- **Minimized drift indicators throughout the project**
- **Consistent project health metrics across all DDD passes**
- Fully aligned documentation and code with improved quality

## Example Commit Message
`DDD: Full Pass - Balanced alignment across all passes, reduced drift indicators`

## Execution Strategy

**Streamlined Approach:** Execute all 10 passes systematically, prioritizing passes with lower alignment levels:

1. **Foundation** → 2. **Documentation** → 3. **Implementation** → 4. **Testing** → 5. **Refactoring**
6. **Code Review** → 7. **Synchronization** → 8. **Quality** → 9. **Prune** → 10. **Reverse**

**Focus Areas:**
- **Alignment Balancing:** Bring all passes to 90%+ alignment
- **Drift Elimination:** Resolve all drift indicators (target: 🟢 across all passes)
- **Quality Enhancement:** Improve overall quality score to 95%+
- **Consistency Achievement:** Ensure uniform documentation standards

Each phase follows the **Scan → Draft → Ask → Sync** workflow. **Goal: Achieve consistent 90%+ alignment across all passes and eliminate all drift indicators.**
