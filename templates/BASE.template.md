# Base Template System

**PURPOSE:** Unified template structure and validation system for Agent3D documentation.

## Common Template Structure

**STANDARD SECTIONS:**
1. **Format Specification** - Document purpose and requirements
2. **Template Content** - Placeholder structure with {{variables}}
3. **Validation** - Universal + template-specific rules

**UNIVERSAL VARIABLES:**
- `{{document_title}}`, `{{document_purpose}}`, `{{project_name}}`
- `{{author}}`, `{{creation_date}}`, `{{last_updated}}`, `{{version}}`

## Universal Validation Rules

**ALL TEMPLATES MUST:**
- [ ] Follow [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist)
- [ ] Replace ALL {{placeholders}} with actual content
- [ ] Remove `<template>` and `<example>` tags
- [ ] Use `## Groups` / `### Sub-Groups` structure
- [ ] Include functional links and single-line entries
- [ ] Mark `[x]` only with verifiable evidence

## Template-Specific Validation

### Documentation Templates (FEATURES, REQUIREMENTS, TASKS, etc.)
- [ ] **Format Compliance:** Follow specified format patterns exactly
- [ ] **Priority Organization:** Use High/Medium/Low/Completed structure where applicable
- [ ] **Status Indicators:** Use `[x]`/`[ ]`/`[~]` consistently
- [ ] **Functional Grouping:** Organize content by logical functional areas
- [ ] **Completion Criteria:** Include clear acceptance criteria for each item

### Design Templates (HIGH-LEVEL-DESIGN, DETAILED-DESIGN, etc.)
- [ ] **Architecture Clarity:** Clear system architecture and component relationships
- [ ] **Technical Accuracy:** All technical specifications are accurate and testable
- [ ] **Diagram Validation:** All diagrams render correctly and support the text
- [ ] **Interface Documentation:** All APIs and interfaces properly documented

### Process Templates (EXEC-PLAN, IMPLEMENTATION-PLAN, etc.)
- [ ] **Step Sequencing:** Logical step-by-step progression
- [ ] **Checkpoint Definition:** Clear checkpoints and verification criteria
- [ ] **Risk Assessment:** Identified risks with mitigation strategies
- [ ] **Resource Planning:** Required resources and dependencies identified

### User-Focused Templates (USER-STORIES, USER-JOURNEY-MAP, etc.)
- [ ] **User Perspective:** Written from user's point of view
- [ ] **Acceptance Criteria:** Clear, testable acceptance criteria
- [ ] **Journey Mapping:** Logical user flow and interaction patterns
- [ ] **Persona Alignment:** Content aligns with defined user personas

## Template Usage Process

1. **Access**: Templates from `~/.agent3d/templates/`
2. **Replace**: All {{placeholders}} with actual content
3. **Remove**: Template tags before finalizing
4. **Validate**: Against universal + specific rules

**REFERENCE:** See [Common Procedures - Template System](../docs/COMMON-PROCEDURES.md#template-system) for complete usage instructions.
