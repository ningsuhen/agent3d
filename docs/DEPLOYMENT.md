# Deployment

This document outlines how to reference and use the Agent3D documentation framework.

## Overview

Agent3D is **exclusively a documentation framework** and doesn't have any code to deploy. It's designed to be referenced remotely by LLM coding agents through the Agent Guideline Protocol.

## Integration Methods

### Method 1: Direct URL Reference

The simplest integration method is to have the LLM agent directly reference the Agent3D guidelines URL:

```
https://raw.githubusercontent.com/ningsuhen/agent3d/main/AGENT-GUIDELINES.md
```

This approach requires the agent to have internet access but ensures it always has the latest guidelines.

### Method 2: Local Cache with Periodic Updates

For better performance and offline capability, implement the full Agent Guideline Protocol:

1. Initial retrieval of guidelines
2. Local caching as `.agent-guidelines.md`
3. Periodic checking for updates (e.g., every 6 hours)
4. Updating local cache when remote guidelines change

## CI/CD Integration

To enforce documentation-code alignment in CI/CD pipelines:

1. Add a pre-commit hook that verifies documentation updates for code changes
2. Implement a CI check that validates documentation completeness
3. Add a documentation drift detector that fails the build if code and docs are misaligned

Example GitHub Actions workflow:

```yaml
name: Documentation Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check for documentation updates
        run: |
          # Script to check if code changes have corresponding doc changes
          # or are tagged with docs-n/a

      - name: Validate documentation completeness
        run: |
          # Script to ensure all required documentation exists

      - name: Check for documentation-code alignment
        run: |
          # Script to verify documentation accurately reflects code
```

## Implementation in LLM Agents

Since Agent3D is a documentation-only framework, there's no code to set up or deploy. Instead, LLM agents should be instructed to:

1. Reference the Agent3D guidelines remotely
2. Follow the documented DDD passes
3. Adhere to the language-specific rules

### Example Agent Instructions

Here's an example of how to instruct an LLM agent to use Agent3D:

```
As an AI coding assistant, you should follow the Agent3D Documentation-Driven Development guidelines:

1. Always retrieve and reference the latest guidelines from:
   https://raw.githubusercontent.com/ningsuhen/agent3d/main/AGENT-GUIDELINES.md

2. Follow the DDD passes in sequence:
   - Foundation Pass
   - Documentation Pass
   - Implementation Pass
   - Testing Pass
   - Refactoring Pass
   - Code Review Pass
   - Synchronization Pass
   - Quality Pass
   - Prune Pass

3. Adhere to the language-specific rules for the project's programming language.

4. Remember the core principle: "Write the docs, then write the code—keep it lean, test it for real."
```

### Language-Specific Rules

The Agent3D guidelines include rules for several programming languages. When instructing an LLM agent, you should direct it to follow the appropriate language-specific rules based on your project:

- Python: https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/python.md
- JavaScript: https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/javascript.md
- Java: https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/java.md
- Go: https://raw.githubusercontent.com/ningsuhen/agent3d/main/rules/go.md

## Monitoring and Logging

For agents implementing the Agent Guideline Protocol:

1. Log guideline retrieval attempts and successes/failures
2. Track guideline version changes
3. Monitor documentation-code alignment metrics
4. Log DDD pass executions and outcomes

## Rollback Procedure

If issues arise with new guideline versions:

1. Revert to a previous version of the guidelines
2. Update the local cache with the stable version
3. Implement a version pinning mechanism if needed
