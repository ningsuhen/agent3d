# Architecture

This document outlines the architecture of the Agent3D documentation framework.

## System Overview

Agent3D is a **documentation-only** framework that defines documentation-driven development principles for LLM coding agents. The framework consists of documentation components that work together to provide a comprehensive guideline system that ensures documentation remains the single source of truth throughout the development process.

```mermaid
graph TD
    A[Agent] -->|Follows| B[Agent Guidelines]
    B -->|Implements| C[DDD Passes]
    C -->|Creates/Updates| D[Documentation]
    C -->|Creates/Updates| E[Code]
    D -->|Guides| E
    F[Language Rules] -->|Informs| E
```

## Core Components

### Agent Guideline Protocol

The Agent Guideline Protocol is the mechanism by which LLM agents retrieve, cache, and follow the DDD guidelines.

```mermaid
sequenceDiagram
    participant Agent
    participant Local Cache
    participant Remote Repo

    Agent->>Remote Repo: Initial Guideline Acquisition
    Remote Repo-->>Agent: AGENT-GUIDELINES.md
    Agent->>Local Cache: Store as .agent-guidelines.md

    loop Every 6 hours
        Agent->>Remote Repo: Check for updates
        Remote Repo-->>Agent: Updated guidelines (if any)
        Agent->>Local Cache: Update if changed
    end

    Agent->>Local Cache: Reference for all actions
```

### DDD Pass System

The DDD Pass System provides a structured approach to documentation-driven development through a series of passes.

```mermaid
graph LR
    A[Foundation Pass] --> B[Documentation Pass]
    B --> C[Implementation Pass]
    C --> D[Testing Pass]
    D --> E[Refactoring Pass]
    E --> F[Code Review Pass]
    F --> G[Synchronization Pass]
    G --> H[Quality Pass]
    H --> I[Prune Pass]

    J[Full Pass] -.-> A
    J -.-> B
    J -.-> C
    J -.-> D
    J -.-> E
    J -.-> F
    J -.-> G
    J -.-> H
    J -.-> I
```

Each pass follows the Scan → Draft → Ask → Sync workflow:

```mermaid
graph LR
    A[Scan] --> B[Draft]
    B --> C[Ask]
    C --> D[Sync]
```

### Language-Specific Rules

Language-specific rules provide tailored guidelines for different programming languages:

```mermaid
graph TD
    A[Language Rules] --> B[Python]
    A --> C[JavaScript]
    A --> D[Java]
    A --> E[Go]

    B --> B1[Environment Setup]
    B --> B2[Code Style]
    B --> B3[Testing]

    C --> C1[Environment Setup]
    C --> C2[Code Style]
    C --> C3[Testing]

    D --> D1[Environment Setup]
    D --> D2[Code Style]
    D --> D3[Testing]

    E --> E1[Environment Setup]
    E --> E2[Code Style]
    E --> E3[Testing]
```

## Data Flow

The following diagram illustrates the data flow in the Agent3D framework:

```mermaid
graph TD
    A[Agent] -->|Reads| B[AGENT-GUIDELINES.md]
    A -->|Executes| C[DDD Pass]
    C -->|Updates| D[Documentation]
    C -->|Creates/Updates| E[Code]
    C -->|Verifies| F[Tests]
    A -->|Follows| G[Language Rules]
    A -->|Creates| H[PR/Commit]
```

## Directory Structure

```
agent3d/
├── AGENT-GUIDELINES.md    # Main guidelines document
├── README.md              # Project overview
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── docs/                  # Documentation directory
│   ├── FEATURES.md        # Feature specifications
│   ├── ARCHITECTURE.md    # This document
│   ├── TASKS.md           # Project backlog
│   ├── TEST-CASES.md      # Test case specifications
│   └── DEPLOYMENT.md      # Deployment instructions
├── passes/                # DDD passes documentation
│   └── simplified/        # Simplified pass definitions
│       ├── full_pass.md   # Full pass documentation
│       ├── 1_foundation_pass.md
│       ├── 2_documentation_pass.md
│       └── ...            # Other numbered passes
└── rules/                 # Language-specific rules documentation
    ├── python.md          # Python rules
    ├── javascript.md      # JavaScript rules
    ├── java.md            # Java rules
    └── go.md              # Go rules
```

**Note:** This repository contains only documentation files. There are no implementation files, libraries, or executable code. All examples are provided as documentation examples only and are not meant to be functional.
