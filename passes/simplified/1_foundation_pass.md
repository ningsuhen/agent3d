# Foundation Pass

**Purpose:** Establish core project documentation including architecture, technical decisions, and documentation structure.

## When to Use
- Starting new projects or major features without existing documentation
- Making significant architectural changes to existing systems
- Establishing or restructuring documentation framework
- Documenting major technical decisions and their rationales
- **Refactoring existing projects** that still use `ARCHITECTURE.md` (should be renamed to `HIGH-LEVEL-DESIGN.md`)

## Process
1. **Scan:**
   - Identify what documentation is missing or needs architectural updates
   - Check which foundation documents need to be created or updated
   - **Legacy Check**: Look for `ARCHITECTURE.md` files that need to be renamed to `HIGH-LEVEL-DESIGN.md`
   - **Module Structure Check**: Verify if `docs/modules/` directory exists for detailed designs
2. **Draft:**
   - Create foundation documents using the provided templates:
     - `README.md` using [README Template]({{DDD_REMOTE_BASE}}/templates/README.template.md)
     - `docs/HIGH-LEVEL-DESIGN.md` using [HIGH-LEVEL-DESIGN Template]({{DDD_REMOTE_BASE}}/templates/HIGH-LEVEL-DESIGN.template.md)
     - `docs/FEATURES.md` using [FEATURES Template]({{DDD_REMOTE_BASE}}/templates/FEATURES.template.md)
     - `docs/TASKS.md` using [TASKS Template]({{DDD_REMOTE_BASE}}/templates/TASKS.template.md)
     - `docs/TEST-CASES.md` using [TEST-CASES Template]({{DDD_REMOTE_BASE}}/templates/TEST-CASES.template.md)
     - `docs/DDD-STATUS.md` using [DDD-STATUS Template]({{DDD_REMOTE_BASE}}/templates/DDD-STATUS.template.md)
   - Follow template format specifications exactly, replacing {{placeholders}} with actual content
   - Do NOT include `<template>` or `<example>` tags in actual documentation files
   - **🔗 CRITICAL**: Use `## Groups (Modules)` and `### Sub-Groups (Sub-modules)` heading structure
   - **🚨 CRITICAL**: Mark features as `[x]` completed ONLY when verifiable evidence exists (tests or manual verification)
   - **📁 REFACTORING**: If `ARCHITECTURE.md` exists, rename to `HIGH-LEVEL-DESIGN.md` and update all references
   - **📁 MODULE STRUCTURE**: Create `docs/modules/` directory for detailed design documents
   - Develop architectural diagrams using Mermaid syntax as shown in templates
   - Document technical decisions and trade-offs following template structure
3. **Ask:**
   - Clarify project scope, architecture, or requirements
   - Discuss technical constraints, integration points, or design alternatives
   - Verify template usage and content accuracy
4. **Sync:**
   - Ensure all foundation documentation follows template formats exactly
   - Verify architectural documentation is complete and accurate
   - Validate that all {{placeholders}} have been replaced with actual content

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Complete set of foundation documentation files following template formats:
  - `README.md` with project overview, features, installation, and usage
  - `docs/HIGH-LEVEL-DESIGN.md` with system overview, components, data flow, and technical decisions
  - `docs/FEATURES.md` with feature list including acceptance criteria in (Criteria: <>) format
  - `docs/TASKS.md` with prioritized work backlog
  - `docs/TEST-CASES.md` with test specifications using TC-#### format and execution framework
  - `docs/DDD-STATUS.md` with pass status tracking, alignment metrics, and drift indicators
- All documentation follows exact template specifications with {{placeholders}} replaced
- Architectural diagrams using proper Mermaid syntax
- No `<template>` or `<example>` tags in actual documentation files
- Comprehensive foundation for subsequent DDD passes

## Example Commit Message
`DDD: Foundation Pass - Created initial documentation and architecture for payment processing system`
