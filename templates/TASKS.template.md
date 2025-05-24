# Tasks

**FORMAT SPECIFICATION:** Tasks organized by priority (High/Medium/Low/Completed) with status `[x]`/`[ ]`/`[~]` and actionable descriptions. Use `## Groups`/`### Sub-Groups` structure.

**SUB-TASKS:** Complex tasks can have sub-tasks using indented bullets (2 spaces).

**PRIORITY GUIDELINES:**
- **High Priority:** Tasks that block other work, critical bugs, security issues
- **Medium Priority:** Feature improvements, performance optimizations, documentation updates
- **Low Priority:** Nice-to-have features, experimental ideas, long-term goals

**🔗 CRITICAL:** Use `## Groups (Priority Levels)` for High/Medium/Low/Completed and `### Sub-Groups (Functional Areas)` for specific work areas within each priority.

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Tasks

## High Priority

### {{functional_area}} (e.g., Documentation & Guidelines)
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}

### {{functional_area}} (e.g., Infrastructure & Tooling)
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}

## Medium Priority

### {{functional_area}} (e.g., Feature Development)
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}
  - {{status}} {{sub_task_name}} - {{sub_task_description}}

### {{functional_area}} (e.g., Quality & Testing)
- {{status}} {{task_name}} - {{task_description}}

## Low Priority

### {{functional_area}} (e.g., Future Enhancements)
- {{status}} {{task_name}} - {{task_description}}
- {{status}} {{task_name}} - {{task_description}}

## Completed

### {{functional_area}} (e.g., Documentation & Guidelines)
- [x] {{completed_task_name}} - {{completion_description}}
- [x] {{completed_task_name}} - {{completion_description}}
  - [x] {{completed_sub_task}} - {{sub_completion_description}}

### {{functional_area}} (e.g., Infrastructure & Tooling)
- [x] {{completed_task_name}} - {{completion_description}}
</template>

**EXAMPLE:** See the actual TASKS.md file in the local repository: `~/.agent3d/docs/TASKS.md`

**VALIDATION CHECKLIST:**
- [ ] Tasks are prioritized correctly based on impact and urgency
- [ ] Each task has a clear, actionable description
- [ ] Sub-tasks use 2-space indentation and are logically related to parent tasks
- [ ] **CRITICAL**: Uses `## Groups (Priority Levels)` and `### Sub-Groups (Functional Areas)` heading structure
- [ ] Tasks are grouped by functional area within each priority level
- [ ] Completed tasks are moved to the Completed section with appropriate grouping
- [ ] Task descriptions are specific enough to be actionable
