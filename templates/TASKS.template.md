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

**🔗 CRITICAL - Documentation Structure:**
- **ALWAYS use `## Groups (Priority Levels)` for High, Medium, Low, Completed**
- **ALWAYS use `### Sub-Groups (Functional Areas)` for specific work areas within each priority**

**GROUPING STRATEGY:** Use a two-level hierarchy within each priority level to organize tasks:
- **## Groups (Priority Levels):** High, Medium, Low, Completed
- **### Sub-Groups (Functional Areas):** Specific work areas within each priority
- **By Feature Area:** Group tasks related to the same feature or functionality
- **By Component:** Group tasks that affect the same system component
- **By Skill/Team:** Group tasks that require similar expertise or team assignment
- **By Dependencies:** Group tasks that have dependencies on each other
- **By Timeline:** Group tasks that should be completed in the same timeframe

**EXAMPLES OF GOOD GROUPING:**
- **## High Priority** → ### Documentation & Guidelines, ### Infrastructure & Tooling
- **## Medium Priority** → ### Feature Development, ### Quality & Testing
- **## Low Priority** → ### Future Enhancements, ### Research & Planning
- **## Completed** → ### Documentation & Guidelines, ### Infrastructure & Tooling

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

**EXAMPLE:** See the actual TASKS.md file in this project: [docs/TASKS.md]({{DDD_REMOTE_BASE}}/docs/TASKS.md)

**VALIDATION CHECKLIST:**
- [ ] Tasks are prioritized correctly based on impact and urgency
- [ ] Each task and sub-task has a clear, actionable description
- [ ] Sub-tasks use 2-space indentation and are logically related to parent tasks
- [ ] **CRITICAL**: Uses `## Groups (Priority Levels)` and `### Sub-Groups (Functional Areas)` heading structure
- [ ] Tasks are grouped by functional area within each priority level
- [ ] Functional area headers clearly indicate the type of work
- [ ] Related tasks are grouped together for easy identification
- [ ] No duplicate tasks across priority levels or functional areas
- [ ] Completed tasks are moved to the Completed section with appropriate grouping
- [ ] Task descriptions are specific enough to be actionable
- [ ] Complex tasks are appropriately broken down into sub-tasks
- [ ] Each functional area has 2-8 tasks for optimal readability
