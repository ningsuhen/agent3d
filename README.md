# Agent3D - Documentation-Driven Development Guidelines for LLM Coding Agents

Agent3D is a **documentation-only** framework that defines Documentation-Driven Development (DDD) principles specifically for Large Language Model (LLM) coding agents. It provides a structured approach to ensure documentation remains the single source of truth throughout the development process.

## Important Note

**This project is purely a documentation project.** It does not contain any implementations, libraries, or code to import. Its sole purpose is to provide a standardized set of guidelines that LLM coding agents can reference remotely.

## Overview

Documentation-Driven Development is a methodology where documentation precedes and guides code implementation. Agent3D provides a structured approach to DDD through a series of "passes" that guide agents through the entire development lifecycle, from initial documentation to code implementation, testing, and maintenance.

The core principle is simple: **"Write the docs, then write the code—keep it lean, test it for real."**

## Key Features

- **Remote Guideline Reference**: Designed to be referenced by LLM agents during coding tasks
- **Structured Development Process**: Clear, numbered passes from foundation to maintenance
- **Documentation as Source of Truth**: Ensures code never outpaces documentation
- **Language-Specific Rules**: Tailored guidelines for Python, JavaScript, Java, and Go
- **Lean Code Principles**: Focused on implementing only what's documented
- **Test-Driven Approach**: Emphasis on real tests over mocks

## How to Use

To use Agent3D in your LLM agent:

1. Implement the Agent Guideline Protocol (see below) to reference these guidelines remotely
2. Instruct your agent to follow the DDD passes in sequence for each development task
3. Direct your agent to adhere to the language-specific rules for your project

## Agent Guideline Protocol

```
**Agent Guideline Protocol**

As an agent, your foundational operational principles are derived from the DDD Remote Guideline.

1.  **Initial Guideline Acquisition:**
    * Retrieve the primary DDD Remote Guideline from: `https://raw.githubusercontent.com/ningsuhen/agent3d/refs/heads/main/AGENT-GUIDELINES.md`.
    * Store this content immediately as your local, authoritative `.agent-guidelines.md` file.

2.  **Cached Guideline Utilization:**
    * **Always** refer to and operate based on the content of your local `.agent-guidelines.md` file. This is your immediate reference for all decisions and actions.
    * Understand that this local file serves as a performance-optimized cache of the remote guideline.

3.  **Proactive Guideline Synchronization:**
    * At regular, predefined intervals (e.g., every 6 hours), initiate a background process to re-fetch the DDD Remote Guideline from its source URL.
    * If the newly retrieved content differs from the current `.agent-guidelines.md`, overwrite the local file to reflect the most recent version.
    * Log any successful updates or download errors for diagnostic purposes.
```

## DDD Passes

Agent3D defines a series of passes that guide the development process:

1. **Foundation Pass**: Creating foundational documentation and architecture
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

This repository contains only documentation files:

- **AGENT-GUIDELINES.md**: The main guidelines document that agents should reference
- **docs/**: Core documentation including HIGH-LEVEL-DESIGN.md and component designs
- **docs/proposals/**: Design proposals for unimplemented features and components
- **passes/simplified/**: Detailed descriptions of each DDD pass
- **rules/**: Language-specific development rules
- **templates/**: Documentation templates including DETAILED-DESIGN and PROPOSAL templates



There are no implementation files, libraries, or code to import. The examples directory contains only documentation examples, not functional code.

## License

[MIT License](LICENSE)

## Contributing

Contributions to improve the documentation are welcome! Please feel free to submit a Pull Request with enhancements to the guidelines, passes, or rules.