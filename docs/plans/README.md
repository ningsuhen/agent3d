# Implementation Plans Directory

This directory contains step-by-step implementation plans created by the Planning Pass for major changes, migrations, refactoring, and complex features.

## Directory Structure

```
docs/plans/
├── README.md                           # This file
├── completed/                          # Archived completed plans
│   └── IMPLEMENTATION-PLAN-{feature}.md
└── IMPLEMENTATION-PLAN-{feature}.md    # Active implementation plans
```

## File Naming Convention

**Active Plans:** `IMPLEMENTATION-PLAN-{feature-name}.md`
**Completed Plans:** Moved to `completed/` subdirectory

## When Plans Are Created

Implementation plans are automatically created by the Planning Pass when:

- **Major Changes:** Migrations, refactoring, architecture changes
- **Complex Features:** Multi-component features, external integrations
- **High Risk Changes:** Breaking changes, backward-incompatible updates
- **Large Scope:** Changes affecting >3 components/files
- **Extended Timeline:** Estimated effort >8 hours

## Plan Lifecycle

1. **Creation:** Planning Pass creates detailed implementation plan
2. **Validation:** Plan reviewed and approved before Implementation Pass
3. **Execution:** Implementation Pass follows plan steps and updates progress
4. **Completion:** Plan marked as completed when all steps finished
5. **Archive:** Completed plans moved to `completed/` for reference

## Plan Structure

Each implementation plan includes:

- **Executive Summary:** High-level overview and objectives
- **Scope and Dependencies:** What's included/excluded, external requirements
- **Risk Assessment:** Potential issues and mitigation strategies
- **Step-by-Step Execution Plan:** Detailed implementation steps with checkpoints
- **Rollback Strategy:** How to undo changes at each checkpoint
- **Validation Criteria:** Success criteria for each step
- **Timeline and Effort:** Estimated duration and resource requirements

## Checkpoint System

Plans include checkpoints every 2-4 steps that provide:

- **Progress Tracking:** Clear markers of completion
- **Rollback Points:** Safe points to revert changes
- **Resumability:** Ability to continue work after interruption
- **Validation Gates:** Criteria that must be met before proceeding

## Usage by Implementation Pass

The Implementation Pass uses these plans to:

1. **Validate Plan Exists:** Check for required implementation plan
2. **Follow Step Sequence:** Execute steps in planned order
3. **Update Progress:** Mark steps as completed in the plan
4. **Respect Checkpoints:** Validate criteria before proceeding
5. **Handle Failures:** Use rollback instructions if issues arise
6. **Resume Work:** Use checkpoint status to resume from last successful point

## Template

New implementation plans are created using:
`~/.agent3d/templates/IMPLEMENTATION-PLAN.template.md`

## Related Documentation

- [Planning Pass](../../passes/simplified/3_planning_pass.md) - Creates implementation plans
- [Implementation Pass](../../passes/simplified/4_implementation_pass.md) - Executes implementation plans
- [Common Procedures](../COMMON-PROCEDURES.md#planning-document-management) - Planning document management procedures
