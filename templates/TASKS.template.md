# Tasks

**FORMAT SPECIFICATION:** This document must organize all project tasks by priority levels. Each task must include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Task description: Clear, actionable description
- Context: Brief explanation of why the task matters (optional)

**SUB-TASKS:** Complex tasks can have sub-tasks using indented bullets (2 spaces):
- Main task with multiple components can be broken down
  - Sub-task 1 - Specific component or step
  - Sub-task 2 - Another component or step

**REQUIRED SECTIONS:**
1. High Priority - Critical tasks that block other work
2. Medium Priority - Important tasks that improve the project
3. Low Priority - Nice-to-have tasks for future consideration
4. Completed - Archive of finished tasks for reference

**PRIORITY GUIDELINES:**
- **High Priority:** Tasks that block other work, critical bugs, security issues
- **Medium Priority:** Feature improvements, performance optimizations, documentation updates
- **Low Priority:** Nice-to-have features, experimental ideas, long-term goals

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Tasks

## High Priority
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}

## Medium Priority
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}

## Low Priority
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}

## Completed
- [x] {{completed_task_name}} - {{completion_description}}
- [x] {{completed_task_name}} - {{completion_description}}
  - [x] {{completed_sub_task}} - {{sub_completion_description}}
</template>

**EXAMPLE:** See the actual TASKS.md file in this project: [docs/TASKS.md]({{DDD_REMOTE_BASE}}/docs/TASKS.md)

**VALIDATION CHECKLIST:**
- [ ] Tasks are prioritized correctly based on impact and urgency
- [ ] Each task and sub-task has a clear, actionable description
- [ ] Sub-tasks use 2-space indentation and are logically related to parent tasks
- [ ] No duplicate tasks across priority levels
- [ ] Completed tasks are moved to the Completed section
- [ ] Task descriptions are specific enough to be actionable
- [ ] Complex tasks are appropriately broken down into sub-tasks
