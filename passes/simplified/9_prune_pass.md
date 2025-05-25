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
1. **Scan:**
   - Identify outdated, redundant, or irrelevant documentation
   - Look for deprecated features that are still documented
   - Find duplicate information across multiple documents
   - Identify documentation for removed components or functionality

2. **Draft:**
   - Mark sections for removal or archiving
   - Prepare consolidated versions of redundant information
   - Document what will be removed and why

3. **Ask:**
   - Confirm which documentation is safe to remove
   - Verify that marked sections are truly obsolete
   - Clarify historical value of potentially outdated documentation

4. **Sync:**
   - Remove or archive unnecessary documentation
   - Update cross-references to removed content
   - Ensure remaining documentation maintains coherence after removals

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
