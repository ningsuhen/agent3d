# Development Pass

**Purpose:** Plan and implement features through step-by-step execution with checkpoints, combining planning and implementation in a unified workflow that documents all steps beforehand and executes them in a loop until completion.

**Role:** **Development Lead** combining Technical Project Manager and Senior Software Developer expertise. Focus on feature discovery, detailed planning, clean implementation, and checkpoint-based execution with rollback capabilities.

## When to Use

### Required for Major Changes
- **Migrations:** Database schema changes, platform migrations, framework upgrades
- **Refactoring:** Large-scale code restructuring, architecture changes
- **Complex Features:** Multi-component features, integration with external systems
- **Infrastructure Changes:** Deployment pipeline modifications, environment setup
- **Breaking Changes:** API modifications, backward-incompatible updates

### Suitable for All Development Work
- Feature implementation from documentation
- Bug fixes with clear scope
- Documentation-driven development
- Converting proof of concept to production code
- Any change requiring step-by-step execution

### Automatic Triggers
Development Pass is automatically triggered when Documentation Pass identifies:
- Changes affecting >3 components/files
- Dependencies on external systems
- Risk level marked as "Medium" or "High"
- Timeline >1 day estimated effort
- Rollback complexity marked as "Complex"

## Process

1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), scan all relevant docs from docs/, identify features/drift that need development work
2. **Draft:** Feature selection (AUTO MODE picks features/drift based on priority, PICKER MODE allows human choice), create complete EXEC-PLAN-{change-name}.md with all steps documented
3. **Ask:** Validate feature selection and execution plan, confirm approach and priorities
4. **Sync:** Execute documented steps in loop until all features complete, update progress in execution plan, respect checkpoints and rollback strategies

**Note:** During execution, mark completed steps with ✅ to track progress.

## Feature Discovery and Selection

