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

**EXAMPLE:** (Do NOT include `<example>` tags in actual documentation)
<example>
# Tasks

## High Priority
- [ ] Fix Authentication Bug - Users cannot login after password reset (blocks user access)
- [~] Database Migration - Upgrade to PostgreSQL 15 for performance improvements
- [ ] Security Audit - Complete penetration testing before production release

## Medium Priority
- [ ] Add Dark Mode - Implement dark theme for better user experience
- [ ] API Documentation - Update OpenAPI specs for new endpoints

## Low Priority
- [ ] Mobile App - Create native iOS and Android applications
- [ ] Advanced Analytics - Implement user behavior tracking dashboard

## Completed
- [x] User Registration - Implemented email verification system (completed 2024-01-15)
- [x] Payment Integration - Added Stripe payment processing (completed 2024-01-10)
</example>

**VALIDATION CHECKLIST:**
- [ ] Tasks are prioritized correctly based on impact and urgency
- [ ] Each task has a clear, actionable description
- [ ] No duplicate tasks across priority levels
- [ ] Completed tasks are moved to the Completed section
- [ ] Task descriptions are specific enough to be actionable
