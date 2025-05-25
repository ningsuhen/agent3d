# Markdown Development Rules

**Language:** Markdown  
**Purpose:** Documentation-focused development with LLM optimization  
**Scope:** Documentation projects, technical writing, and LLM-consumed content  

## Core Principles

### Documentation-First Development
- Markdown is the implementation, not just documentation
- Structure and clarity are paramount
- Consistency across all documentation files
- LLM-optimized content for agent consumption

### Content Philosophy
- **Assume LLM Competency:** Remove verbose explanations of standard tools and practices
- **Command-Centric:** Provide exact commands and syntax, minimal explanation
- **Project-Specific Focus:** Emphasize unique procedures and configurations
- **Brevity with Context:** Maintain necessary context without verbosity

## File Structure Standards

### Naming Conventions
- Use kebab-case for file names: `user-guide.md`, `api-reference.md`
- Use descriptive, specific names: `github-integration.md` not `integration.md`
- Prefix numbered sequences: `1_foundation_pass.md`, `2_documentation_pass.md`
- Use `.template.md` suffix for templates

### Directory Organization
```
docs/
├── README.md                    # Project overview
├── REQUIREMENTS.md              # Functional requirements
├── designs/                     # Component specifications
├── proposals/                   # Feature proposals
└── guides/                      # User guides
```

### File Headers
Every markdown file should start with:
```markdown
# Document Title

**Purpose:** Brief description of document purpose
**Audience:** Target audience (developers, LLMs, users)
**Last Updated:** YYYY-MM-DD
```

## Content Structure Rules

### Heading Hierarchy
- Use consistent heading levels: `#` → `##` → `###`
- No skipping levels: Don't go from `#` to `###`
- Use descriptive headings that work as standalone navigation
- Maximum 4 heading levels for readability

### Lists and Organization
- Use `-` for unordered lists (consistent bullet style)
- Use `1.` for ordered lists (auto-numbering)
- Nest lists with 2-space indentation
- Use task lists `- [ ]` for actionable items

### Code Blocks and Commands
- Always specify language for syntax highlighting: ````markdown` not ````
- Use `bash` for shell commands, not `sh` or `shell`
- Include exact commands without verbose explanations
- Use inline code for file names, variables, and short commands

## LLM Optimization Rules

### Content Compression
- **Remove Basic Explanations:** Assume knowledge of git, npm, standard tools
- **Focus on Specifics:** Keep project-specific details and exact commands
- **Eliminate Redundancy:** Don't repeat information available elsewhere
- **Command-First:** Lead with the command, minimal context

### Examples of Compression
**Before (Verbose):**
```markdown
To create a new branch, you need to use git checkout with the -b flag. 
This will create and switch to a new branch. Run the following command 
where feature-name should be descriptive of your changes:
```

**After (LLM-Optimized):**
```markdown
Create feature branch:
```bash
git checkout -b feature-name
```

### Information Hierarchy
1. **Essential Commands:** Always include exact syntax
2. **Project Context:** Keep project-specific configurations
3. **Critical Warnings:** Preserve important constraints
4. **Standard Procedures:** Compress to command-only format

## Link and Reference Standards

### Internal Links
- Use relative paths: `[Guide](../guides/setup.md)` not absolute URLs
- Link to specific sections: `[Setup Process](setup.md#installation)`
- Verify all links during documentation passes
- Use descriptive link text, not "click here"

### External Links
- Use reference-style links for repeated URLs
- Include link validation in testing
- Prefer stable, official documentation links
- Archive important external content when possible

## Template Integration

### Template Usage
- All documents should derive from appropriate templates
- Replace all `{{placeholders}}` with actual content
- Remove `<template>` and `<example>` tags before finalizing
- Follow template structure exactly for consistency

### Template Variables
Common variables across markdown documents:
- `{{project_name}}` - Project name
- `{{document_title}}` - Document title
- `{{creation_date}}` - Creation timestamp
- `{{author}}` - Document author

## Quality Standards

### Content Quality
- **Clarity:** Every sentence should have clear purpose
- **Accuracy:** All commands and procedures must be tested
- **Completeness:** Cover all necessary information without excess
- **Consistency:** Use same terminology and format throughout

### Technical Accuracy
- Test all commands and procedures
- Verify all links and references
- Ensure code examples are functional
- Validate against actual implementation

### LLM Readability
- Use clear, unambiguous language
- Structure information hierarchically
- Provide context without verbosity
- Focus on actionable information

## Documentation Types

### Process Documentation
- Focus on step-by-step procedures
- Use numbered lists for sequential steps
- Include verification steps
- Compress standard tool usage

### Reference Documentation
- Organize information for quick lookup
- Use consistent formatting for similar items
- Include examples for complex concepts
- Minimize explanatory text

### Guide Documentation
- Balance completeness with brevity
- Assume reader competency with basics
- Focus on project-specific procedures
- Include troubleshooting for common issues

## Validation Rules

### Automated Checks
- Markdown linting (markdownlint)
- Link validation
- Spell checking
- Template compliance

### Manual Review
- Content accuracy verification
- LLM optimization review
- Cross-reference validation
- Consistency checking

## Common Anti-Patterns

### Avoid These Patterns
- **Over-explanation:** Don't explain basic development concepts
- **Redundant Information:** Don't repeat content from other documents
- **Verbose Commands:** Don't include installation instructions for standard tools
- **Inconsistent Structure:** Don't deviate from established patterns
- **Broken Links:** Don't leave unvalidated references

### Preferred Alternatives
- **Concise Commands:** Provide exact syntax with minimal context
- **Cross-References:** Link to detailed information instead of repeating
- **Assumed Knowledge:** Build on standard development knowledge
- **Consistent Patterns:** Follow established documentation structure

---

**Usage:** Apply these rules during Documentation Pass, Refactoring Pass, and Code Review Pass for all markdown content.
