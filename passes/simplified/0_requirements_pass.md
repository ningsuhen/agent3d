# Requirements Pass

**Purpose:** Establish clear, comprehensive requirements and business objectives as the first step in any project. Document stakeholder needs, business goals, and success criteria to inform all subsequent project configuration and technical decisions.

**Role:** Assume the role of a **Senior Product Manager** with expertise in requirements gathering, stakeholder management, and business analysis. Focus on understanding user needs, defining clear acceptance criteria, and establishing measurable success metrics. Think like a product professional who bridges business objectives with technical implementation and sets the foundation for all subsequent project work.

## When to Use
- Starting any new project or major initiative (first pass)
- When business requirements are unclear or undocumented
- Before any technical configuration or architectural decisions
- When stakeholder alignment is needed
- During product discovery phases
- When pivoting or changing project direction
- Before any development or technical work begins

## Process
1. **Scan:**
   - **Common Setup**: Follow [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management) and [Project Root Establishment](../docs/COMMON-PROCEDURES.md#project-root-establishment)
   - Identify existing requirements documentation gaps
   - Review any existing business documentation
   - Assess stakeholder alignment on project goals
   - Identify missing or unclear requirements
   - Understand the business context and problem space

2. **Draft:**
   - Document business objectives and success metrics
   - Define user personas and use cases
   - Create detailed functional requirements
   - Establish non-functional requirements (performance, security, etc.)
   - Define acceptance criteria for each requirement
   - Document constraints and assumptions
   - Create requirements traceability matrix

3. **Ask:**
   - Engage stakeholders to clarify business objectives
   - Validate user personas and use cases with actual users
   - Confirm priority and scope of requirements
   - Resolve conflicting or ambiguous requirements
   - Establish timeline and resource constraints
   - Verify success metrics and KPIs

4. **Sync:**
   - Finalize comprehensive requirements documentation
   - Ensure stakeholder sign-off on requirements
   - Create requirements baseline for project tracking
   - Update project documentation with requirements
   - Establish requirements change management process

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Comprehensive Requirements Documentation:**
  - `docs/REQUIREMENTS.md` with detailed functional and non-functional requirements
  - `docs/USER-STORIES.md` with user personas and use cases
  - `docs/ACCEPTANCE-CRITERIA.md` with testable acceptance criteria
  - `docs/BUSINESS-OBJECTIVES.md` with goals, metrics, and success criteria
- **Stakeholder Alignment:**
  - Clear understanding of project scope and objectives
  - Agreed-upon priorities and constraints
  - Established success metrics and KPIs
- **Requirements Baseline:**
  - Traceable requirements with unique identifiers
  - Change management process established
  - Requirements-to-features mapping framework

## Related Passes
- **First Pass:** This is the initial pass that establishes business requirements
- **Next:** [Foundation Pass](1_foundation_pass.md) - Project configuration follows requirements
- **Informs:** All subsequent DDD passes based on requirements scope
- **Templates:**
  - `~/.agent3d/templates/REQUIREMENTS.template.md` - Main requirements documentation
  - `~/.agent3d/templates/USER-STORIES.template.md` - User stories and personas
  - `~/.agent3d/templates/ACCEPTANCE-CRITERIA.template.md` - Acceptance criteria
  - `~/.agent3d/templates/BUSINESS-OBJECTIVES.template.md` - Business objectives and KPIs

## Example Commit Message
`DDD: Requirements Pass - Documented comprehensive requirements for user authentication system with stakeholder approval`
