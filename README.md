# Agent3D - Documentation-Driven Development Guidelines for LLM Coding Agents

Agent3D is a **documentation-only** framework that defines Documentation-Driven Development (DDD) principles specifically for Large Language Model (LLM) coding agents. It provides a structured approach to ensure documentation remains the single source of truth throughout the development process.

## Important Note

**This project is purely a documentation project.** It does not contain any implementations, libraries, or code to import. Its sole purpose is to provide a standardized set of guidelines that LLM coding agents can reference remotely.

## Overview

Documentation-Driven Development is a methodology where documentation precedes and guides code implementation. Agent3D provides a structured approach to DDD through a series of "passes" that guide agents through the entire development lifecycle, from initial documentation to code implementation, testing, and maintenance.

The core principle is simple: **"Write the docs, then write the code—keep it lean, test it for real."**

## Key Features

- **LLM Speed Optimized**: Memory-first approach minimizes file lookups during execution
- **Memory-Cached Patterns**: SCAN→DRAFT→ASK→SYNC and language rules stored in LLM memory
- **Configuration-Centric**: Single `.agent3d-config.yml` file for project management
- **Documentation as Source of Truth**: Ensures code never outpaces documentation
- **Language-Specific Rules**: Memorizable patterns for Python, JavaScript, Java, Go, Markdown
- **Lean Code Principles**: Focused on implementing only what's documented

## How to Use

1. **Memorize Core Patterns**: Cache SCAN→DRAFT→ASK→SYNC and language rules
2. **Configure Project**: Run Foundation Pass to create `.agent3d-config.yml`
3. **Speed Execution**: Use memory-cached patterns to minimize file lookups
4. Follow DDD passes in sequence

## Agent Guideline Protocol

The Agent Guideline Protocol is the **entry point** for the Agent3D system. It contains the only hardcoded repository URL in the system, which is necessary since agents start without any repository access.

**Repository Access Flow:** `Agent Guideline Protocol` → `~/.agent3d`

```
**Agent Guideline Protocol**

Agent operational principles derived from the DDD Remote Repository.

1.  **Repository Setup:**
    * Clone repository: `git@github.com:ningsuhen/agent3d.git` to `~/.agent3d`
    * Use `~/.agent3d/AGENT-GUIDELINES.md` as main entry point

2.  **Guideline Operations:**
    * **Always** refer to `~/.agent3d/AGENT-GUIDELINES.md` for all decisions and actions
    * Update regularly with `git pull` in `~/.agent3d` directory

3.  **Synchronization:**
    * Pull latest changes: `cd ~/.agent3d && git pull`
    * Frequency: As needed or at regular intervals
```

### Repository Access Process

Simplified two-stage access pattern:

1. **Agent Guideline Protocol** - Entry point with repository URL
2. **Local Repository Clone** (`~/.agent3d`) - Full repository with AGENT-GUIDELINES.md, templates, and rules

**To Change Repository Source:** Update repository URL in Agent Guideline Protocol above

## DDD Passes

Agent3D defines a series of passes that guide the development process:

0. **Requirements Pass**: Documenting comprehensive requirements and business objectives
1. **Foundation Pass**: Project configuration and foundational setup
2. **Documentation Pass**: Documenting features, requirements, and priorities
3. **Implementation Pass**: Implementing features with basic test coverage
4. **Testing Pass**: Adding comprehensive tests and verifying edge cases
5. **Refactoring Pass**: Cleaning up code without changing functionality
6. **Code Review Pass**: Reviewing PR changes and providing feedback
7. **Synchronization Pass**: Aligning documentation with code at any scale
8. **Quality Pass**: Verifying and improving documentation quality
9. **Prune Pass**: Removing outdated or redundant content
10. **Reverse Pass**: Detecting and addressing reverse drift (implementation without documentation)

Additionally, a **Full Pass** encompasses all of the above passes for comprehensive project updates.

## Documentation Structure

### 📋 Core Documents
- **[AGENT-GUIDELINES.md](AGENT-GUIDELINES.md)**: Main guidelines for agents
- **[docs/BUSINESS-OBJECTIVES.md](docs/BUSINESS-OBJECTIVES.md)**: Business goals and success metrics
- **[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md)**: Functional and non-functional requirements
- **[docs/USER-STORIES.md](docs/USER-STORIES.md)**: User personas and story mapping
- **[docs/ACCEPTANCE-CRITERIA.md](docs/ACCEPTANCE-CRITERIA.md)**: Testable acceptance criteria
- **[docs/HIGH-LEVEL-DESIGN.md](docs/HIGH-LEVEL-DESIGN.md)**: System architecture overview
- **[docs/DDD-STATUS.md](docs/DDD-STATUS.md)**: Pass status and project health

### 🔄 DDD Passes
- **[Full Pass](passes/simplified/full_pass.md)**: Comprehensive project update
- **[Requirements Pass](passes/simplified/0_requirements_pass.md)**: Business requirements and objectives
- **[Foundation Pass](passes/simplified/1_foundation_pass.md)**: Project configuration and setup
- **[Documentation Pass](passes/simplified/2_documentation_pass.md)**: Feature documentation
- **[Implementation Pass](passes/simplified/3_implementation_pass.md)**: Code development
- **[Testing Pass](passes/simplified/4_testing_pass.md)**: Test coverage
- **[Refactoring Pass](passes/simplified/5_refactoring_pass.md)**: Code cleanup
- **[Code Review Pass](passes/simplified/6_code_review_pass.md)**: PR reviews
- **[Synchronization Pass](passes/simplified/7_synchronization_pass.md)**: Doc-code alignment
- **[Quality Pass](passes/simplified/8_quality_pass.md)**: Documentation quality
- **[Prune Pass](passes/simplified/9_prune_pass.md)**: Content cleanup
- **[Reverse Pass](passes/simplified/10_reverse_pass.md)**: Reverse drift detection

### 📁 Supporting Files
- **docs/designs/**: Component specifications ([Agent Protocol](docs/designs/AGENT-PROTOCOL.md), [DDD Passes](docs/designs/DDD-PASSES.md), [Language Rules](docs/designs/LANGUAGE-RULES.md))
- **docs/proposals/**: Unimplemented feature designs
- **rules/**: Language-specific development rules ([Python](rules/python.md), [JavaScript](rules/javascript.md), [Java](rules/java.md), [Go](rules/go.md))
- **templates/**: Documentation format specifications

### 🚀 Advanced Features
- **[Advanced Features Guide](docs/ADVANCED-FEATURES.md)**: Sophisticated capabilities and power-user features
- **[Configuration Guide](docs/CONFIGURATION-GUIDE.md)**: Customization and project-specific settings
- **[GitHub CLI Integration](docs/GITHUB-CLI-INTEGRATION.md)**: Automated PR review workflows



There are no implementation files, libraries, or code to import. The examples directory contains only documentation examples, not functional code.

## License

[MIT License](LICENSE)

## Contributing

Contributions to improve the documentation are welcome! Please feel free to submit a Pull Request with enhancements to the guidelines, passes, or rules.