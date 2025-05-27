# Development Runs Directory

This directory contains execution plans for Development Pass runs.

## Directory Structure

```
docs/runs/
├── README.md                           # This file
├── EXEC-PLAN-{change-name}.md         # Active execution plans
├── completed/                         # Completed execution plans
│   └── EXEC-PLAN-{change-name}-{date}.md
└── failed/                           # Failed execution plans
    └── EXEC-PLAN-{change-name}-{date}.md
```

## File Naming Convention

**Active Plans:** `EXEC-PLAN-{change-name}.md`
**Completed Plans:** Moved to `completed/` subdirectory with date suffix
**Failed Plans:** Moved to `failed/` subdirectory for analysis

## Usage

Execution plans are created by the Development Pass and contain step-by-step instructions for implementing features, refactoring, migrations, or other development work.
