# Requirements Pass

**Purpose:** Establish clear, comprehensive requirements and business objectives before any technical implementation begins. Document stakeholder needs, business goals, and success criteria.

**Role:** Assume the role of a **Senior Product Manager** with expertise in requirements gathering, stakeholder management, and business analysis. Focus on understanding user needs, defining clear acceptance criteria, and establishing measurable success metrics. Think like a product professional who bridges business objectives with technical implementation.

## When to Use
- Starting new projects or major features
- When business requirements are unclear or undocumented
- Before architectural decisions are made
- When stakeholder alignment is needed
- During product discovery phases
- When pivoting or changing project direction
- Before major feature development cycles

## Process
1. **Scan:**
   - **Common Setup**: Follow [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management) and [Project Root Establishment](../docs/COMMON-PROCEDURES.md#project-root-establishment)
   - Identify existing requirements documentation gaps
   - Review any existing business documentation
   - Assess stakeholder alignment on project goals
   - Identify missing or unclear requirements

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
- **Precedes:** [Foundation Pass](1_foundation_pass.md) - Requirements inform architectural decisions
- **Informs:** [Documentation Pass](2_documentation_pass.md) - Requirements drive feature documentation
- **Templates:**
  - `~/.agent3d/templates/REQUIREMENTS.template.md` - Main requirements documentation
  - `~/.agent3d/templates/USER-STORIES.template.md` - User stories and personas
  - `~/.agent3d/templates/ACCEPTANCE-CRITERIA.template.md` - Acceptance criteria
  - `~/.agent3d/templates/BUSINESS-OBJECTIVES.template.md` - Business objectives and KPIs

## Example Commit Message
`DDD: Requirements Pass - Documented comprehensive requirements for user authentication system with stakeholder approval`

## Requirements Documentation Structure

### Business Requirements
- **Business Objectives**: Clear goals and expected outcomes
- **Success Metrics**: Measurable KPIs and success criteria
- **Stakeholder Needs**: Identified stakeholder groups and their needs
- **Business Constraints**: Budget, timeline, regulatory requirements

### Functional Requirements
- **User Stories**: As a [user type], I want [functionality] so that [benefit]
- **Use Cases**: Detailed scenarios of system interactions
- **Feature Requirements**: Specific functionality the system must provide
- **Integration Requirements**: External system interactions

### Non-Functional Requirements
- **Performance**: Response times, throughput, scalability requirements
- **Security**: Authentication, authorization, data protection requirements
- **Usability**: User experience and accessibility requirements
- **Reliability**: Availability, fault tolerance, recovery requirements

### Acceptance Criteria
- **Testable Conditions**: Clear pass/fail criteria for each requirement
- **Definition of Done**: Completion criteria for features
- **Quality Gates**: Standards that must be met before delivery

## Requirements Quality Standards
- **Clear and Unambiguous**: Each requirement has single interpretation
- **Testable and Verifiable**: Can be validated through testing
- **Traceable**: Linked to business objectives and design decisions
- **Prioritized**: Ranked by business value and urgency
- **Feasible**: Technically and economically achievable
- **Complete**: All necessary requirements captured

## Stakeholder Management
- **Identification**: Map all stakeholders and their interests
- **Communication Plan**: Regular updates and feedback loops
- **Conflict Resolution**: Process for resolving requirement conflicts
- **Change Management**: Controlled process for requirement changes
- **Sign-off Process**: Formal approval of requirements baseline

## Requirements Traceability
- **REQ-####**: Unique identifiers for each requirement
- **Business-to-Technical Mapping**: Link business needs to technical features
- **Requirements-to-Test Mapping**: Ensure all requirements are testable
- **Change Impact Analysis**: Track effects of requirement changes

## Validation Techniques
- **Stakeholder Reviews**: Regular validation with business stakeholders
- **User Feedback**: Direct input from end users
- **Prototyping**: Early validation through mockups or prototypes
- **Requirements Walkthrough**: Systematic review of all requirements
- **Acceptance Testing**: Validation through acceptance criteria testing

## Common Requirements Anti-Patterns to Avoid
- **Vague Language**: "User-friendly," "fast," "secure" without specifics
- **Solution-Focused**: Describing how instead of what
- **Untestable Requirements**: Cannot be verified objectively
- **Conflicting Requirements**: Contradictory or incompatible needs
- **Missing Stakeholders**: Not involving all affected parties
- **Scope Creep**: Uncontrolled expansion of requirements
- **Gold Plating**: Adding unnecessary features beyond requirements

## Quality Gates
- [ ] All business objectives clearly documented
- [ ] Functional requirements complete and unambiguous
- [ ] Non-functional requirements specified with metrics
- [ ] Acceptance criteria defined for all requirements
- [ ] Stakeholder sign-off obtained
- [ ] Requirements traceability established
- [ ] Change management process defined
- [ ] Success metrics and KPIs agreed upon
- [ ] User personas and use cases validated
- [ ] Requirements baseline established
