# Common DDD Procedures

This document centralizes all common procedures used across DDD passes to eliminate duplication and ensure consistency.

## LLM Speed Optimization

### Memory-First Execution
**Purpose:** Minimize file lookups by memorizing critical patterns and structures

**Critical Requirement:** MEMORIZE these patterns to avoid repeated file access during execution

**Core Memory Patterns:**
1. **Pass Execution (Universal):** SCAN → DRAFT → ASK → SYNC
2. **Pass Sequence:** REQ → FOUND → DOC → IMPL → TEST → REFACT → REVIEW → SYNC → QUAL → PRUNE → REV
3. **File Locations:** CONFIG(.agent3d-config.yml), DOCS(docs/), RULES(~/.agent3d/rules/), TEMPLATES(~/.agent3d/templates/)
4. **Quality Gates:** Requirements(objectives), Foundation(config), Documentation(criteria), Implementation(matches), Testing(passes), Review(rules)

**Speed Optimization Rules:**
- **NEVER** look up pass definitions during execution
- **CACHE** language rules in working memory
- **MINIMIZE** template file access
- **INTERNALIZE** validation patterns
- **MEMORIZE** decision trees for pass selection

**File Access Priority:**
1. **FIRST:** .agent3d-config.yml (project context)
2. **THEN:** Target documents (REQUIREMENTS.md, FEATURES.md, etc.)
3. **AVOID:** Repeated rule/template lookups
4. **CACHE:** Language patterns in memory

## Repository Management

### Repository Update
**Command:** `git -C ~/.agent3d pull origin main`
**Purpose:** Ensure local Agent3D repository is current before any DDD work
**Usage:** Execute at the start of every DDD pass

### Project Root Establishment (Speed Optimized)
**Purpose:** Quickly identify project root and cache context

**Fast Process:**
1. **Quick Search**: Look for `.agent3d-config.yml` in current directory, then parent directories
2. **Cache Location**: Store project root path in memory for session
3. **Load Config**: Read `.agent3d-config.yml` once and cache project context
4. **No Fallback**: If no config found, run Foundation Pass immediately

### Project Configuration Management
**Purpose:** Manage project-specific configuration and pass settings

**Configuration File:** `.agent3d-config.yml` in project root

**Process:**
1. **Check for existing config**: Look for `.agent3d-config.yml` in project root
2. **If not found**: Run Foundation Pass to create configuration through interactive setup
3. **Configuration scope**: Project type, language, enabled passes, quality standards
4. **Usage**: All DDD passes reference this configuration for project-specific behavior

## Template System

### Template Access
**Location:** `~/.agent3d/templates/`
**Setup:** Clone repository to `~/.agent3d` (see repository URL in README.md Agent Guideline Protocol)

### Template Usage Process
1. Update repository: `git -C ~/.agent3d pull origin main`
2. Access templates from `~/.agent3d/templates/`
3. Replace all {{placeholders}} with actual content
4. Remove template tags (`<template>`, `<example>`) before finalizing documentation
5. Validate against template checklist requirements

