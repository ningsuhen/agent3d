# Agent3D - Documentation-Driven Development Framework for LLM Coding Agents

Agent3D is a comprehensive framework that implements Documentation-Driven Development (DDD) principles specifically designed for Large Language Model (LLM) coding agents. It ensures that documentation remains the single source of truth throughout the development process.

## Overview

Documentation-Driven Development is a methodology where documentation precedes and guides code implementation. Agent3D provides a structured approach to DDD through a series of "passes" that guide agents through the entire development lifecycle, from initial documentation to code implementation, testing, and maintenance.

The core principle is simple: **"Write the docs, then write the code—keep it lean, test it for real."**

## Key Features

- **Structured Development Process**: Clear, numbered passes from foundation to maintenance
- **Documentation as Source of Truth**: Ensures code never outpaces documentation
- **Language-Specific Rules**: Tailored guidelines for Python, JavaScript, Java, and Go
- **Lean Code Principles**: Focused on implementing only what's documented
- **Test-Driven Approach**: Emphasis on real tests over mocks

## Getting Started

To use Agent3D in your LLM agent:

1. Implement the Agent Guideline Protocol (see below)
2. Follow the DDD passes in sequence for each development task
3. Adhere to the language-specific rules for your project

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

Agent3D implements a series of passes that guide the development process:

1. **Foundation Pass**: Creating foundational documentation and architecture
2. **Documentation Pass**: Documenting features, requirements, and priorities
3. **Implementation Pass**: Implementing features with basic test coverage
4. **Testing Pass**: Adding comprehensive tests and verifying edge cases
5. **Refactoring Pass**: Cleaning up code without changing functionality
6. **Code Review Pass**: Reviewing PR changes and providing feedback
7. **Synchronization Pass**: Aligning documentation with code at any scale
8. **Quality Pass**: Verifying and improving documentation quality
9. **Prune Pass**: Removing outdated or redundant content

Additionally, a **Full Pass** encompasses all of the above passes for comprehensive project updates.

## Documentation

For detailed guidelines, refer to the [AGENT-GUIDELINES.md](AGENT-GUIDELINES.md) file.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.