# Refactoring Pass

**Purpose:** Code structure improvement without changing functionality, LLM-focused compression, DRY compliance.

**Role:** **Senior Software Engineer** - refactoring techniques, performance optimization, technical debt management.

## When to Use

After implementation/testing, technical debt accumulation, before new features, performance needs, maintenance cycles, major releases.

## Process

1. **Scan:** Repository-wide DRY audit, modularization opportunities, LLM compression targets
2. **Draft:** Consolidation plan, DRY implementation strategy, compression approach
3. **Ask:** Structural changes approval, priority alignment, breaking change discussion
4. **Sync:** Incremental implementation, duplication elimination, testing verification (mark ✅)

## Outcomes

- Repository optimization, documentation clarity, LLM-optimized content
- DRY compliance, improved maintainability, modular architecture
- Performance improvements, preserved functionality, enhanced clarity, consistent structure

**Commit:** `DDD: Refactoring Pass - Improved authentication service performance and reduced code complexity`

## Focus Areas

**Repository-Wide:** File consolidation, directory structure optimization, cross-repository consistency
**Horizontal Merging:** Merge files with overlapping content (language rules + review guidelines, similar templates, redundant documentation), consolidate related functionality into single comprehensive files, eliminate duplicate information across merged files
**DRY Implementation:** Code/documentation/configuration deduplication, template optimization
**Modularization:** Component separation, logical grouping, interface simplification, dependency optimization
**Code Quality:** Complexity reduction, performance optimization, naming improvements, error handling consistency
**Documentation:** Clarity improvement, LLM-focused compression, test consolidation, language compliance, cross-reference optimization
**LLM Compression:** Apply rules from `~/.agent3d/rules.yml/markdown.yml` (LLM processing) or `~/.agent3d/rules/markdown.md` (human reference), remove basic task explanations, command simplification, essential information only

## Guidelines

**Standards:** Follow [Common Procedures - Quality Standards](../docs/COMMON-PROCEDURES.md#quality-standards)
**Principles:** DRY enforcement, incremental changes, functionality preservation, performance mindset
**Horizontal Merging:** Merge files with overlapping purposes (e.g., language rules + review guidelines), maintain logical separation between different concerns, preserve essential functionality, ensure comprehensive coverage in merged files
**LLM Compression:** See [Language-Specific Rules](../../AGENT-GUIDELINES.md#language-specific-rules) - assume LLM competency, command-centric, project-specific focus
