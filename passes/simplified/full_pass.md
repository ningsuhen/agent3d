# Full Pass

**Purpose:** Comprehensive documentation-driven development pass that reduces overall project drift and brings all passes to a similar alignment level, ensuring complete consistency across all project aspects.

**Includes:** All numbered passes (Foundation → Documentation → Implementation → Testing → Refactoring → Code Review → Synchronization → Quality → Prune)

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

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Fully aligned documentation and code
- Complete and accurate architectural documentation
- Comprehensive feature documentation
- Updated roadmap and priorities
- Resolved ambiguities
- Improved documentation quality and readability
- Removed outdated or redundant content
- Validated consistency across all documentation
- **Balanced alignment levels across all passes (90%+ target)**
- **Minimized drift indicators throughout the project**
- **Consistent project health metrics across all DDD passes**

## Example Commit Message
`DDD: Full Pass - Balanced alignment across all passes, reduced drift indicators`

## Execution Strategy
A Full Pass is extensive and may be executed in phases, focusing on different aspects. **Priority should be given to passes with lower alignment levels to achieve balance:**

1. **Foundation Phase**
   - Update architectural documentation
   - Establish or refresh core documentation structure

2. **Documentation Phase**
   - Document all features and requirements
   - Update priorities and roadmap
   - Resolve ambiguities

3. **Implementation Phase**
   - Implement features according to documentation
   - Add basic test coverage for core functionality
   - Ensure code meets project standards

4. **Testing Phase**
   - Add comprehensive test coverage
   - Test edge cases and error conditions
   - Verify all test cases in TEST-CASES.md

5. **Refactoring Phase**
   - Clean up code without changing functionality
   - Improve performance and maintainability
   - Ensure architectural alignment

6. **Code Review Phase**
   - Review changes between base branch and PR
   - Provide feedback through PR comments
   - Set PR review status to "Pending" until issues are addressed
   - Approve PR once all issues are resolved

7. **Synchronization Phase**
   - Align documentation with current implementation
   - Reconcile any divergences

8. **Quality Phase**
   - Verify documentation accuracy
   - Improve quality

9. **Prune Phase**
   - Remove outdated or redundant content
   - Archive historical information when appropriate

Each phase follows the Scan → Draft → Ask → Sync workflow, building upon the previous phase. **The goal is to achieve consistent alignment levels (90%+) across all passes and minimize drift indicators throughout the project.**
