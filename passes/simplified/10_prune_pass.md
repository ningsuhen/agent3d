# Prune Pass

**Purpose:** Focused pass to identify and remove outdated, redundant, or irrelevant documentation, streamlining documentation for improved maintainability while ensuring quality standards are maintained.

**Role:** **Technical Debt Specialist and Maintenance Engineer** with expertise in information architecture, content lifecycle management, system optimization, and quality validation. Focus on eliminating documentation debt while preserving valuable historical context and ensuring remaining content meets quality standards.

## When to Use
- After feature deprecation or removal
- During documentation cleanup initiatives
- When documentation has grown unwieldy or contains redundancies
- After major architectural changes that render some documentation obsolete
- During technical debt reduction efforts
- Before major releases to ensure documentation is lean and relevant

## Process
1. **Scan:** Outdated/redundant documentation, deprecated features, duplicate information, historical content, migration notes, quality validation needs
2. **Draft:** Mark for removal/archiving, consolidation plans, historical content removal strategy, removal rationale, quality assessment
3. **Ask:** Confirm safe removal, verify obsolescence, clarify historical value, validate historical relevance, validate quality standards
4. **Sync:** Remove/archive content, eliminate historical artifacts, update cross-references, maintain coherence, ensure quality standards

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Streamlined relevant documentation
- Removed deprecated references
- **Eliminated historical artifacts** (migration notes, legacy references, outdated changelogs)
- **Removed irrelevant historical content** (old version notes, deprecated workflows, obsolete procedures)
- Archived valuable historical information (if needed)
- Improved maintainability
- Reduced cognitive load
- Clearer focus on current functionality
- **Quality-validated remaining content**
- **Ensured documentation meets standards before finalization**

## Related Passes
Synchronization → **Prune** → Reverse

## Historical Content Removal

### Target Historical Artifacts
**Migration Notes and Legacy References:**
- Migration instructions for deprecated systems
- Legacy file naming conventions and references
- Outdated architectural decisions and rationale
- Historical workflow descriptions no longer in use

**Version History and Changelogs:**
- Detailed version histories for internal tools/frameworks
- Extensive changelog entries for minor internal changes
- Historical DDD pass execution logs (keep only recent/relevant)
- Old feature development timelines and milestones

**Obsolete Procedures and Workflows:**
- Deprecated development workflows
- Outdated quality standards and procedures
- Historical team structure and role definitions
- Legacy tool configurations and setup instructions

**Outdated References:**
- References to deprecated tools, systems, or platforms
- Historical business context no longer relevant
- Old stakeholder information and contact details
- Superseded technical specifications

### Preservation Guidelines
**Keep Historical Content When:**
- Required for compliance or audit purposes
- Contains valuable lessons learned or decision rationale
- Provides context for current architectural decisions
- Documents breaking changes that affect current users

**Remove Historical Content When:**
- No longer relevant to current project state
- Increases cognitive load without providing value
- References deprecated/removed systems or processes
- Contains outdated information that could mislead users

### Historical Content Removal Process
1. **Identify:** Scan for migration notes, version histories, legacy references
2. **Evaluate:** Assess current relevance and value
3. **Preserve:** Archive truly valuable historical context (if needed)
4. **Remove:** Delete irrelevant historical artifacts
5. **Update:** Fix any broken references or dependencies

## Example Commit Message
`DDD: Prune Pass - Removed deprecated authentication docs, migration notes, and historical artifacts`
