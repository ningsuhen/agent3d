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

LLM agents should reference the Agent3D guidelines remotely and follow the documented DDD passes. See [AGENT-GUIDELINES.md](../AGENT-GUIDELINES.md) for complete instructions and language-specific rules.

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
