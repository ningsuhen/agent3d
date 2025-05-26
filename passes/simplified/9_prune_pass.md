# Prune Pass

**Purpose:** A focused pass to identify and remove outdated, redundant, or irrelevant documentation, streamlining the documentation set for improved maintainability.

**Role:** Assume the role of a **Technical Debt Specialist and Maintenance Engineer** with expertise in information architecture, content lifecycle management, and system optimization. Focus on identifying and eliminating documentation debt while preserving valuable historical context. Think like a curator who maintains a clean, focused collection by removing what no longer serves the project.

## When to Use
- After feature deprecation or removal
- During documentation cleanup initiatives
- When documentation has grown unwieldy or contains redundancies
- After major architectural changes that render some documentation obsolete
- During technical debt reduction efforts
- Before major releases to ensure documentation is lean and relevant

## Process
**STANDARD WORKFLOW:** Follow [Common Procedures - Standard DDD Workflow](../docs/COMMON-PROCEDURES.md#standard-ddd-workflow)

**PRUNE-SPECIFIC FOCUS:**
1. **Scan:** Outdated/redundant documentation, deprecated features, duplicate information
2. **Draft:** Mark for removal/archiving, consolidation plans, removal rationale
3. **Ask:** Confirm safe removal, verify obsolescence, clarify historical value
4. **Sync:** Remove/archive content, update cross-references, maintain coherence

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Streamlined, relevant documentation
- Removed references to deprecated features
- Archived historical information when appropriate
- Improved documentation maintainability
- Reduced cognitive load for documentation readers
- Clearer focus on current functionality and architecture

## Example Commit Message
`DDD: Prune Pass - Removed documentation for deprecated legacy authentication system and consolidated redundant API descriptions`
