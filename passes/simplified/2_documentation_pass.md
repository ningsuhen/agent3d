# Documentation Pass

**Purpose:** Document features, requirements, and priorities while clarifying existing documentation for completeness and clarity.

**Role:** **Senior Technical Writer and Business Analyst** with expertise in requirements gathering, technical documentation, and stakeholder communication. Focus on clarity, completeness, and user-centered documentation.

## When to Use
- Adding new features to the project
- After planning meetings or scope changes
- When documentation contains ambiguities or inconsistencies
- Before implementing complex features with unclear requirements
- When exploring unfamiliar technical domains
- **Creating design proposals** for complex features that need detailed planning
- **UI/UX projects** requiring wireframes, user flows, and interaction specifications

## Process
1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), review `.agent3d-config.yml`, identify gaps, check `docs/proposals/active/`
2. **Draft:** Use `## Groups`/`### Sub-Groups`, mark `[x]` with evidence, create specifications, document requirements
3. **Ask:** Clarify scope, priorities, constraints
4. **Sync:** Update FEATURES.md, align roadmap

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Feature entries in `FEATURES.md`
- Test cases in `TEST-CASES.md`
- Technical constraints documented
- Updated `TASKS.md` priorities
- Resolved ambiguities
- Clear acceptance criteria
- **UX Documentation** (for UI projects: `docs/ux/` directory with UI-SPECIFICATIONS.md, wireframes, user-flows, interaction-patterns)

## Related Passes
Requirements → Foundation → **Documentation** → Development → Testing

**Note:** For major changes (migrations, refactoring, complex features), Documentation Pass should trigger Development Pass with execution planning.

## Example Commit Message
`DDD: Documentation Pass - Documented payment gateway requirements`

## UX Documentation Guidelines

### **For UI/UX Projects**
When the project involves user interfaces, Documentation Pass should create comprehensive UX documentation:

#### **Required UX Directory Structure**
```
docs/ux/
├── UI-SPECIFICATIONS.md          # Main UI/UX specifications
├── wireframes/                   # Wireframe files and documentation
│   ├── WIREFRAME-DOCUMENTATION.md
│   ├── desktop-wireframes.drawio
│   └── mobile-wireframes.drawio
├── user-flows/                   # User journey documentation
│   └── primary-user-flow.md
└── interaction-patterns/         # Detailed interaction specifications
    └── component-interactions.md
```

#### **UX Documentation Process**
1. **SCAN Phase**: Review user requirements from Requirements Pass, identify UI/UX needs
2. **DRAFT Phase**:
   - Create `docs/ux/UI-SPECIFICATIONS.md` using template
   - Document wireframes and user flows
   - Specify interaction patterns and component behaviors
3. **ASK Phase**: Validate UX approach with stakeholders and users
4. **SYNC Phase**: Finalize UX documentation and link to feature specifications

#### **UX Templates to Use**
- `~/.agent3d/templates/UX-SPECIFICATIONS.template.md` - Main UI/UX specifications
- `~/.agent3d/templates/USER-JOURNEY-MAP.template.md` - User flow documentation

#### **Integration with Requirements**
UX documentation in Documentation Pass should reference and build upon:
- User personas from Requirements Pass
- UX principles from Requirements Pass
- User journey maps from Requirements Pass
- Business objectives and user stories
