# Common DDD Procedures

This document centralizes all common procedures used across DDD passes to eliminate duplication and ensure consistency.

## LLM Speed Optimization

### Memory-First Execution
**Purpose:** Minimize file lookups by memorizing critical patterns and structures

**Critical Requirement:** MEMORIZE these patterns to avoid repeated file access during execution

**Core Memory Patterns:**
1. **Pass Execution (Universal):** SCAN → DRAFT → ASK → SYNC
2. **Pass Sequence:** REQ → FOUND → DOC → PLAN → IMPL → TEST → REFACT → REVIEW → SYNC → QUAL → PRUNE → REV
3. **File Locations:** CONFIG(.agent3d-config.yml), DOCS(docs/), PLANS(docs/plans/), RULES(~/.agent3d/rules/), TEMPLATES(~/.agent3d/templates/)
4. **Quality Gates:** Requirements(objectives), Foundation(config), Documentation(criteria), Planning(checkpoints), Implementation(matches), Testing(passes), Review(rules)

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
1. `git -C ~/.agent3d pull origin main`
2. Access `~/.agent3d/templates/`
3. Replace {{placeholders}}
4. Remove template tags
5. Validate against checklist

### Template Path Pattern
**Location:** `~/.agent3d/templates/`
**Pattern:** `{DOCUMENT-NAME}.template.md`
**Examples:** `FEATURES.template.md`, `HIGH-LEVEL-DESIGN.template.md`

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
- **Exception Handling:** Proper handling throughout
- **Memory Efficiency:** Efficient patterns used
- **Test Coverage:** Comprehensive coverage required
- **Security:** Best practices followed
- **Performance:** Considerations addressed
- **Documentation:** Updated with code changes
- **Technical Debt:** Zero tolerance

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

## Planning Document Management

### Implementation Plan Creation
**Location:** `docs/plans/`
**Template:** `~/.agent3d/templates/IMPLEMENTATION-PLAN.template.md`
**Naming Convention:** `IMPLEMENTATION-PLAN-{feature-name}.md`

### Planning Document Lifecycle
1. **Creation:** Planning Pass creates detailed implementation plan
2. **Validation:** Plan reviewed and approved before Implementation Pass
3. **Execution:** Implementation Pass follows plan steps and updates progress
4. **Completion:** Plan marked as completed when all steps finished
5. **Archive:** Completed plans moved to `docs/plans/completed/` for reference

### Checkpoint Management
- **Checkpoint Frequency:** Every 2-4 implementation steps
- **Progress Tracking:** Mark steps as `[x]` completed, `[~]` in progress, `[ ]` not started
- **Rollback Points:** Clear instructions for reverting to previous checkpoint
- **Resumability:** Use checkpoint status to resume work after interruption

### Planning Triggers
**Automatic triggers for Planning Pass:**
- Changes affecting >3 components/files
- Estimated effort >8 hours
- Risk level "Medium" or "High"
- Dependencies on external systems
- Breaking changes or migrations

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
- `docs/plans/` - Implementation plans for major changes
- `docs/ux/` - UI/UX specifications, wireframes, and user flows (for UI projects)

### File Organization
- Core documentation in `docs/` root
- Specialized designs in `docs/designs/`
- Future proposals in `docs/proposals/`
- Implementation plans in `docs/plans/`
- UI/UX documentation in `docs/ux/`
- Pass documentation in `passes/simplified/`
- Templates in `templates/`
- Language rules in `rules/`

## Quality Standards

### Documentation Quality
- **Clarity:** Simple, direct language
- **Completeness:** Cover requirements and edge cases
- **Consistency:** Follow established patterns
- **Traceability:** Link requirements → features → tests
- **Maintainability:** Keep docs current

### Validation Requirements
- All links functional and current
- No template tags in final documentation
- Consistent formatting and structure
- Complete placeholder replacement
- Proper heading hierarchy

## GitHub Integration

### Pull Request Operations
**See [GitHub CLI Integration Guide](GITHUB-CLI-INTEGRATION.md).**

**Key Capabilities:**
- Automated PR detection
- Pending mode review comments
- Human-agent collaborative workflow
- Fallback support

**Usage in DDD Passes:**
- Code Review Pass: Automated comments
- Other passes: PR status updates
- All passes: Context-aware behavior

---

**Usage:** Reference this document from all DDD passes to eliminate duplication and ensure consistency.
