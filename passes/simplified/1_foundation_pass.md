# Foundation Pass

**Purpose:** Establish core project documentation including architecture, technical decisions, and documentation structure.

## When to Use
- Starting new projects or major features
- Making significant architectural changes
- Establishing documentation framework
- Documenting major technical decisions

## Process
1. **Scan:**
   - **Project Root**: Find or create `.agent3d` file to establish project root
   - **Repository Update**: `git -C ~/.agent3d pull origin main`
   - Identify missing/outdated documentation
   - Check foundation documents needed
   - **Structure Check**: Verify `docs/designs/` directory exists
2. **Draft:**
   - Create foundation documents from `~/.agent3d/templates/`: README, HIGH-LEVEL-DESIGN, FEATURES, TASKS, TEST-CASES, DDD-STATUS
   - Follow template format specifications exactly, replacing {{placeholders}} with actual content
   - **CRITICAL**: Use `## Groups` and `### Sub-Groups` heading structure
   - **CRITICAL**: Mark features as `[x]` completed ONLY when verifiable evidence exists
   - Do NOT include `<template>` or `<example>` tags in actual documentation files
   - Create `docs/designs/` directory for component design documents
3. **Ask:** Clarify project scope, architectural decisions, feature priorities
4. **Sync:** Ensure document consistency, validate cross-references, update CHANGELOG and DDD-STATUS

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

## Related Passes
- **Next:** [Documentation Pass](2_documentation_pass.md) - Document features and requirements
- **Templates:** See `~/.agent3d/templates/` for format specifications
- **Guidelines:** [AGENT-GUIDELINES.md](../../AGENT-GUIDELINES.md) for complete instructions

## Example Commit Message
`DDD: Foundation Pass - Created initial documentation and architecture for payment processing system`