### Document Analysis
The Development Pass scans all relevant docs from docs/ including:
- **docs/FEATURES.md** - Identify incomplete features
- **docs/TASKS.md** - Find high-priority development tasks
- **docs/DDD-STATUS.md** - Detect drift and alignment issues
- **docs/REQUIREMENTS.md** - Check unimplemented requirements
- **docs/ACCEPTANCE-CRITERIA.md** - Find unmet criteria
- **docs/designs/*.md** - Review design specifications
- **docs/proposals/*.md** - Check proposed features

### Selection Modes

#### AUTO MODE (Default)
- Automatically picks features/drift from docs based on priority
- Respects dependencies and effort limits
- Includes drift fixes and blocking issues
- Continues with execution plan creation

#### PICKER MODE (Interactive)
- Presents discovered features to human for selection
- Shows priorities, dependencies, and effort estimates
- Allows custom feature combinations
- Human chooses which features to include

## Expected Outcomes

- **Execution Plan Document** (`docs/runs/EXEC-PLAN-{change-name}.md`)
- **Working Implementation** with basic test coverage
- **Checkpoint Strategy** with clear rollback points
- **Risk Assessment** with mitigation strategies
- **Progress Tracking** with real-time status updates
- **Standards Compliance** following language-specific rules
- **Updated Documentation** reflecting implemented changes

## Related Passes

Requirements → Foundation → Documentation → **Development** → Testing

## Example Commit Message

`DDD: Development Pass - Implemented user authentication and security features`

## Execution Plan Structure

### Required Sections
1. **Change Overview** - High-level description and scope
2. **Feature Discovery Results** - Analyzed documents and selected features
3. **Step-by-Step Execution Plan** - Detailed implementation steps with LLM instructions
4. **Checkpoint Strategy** - Verification points every 2-4 steps
5. **Risk Assessment** - Potential issues and mitigation strategies
6. **Dependencies** - Internal, external, and prerequisite requirements
7. **Quality Gates** - Success criteria and completion validation

### Step Documentation Format
Each step includes:
- **Status**: [ ] Not Started | [~] In Progress | [x] Complete
- **Feature**: Which feature this step implements
- **Description**: What the step accomplishes
- **LLM Instructions**: Specific implementation guidance
- **Verification Criteria**: How to validate step completion
- **Estimated Time**: Expected duration

### Checkpoint Guidelines
- **Checkpoint Frequency:** Every 2-4 implementation steps
- **Rollback Points:** Clear instructions for reverting to previous state
- **Validation Gates:** Specific criteria that must be met before proceeding
- **Progress Tracking:** Real-time updates in execution plan file

## Loop Execution Model

```
1. Create execution plan with all steps documented
2. While (incomplete steps exist in execution plan):
   a. Read next incomplete step from plan
   b. Execute step instructions (implement, test, verify)
   c. Update execution plan with completion status
   d. If checkpoint reached, verify checkpoint criteria
   e. Continue to next step
3. Archive completed execution plan
4. Update project documentation
```

## Quality Standards

### Execution Plan Must Include
- [ ] Clear step-by-step execution sequence
- [ ] Checkpoint markers every 2-4 steps
- [ ] Rollback instructions for each checkpoint
- [ ] Risk assessment with mitigation strategies
- [ ] Dependency identification and management
- [ ] Validation criteria for each major step
- [ ] LLM instructions for each step
- [ ] Success criteria and completion definition

### Implementation Standards
- Follow language-specific rules and best practices
- Implement documented requirements only
- Keep code lean and maintainable
- Document technical decisions
- Ensure readability and standards compliance
- Write basic tests for core functionality
- Provide foundation for comprehensive testing

### Validation Requirements
- All dependencies identified and documented
- Rollback strategy tested or validated
- Steps are atomic and clearly defined
- Checkpoints enable safe resumption
- Risk mitigation strategies are actionable
- Timeline estimates are realistic
- Validation criteria are measurable

## Testing Focus

- Happy path test cases
- Basic validation tests
- Core functionality coverage
- Foundation for comprehensive testing
- Integration with existing test suite
- Checkpoint verification tests

## Configuration Options

Development Pass can be configured in `.agent3d-config.yml`:

```yaml
development_pass:
  enabled: true
  selection_mode: "auto"  # "auto" | "picker"
  runs_directory: "docs/runs/"
  always_create_execution_plan: true

  # Auto Selection Criteria
  auto_selection:
    priority_threshold: "high"
    max_features_per_run: 3
    include_drift_fixes: true
    include_blockers: true
    respect_dependencies: true
    max_estimated_effort: "3 days"

  # Execution Settings
  checkpoint_frequency: 3  # steps between checkpoints
  auto_test_after_step: true
  archive_completed_plans: true

  # Auto-trigger thresholds (inherited from Planning Pass)
  auto_trigger_thresholds:
    file_count: 3
    estimated_effort_hours: 8
    risk_level: "medium"
    complexity: "high"

  required_for:
    - migrations
    - refactoring
    - breaking_changes
  optional_for:
    - bug_fixes
    - documentation
```

## Checkpoint Management

### Before Each Checkpoint
- Validate all step criteria are met
- Run tests to ensure functionality works
- Verify no regressions introduced
- Update execution plan with current status

### At Checkpoint Failure
- Follow rollback instructions to previous checkpoint
- Document issues and blockers in execution plan
- Assess whether to continue or abort execution
- Update risk assessment if needed

### Progress Updates
- Mark steps as completed [x] in execution plan
- Update overall progress percentage
- Track time estimates vs. actual time
- Document any deviations from plan

## Integration with Other Passes

### Preparation for Testing Pass
- Provides working implementation with basic tests
- Documents test scenarios and validation criteria
- Establishes foundation for comprehensive testing
- Updates TEST-CASES.md with implemented features

### Documentation Updates
- Updates FEATURES.md with completed features
- Updates TASKS.md with completed work items
- Updates DDD-STATUS.md with progress
- Creates or updates design documentation as needed
