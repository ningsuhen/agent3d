# Tasks

**FORMAT SPECIFICATION:** This document must organize all project tasks by priority levels. Each task must include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Task description: Clear, actionable description
- Context: Brief explanation of why the task matters (optional)

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

## Medium Priority
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}

## Low Priority
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}

## Completed
- [x] {{completed_task_name}} - {{completion_description}}
- [x] {{completed_task_name}} - {{completion_description}}
</template>

**EXAMPLE:** See the actual TASKS.md file in this project: [docs/TASKS.md]({{DDD_REMOTE_BASE}}/docs/TASKS.md)

**VALIDATION CHECKLIST:**
- [ ] Tasks are prioritized correctly based on impact and urgency
- [ ] Each task has a clear, actionable description
- [ ] No duplicate tasks across priority levels
- [ ] Completed tasks are moved to the Completed section
- [ ] Task descriptions are specific enough to be actionable
