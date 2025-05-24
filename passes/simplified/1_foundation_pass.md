# Foundation Pass

**Purpose:** Establish core project documentation including architecture, technical decisions, and documentation structure.

## When to Use
- Starting new projects or major features
- Making significant architectural changes
- Establishing documentation framework
- Documenting major technical decisions

## Process
1. **Scan:**
   - **Repository Update**: `git -C ~/.agent3d pull origin main`
   - Identify missing/outdated documentation
   - Check foundation documents needed
   - **Structure Check**: Verify `docs/designs/` directory exists
2. **Draft:**
   - Create foundation documents from `~/.agent3d/templates/`:
     - `README.md`
     - `docs/HIGH-LEVEL-DESIGN.md`
     - `docs/FEATURES.md`
     - `docs/TASKS.md`
     - `docs/TEST-CASES.md`
     - `docs/DDD-STATUS.md`
   - Follow template format specifications exactly, replacing {{placeholders}} with actual content
   - Do NOT include `<template>` or `<example>` tags in actual documentation files
   - **CRITICAL**: Use `## Groups` and `### Sub-Groups` heading structure
   - **CRITICAL**: Mark features as `[x]` completed ONLY when verifiable evidence exists
   - Create `docs/designs/` directory for component design documents
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
   - Update `CHANGELOG.md` with foundation changes (Added: new documentation files, architectural decisions)
   - Update `DDD-STATUS.md` with Foundation Pass completion

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
