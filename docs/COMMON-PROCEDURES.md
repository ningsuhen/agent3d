# Common DDD Procedures

This document centralizes all common procedures used across DDD passes to eliminate duplication and ensure consistency.

## Repository Management

### Repository Update
**Command:** `git -C ~/.agent3d pull origin main`
**Purpose:** Ensure local Agent3D repository is current before any DDD work
**Usage:** Execute at the start of every DDD pass

### Project Root Establishment
**Purpose:** Establish project root directory for all DDD documentation

**Process:**
1. **Search for `.agent3d` file**: Look for `.agent3d` file starting from current directory, traversing up parent directories
2. **If found**: Use the directory containing `.agent3d` as project root
3. **If not found**: Create `.agent3d` file in current working directory to establish project root
4. **Project Structure**: All DDD documentation should be relative to the directory containing `.agent3d`

**Example `.agent3d` file content:**
```
# Agent3D Project Root Marker
# This file marks the root directory for DDD documentation
# All documentation paths are relative to this directory
```

## Template System

### Template Access
**Location:** `~/.agent3d/templates/`
**Setup:** Clone repository to `~/.agent3d` (see AGENT3D_REPO in [AGENT-GUIDELINES.md](../AGENT-GUIDELINES.md#repository-configuration) for repository URL)

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
- **Heading Hierarchy:** Use `## Groups` and `### Sub-Groups` format for all documentation
- **Single-Line Entries:** Features, tasks, and test cases must be single-line entries
- **Sub-Items:** Use 2-space indentation for sub-components

#### Feature Completion Criteria
- **NEVER mark `[x]` completed** based solely on interface definitions, prototypes, or documentation
- **ONLY mark `[x]` completed** when verifiable evidence exists:
  - Automated tests that pass and validate functionality
  - Manual testing results confirming acceptance criteria
  - Demonstrable working implementation
- **Use `[~]` for in-progress** features with partial implementation but lacking verification

#### Template Compliance
- Replace ALL {{placeholders}} with actual content
- Remove all `<template>` and `<example>` tags from final documentation
- Follow format specifications exactly as defined in templates
- Ensure all required sections are present and complete

#### Quality Standards
- **Cross-References:** Ensure all links are functional and current
- **LLM-Friendly:** Use clear, concise language; consistent structure; no legacy references
- **Traceability:** Link requirements (REQ-####) to features to test cases (TC-####)

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
- [ ] Follow `## Groups` and `### Sub-Groups` heading structure
- [ ] Replace all {{placeholders}} with actual content
- [ ] Remove all `<template>` and `<example>` tags
- [ ] Ensure all links are functional and point to existing resources
- [ ] Use single-line entries for features, tasks, and test cases
- [ ] Mark `[x]` completed ONLY with verifiable evidence
- [ ] Use 2-space indentation for sub-items
- [ ] Maintain clear, concise, LLM-friendly language
- [ ] Include proper traceability links where applicable

## Language-Specific Rules

### Rule Access
**Location:** `~/.agent3d/rules/`
**Available Languages:** Python, JavaScript, Java, Go
**Review Guidelines:** Each language has corresponding `-review-guidelines.md` file

### Rule Application
1. Identify project programming language(s)
2. Load corresponding rules from `~/.agent3d/rules/[language].md`
3. Apply rules consistently throughout development activities
4. Reference review guidelines during code review processes

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
