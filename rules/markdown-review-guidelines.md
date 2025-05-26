# Markdown Code Review Guidelines

**Purpose:** Review criteria for markdown documentation with focus on LLM optimization and technical accuracy
**Scope:** All markdown files in documentation projects
**Role:** Technical Documentation Specialist and LLM Content Optimizer

## Review Priorities

### Critical Issues (Must Fix)
1. **Broken Links:** All internal and external links must be functional
2. **Template Compliance:** Documents must follow template structure exactly
3. **Command Accuracy:** All commands and code examples must be tested and functional
4. **Structural Consistency:** Heading hierarchy and organization must be correct

### High Priority Issues
1. **LLM Optimization:** Remove verbose explanations of standard development tasks
2. **Content Redundancy:** Eliminate duplicate information across documents
3. **Missing Context:** Ensure sufficient context for task completion
4. **Inconsistent Terminology:** Use consistent terms throughout documentation

### Medium Priority Issues
1. **Formatting Consistency:** Standardize code blocks, lists, and emphasis
2. **Link Organization:** Optimize internal linking and cross-references
3. **Content Organization:** Improve information hierarchy and flow
4. **Language Clarity:** Enhance readability and precision

## LLM Optimization Review

### Content Compression Checklist
- [ ] **Basic Tool Explanations:** Remove installation and basic usage instructions for standard tools
- [ ] **Verbose Command Descriptions:** Replace with concise command-first format
- [ ] **Redundant Context:** Eliminate unnecessary background information
- [ ] **Standard Procedures:** Compress to essential commands and parameters

### Compression Examples to Look For

**❌ Verbose (Fix Required):**
```markdown
To leave a comment on a pull request using GitHub CLI, you first need to
install the gh command line tool using your package manager, then authenticate
with your GitHub account using `gh auth login`, and finally use the command
`gh pr comment <number> --body "your comment"` to add your comment.
```

**✅ LLM-Optimized (Correct):**
```bash
gh pr comment <number> --body "comment"
```

### What to Preserve
- **Exact Commands:** Keep complete command syntax
- **Project-Specific Details:** Maintain unique configurations and procedures
- **Critical Warnings:** Preserve important constraints and limitations
- **File Paths:** Keep exact paths and naming conventions

### What to Remove
- **Installation Instructions:** For standard development tools
- **Basic Explanations:** Of widely-known development concepts
- **Step-by-Step Breakdowns:** Of common operations
- **Verbose Descriptions:** Of standard tool functionality

## Technical Accuracy Review

### Command Verification
- [ ] **Syntax Accuracy:** All commands use correct syntax and parameters
- [ ] **Path Validity:** File paths and references are accurate
- [ ] **Version Compatibility:** Commands work with specified tool versions
- [ ] **Environment Assumptions:** Commands work in documented environments

### Link Validation
- [ ] **Internal Links:** All relative links resolve correctly
- [ ] **External Links:** All external URLs are accessible and current
- [ ] **Anchor Links:** Section references work correctly
- [ ] **Cross-References:** Document references are accurate

### Code Example Review
- [ ] **Functional Examples:** All code examples execute successfully
- [ ] **Complete Examples:** Examples include all necessary context
- [ ] **Syntax Highlighting:** Proper language specification for code blocks
- [ ] **Consistent Style:** Code formatting follows project standards

## Structure and Organization Review

### Document Structure
- [ ] **Heading Hierarchy:** Proper H1 → H2 → H3 progression
- [ ] **Logical Flow:** Information organized in logical sequence
- [ ] **Section Balance:** Appropriate content distribution across sections
- [ ] **Navigation Clarity:** Headings work as standalone navigation

### Content Organization
- [ ] **Information Hierarchy:** Most important information first
- [ ] **Logical Grouping:** Related information grouped together
- [ ] **Clear Separation:** Distinct topics properly separated
- [ ] **Consistent Patterns:** Similar content follows same structure

### Template Compliance
- [ ] **Required Sections:** All template sections present
- [ ] **Placeholder Replacement:** All `{{variables}}` replaced with actual content
- [ ] **Tag Removal:** No `<template>` or `<example>` tags in final document
- [ ] **Format Adherence:** Document follows template format exactly

## Language and Style Review

### Clarity and Precision
- [ ] **Clear Language:** Unambiguous, precise terminology
- [ ] **Active Voice:** Prefer active over passive voice
- [ ] **Concise Expression:** Remove unnecessary words and phrases
- [ ] **Consistent Terminology:** Same terms used throughout

### LLM-Friendly Writing
- [ ] **Command-Centric:** Lead with commands, minimal explanation
- [ ] **Assumed Competency:** Build on standard development knowledge
- [ ] **Context Efficiency:** Provide necessary context without verbosity
- [ ] **Actionable Focus:** Emphasize what to do, not how tools work

### Formatting Standards
- [ ] **Code Formatting:** Consistent inline code and code block usage
- [ ] **List Formatting:** Consistent bullet and numbering styles
- [ ] **Emphasis Usage:** Appropriate use of bold, italic, and code formatting
- [ ] **Line Length:** Reasonable line lengths for readability

## Quality Assurance Checklist

### Pre-Review Validation
- [ ] **Markdown Linting:** Document passes markdownlint validation
- [ ] **Spell Check:** No spelling errors or typos
- [ ] **Grammar Check:** Proper grammar and sentence structure
- [ ] **Link Check:** All links validated and functional

### Content Review
- [ ] **Accuracy Verification:** All information is current and correct
- [ ] **Completeness Check:** All necessary information included
- [ ] **Redundancy Elimination:** No duplicate information
- [ ] **Gap Identification:** No missing critical information

### LLM Optimization Review
- [ ] **Compression Applied:** Verbose explanations removed appropriately
- [ ] **Essential Information Preserved:** Critical details maintained
- [ ] **Command Clarity:** All commands clear and executable
- [ ] **Context Sufficiency:** Adequate context for task completion

## Review Comments Format

### Comment Structure
Use this format for review comments:

```
**[PRIORITY]** [CATEGORY]: [DESCRIPTION]

**Issue:** [Specific problem description]
**Suggestion:** [Recommended fix]
**Example:** [If applicable, show before/after]
```

### Priority Levels
- **CRITICAL:** Broken functionality, must fix before merge
- **HIGH:** Significant improvement needed, should fix
- **MEDIUM:** Enhancement opportunity, consider fixing
- **LOW:** Minor improvement, optional fix

### Category Tags
- **LLM-OPT:** LLM optimization issue
- **ACCURACY:** Technical accuracy problem
- **STRUCTURE:** Organization or formatting issue
- **CLARITY:** Language or readability concern
- **CONSISTENCY:** Inconsistency with standards

## Common Review Patterns

### Frequent Issues
1. **Over-explanation of basic tools** (git, npm, standard CLIs)
2. **Broken internal links** after file reorganization
3. **Inconsistent code block language specification**
4. **Template placeholders not replaced**
5. **Redundant information across multiple documents**

### Quick Fixes
1. **Command compression:** Remove verbose explanations, keep commands
2. **Link updates:** Fix relative paths after file moves
3. **Language specification:** Add proper language tags to code blocks
4. **Placeholder replacement:** Replace all template variables
5. **Cross-reference cleanup:** Remove duplicate content, add links

---

**Usage:** Apply during Code Review Pass for all markdown documentation. Focus on LLM optimization while maintaining technical accuracy and completeness.
