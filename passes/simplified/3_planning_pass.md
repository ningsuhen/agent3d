# Planning Pass

**Purpose:** Create detailed, step-by-step implementation plans with checkpoints for major changes, enabling tracking, resumability, and risk mitigation.

**Role:** **Technical Project Manager and Solution Architect** with expertise in project planning, risk assessment, and implementation strategy. Focus on breaking down complex changes into manageable, trackable steps with clear checkpoints and rollback strategies.

## When to Use

### Required for Major Changes
- **Migrations:** Database schema changes, platform migrations, framework upgrades
- **Refactoring:** Large-scale code restructuring, architecture changes
- **Complex Features:** Multi-component features, integration with external systems
- **Infrastructure Changes:** Deployment pipeline modifications, environment setup
- **Breaking Changes:** API modifications, backward-incompatible updates

### Optional for Minor Changes
- Single-file modifications
- Bug fixes with clear scope
- Documentation-only updates
- Configuration tweaks

### Automatic Triggers
Planning Pass is automatically triggered when Documentation Pass identifies:
- Changes affecting >3 components/files
- Dependencies on external systems
- Risk level marked as "Medium" or "High"
- Timeline >1 day estimated effort
- Rollback complexity marked as "Complex"

## Process

1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), review documentation, assess change complexity, identify dependencies and risks
2. **Draft:** Create step-by-step plan with checkpoints, define rollback strategies, estimate effort and timeline
3. **Ask:** Validate approach, confirm checkpoint strategy, clarify dependencies and constraints
4. **Sync:** Finalize implementation plan, update project documentation, prepare for Implementation Pass

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes

- **Implementation Plan Document** (`docs/plans/IMPLEMENTATION-PLAN-{feature-name}.md`)
- **Checkpoint Strategy** with clear rollback points
- **Risk Assessment** with mitigation strategies
- **Dependency Map** with external requirements
- **Timeline Estimation** with effort breakdown
- **Validation Criteria** for each step
- **Updated TASKS.md** with planned work items

## Related Passes

Requirements → Foundation → Documentation → **Planning** → Implementation → Testing

## Example Commit Message

`DDD: Planning Pass - Created implementation plan for user authentication system`

## Planning Document Structure

### Required Sections
1. **Executive Summary** - High-level overview and objectives
2. **Scope and Dependencies** - What's included/excluded, external requirements
3. **Risk Assessment** - Potential issues and mitigation strategies
4. **Step-by-Step Execution Plan** - Detailed implementation steps with checkpoints
5. **Rollback Strategy** - How to undo changes at each checkpoint
6. **Validation Criteria** - Success criteria for each step
7. **Timeline and Effort** - Estimated duration and resource requirements

### Checkpoint Guidelines
- **Checkpoint Frequency:** Every 2-4 implementation steps
- **Rollback Points:** Clear instructions for reverting to previous state
- **Validation Gates:** Specific criteria that must be met before proceeding
- **Progress Tracking:** Mechanism for marking completion and resuming work

## Quality Standards

### Planning Document Must Include
- [ ] Clear step-by-step execution sequence
- [ ] Checkpoint markers every 2-4 steps
- [ ] Rollback instructions for each checkpoint
- [ ] Risk assessment with mitigation strategies
- [ ] Dependency identification and management
- [ ] Validation criteria for each major step
- [ ] Timeline estimation with effort breakdown
- [ ] Success criteria and completion definition

### Validation Requirements
- All dependencies identified and documented
- Rollback strategy tested or validated
- Steps are atomic and clearly defined
- Checkpoints enable safe resumption
- Risk mitigation strategies are actionable
- Timeline estimates are realistic
- Validation criteria are measurable

## Integration with Implementation Pass

The Planning Pass creates the roadmap that the Implementation Pass follows:

1. **Implementation Pass SCAN** validates the existence and completeness of the implementation plan
2. **Implementation Pass DRAFT** references the planned steps and checkpoints
3. **Implementation Pass SYNC** follows the step-by-step execution plan
4. **Progress Tracking** updates the implementation plan with checkpoint completion

## Configuration Options

See [Common Procedures - Planning Pass Configuration](../docs/COMMON-PROCEDURES.md#planning-pass-configuration) for complete configuration options.