### Template Paths Reference
| Document | Template Path |
|----------|---------------|
| README.md | `~/.agent3d/templates/README.template.md` |
| docs/BUSINESS-OBJECTIVES.md | `~/.agent3d/templates/BUSINESS-OBJECTIVES.template.md` |
| docs/REQUIREMENTS.md | `~/.agent3d/templates/REQUIREMENTS.template.md` |
| docs/USER-STORIES.md | `~/.agent3d/templates/USER-STORIES.template.md` |
| docs/ACCEPTANCE-CRITERIA.md | `~/.agent3d/templates/ACCEPTANCE-CRITERIA.template.md` |
| docs/FEATURES.md | `~/.agent3d/templates/FEATURES.template.md` |
| docs/HIGH-LEVEL-DESIGN.md | `~/.agent3d/templates/HIGH-LEVEL-DESIGN.template.md` |
| docs/TASKS.md | `~/.agent3d/templates/TASKS.template.md` |
| docs/TEST-CASES.md | `~/.agent3d/templates/TEST-CASES.template.md` |
| docs/DDD-STATUS.md | `~/.agent3d/templates/DDD-STATUS.template.md` |
| docs/designs/*.md | `~/.agent3d/templates/DETAILED-DESIGN.template.md` |
| docs/proposals/*.md | `~/.agent3d/templates/PROPOSAL.template.md` |
| CHANGELOG.md | `~/.agent3d/templates/CHANGELOG.template.md` |

## Standard DDD Workflow

### Process Structure
All DDD passes follow the same 4-step workflow:

1. **Scan:** Assess current state and identify needs
2. **Draft:** Plan and prepare changes
3. **Ask:** Validate with stakeholders and clarify requirements
4. **Sync:** Implement changes and update documentation

### Progress Tracking
**Convention:** Mark completed steps with ✅ during execution

### Documentation Standards

#### Structure Requirements
- Use `## Groups` and `### Sub-Groups` heading hierarchy
- Single-line entries for features, tasks, test cases
- 2-space indentation for sub-items

#### Feature Completion Criteria
- Mark `[x]` ONLY with verifiable evidence (tests pass, manual verification)
- Use `[~]` for in-progress features
- NEVER mark complete based on interfaces/prototypes alone

#### Template Compliance
- Replace ALL {{placeholders}} with actual content
- Remove `<template>` and `<example>` tags
- Include all required sections

#### Quality Standards
- Functional links and cross-references
- Concise, LLM-friendly language
- Requirements-to-features-to-tests traceability

#### Universal Code Quality Standards
- **Exception Handling:** Proper exception handling throughout
- **Memory Efficiency:** Memory efficient patterns used
- **Test Coverage:** Comprehensive test coverage required
- **Security:** Security best practices followed
- **Performance:** Performance considerations addressed
- **Documentation:** Documentation must be updated with code changes
- **Technical Debt:** Zero tolerance for technical debt introduction

### Common Validation Checklist

**All Documentation Must:**
- [ ] Use `## Groups` / `### Sub-Groups` structure
- [ ] Replace {{placeholders}} and remove template tags
- [ ] Functional links and single-line entries
- [ ] Mark `[x]` only with verifiable evidence
- [ ] 2-space indentation for sub-items
- [ ] Concise, LLM-friendly language
- [ ] Proper traceability links

## Language-Specific Rules (Speed Optimized)

### Memory-Cached Patterns
**CRITICAL:** MEMORIZE these core patterns to avoid file lookups:

| Language | Key Patterns |
|----------|-------------|
| **Markdown** | LLM compression, command-first, no verbose explanations |
| **Python** | Type hints, docstrings, pytest, pyproject.toml, black formatting |
| **JavaScript** | ESLint, TypeScript preferred, Jest testing, modern ES6+ |
| **Java** | Spring patterns, JUnit, Maven/Gradle, SOLID principles |
| **Go** | gofmt, standard library preferred, table tests, idioms |

### Speed Optimization Rules
1. **Cache on First Use:** Load language rules once per session
2. **Memory Application:** Apply cached patterns without file access
3. **Quick Validation:** Use memorized quality gates
4. **No Repeated Lookups:** Store language patterns in working memory

**REFERENCE:** Full rules at [Language-Specific Rules](../AGENT-GUIDELINES.md#language-specific-rules)

## DDD Status Management

### Status Updates
**File:** `docs/DDD-STATUS.md`
**Template:** `~/.agent3d/templates/DDD-STATUS.template.md`
**Frequency:** After completing any DDD pass

### Status Tracking Elements
- **Pass Status:** Completed ✅, Pending ⏸️, In Progress 🔄, Skipped ⏭️
- **Alignment Percentage:** 0-100% with progress bar visualization
- **Drift Level:** None 🟢, Low 🟡, Medium 🟠, High 🔴
- **Health Indicators:** Critical issues, documentation gaps, implementation drift

## Directory Structure Standards

### Required Directories
- `docs/` - Main documentation directory
- `docs/designs/` - Component design specifications
- `docs/proposals/` - Design proposals for unimplemented features

### File Organization
- Core documentation in `docs/` root
- Specialized designs in `docs/designs/`
- Future proposals in `docs/proposals/`
- Pass documentation in `passes/simplified/`
- Templates in `templates/`
- Language rules in `rules/`

## Quality Standards

### Documentation Quality
- **Clarity:** Use simple, direct language
- **Completeness:** Cover all requirements and edge cases
- **Consistency:** Follow established patterns and naming
- **Traceability:** Link requirements to features to test cases
- **Maintainability:** Keep docs current with changes

### Validation Requirements
- All links functional and current
- No template tags in final documentation
- Consistent formatting and structure
- Complete placeholder replacement
- Proper heading hierarchy

## GitHub Integration

### Pull Request Operations
**For comprehensive GitHub CLI integration instructions, see [GitHub CLI Integration Guide](GITHUB-CLI-INTEGRATION.md).**

**Key Capabilities:**
- Automated PR detection and context awareness
- Pending mode review comment submission
- Human-agent collaborative review workflow
- Fallback support for manual processes

**Usage in DDD Passes:**
- Code Review Pass: Automated review comment submission
- Other passes: PR status updates and notifications
- All passes: Context-aware behavior when on PR branches

---

**Usage:** Reference this document from all DDD passes to eliminate duplication and ensure consistency.
