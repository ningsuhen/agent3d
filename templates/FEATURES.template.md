# Features

**FORMAT SPECIFICATION:** This document must list all project features organized by logical modules. Each feature must be on a SINGLE LINE and include:
- Checkbox status: `[x]` for completed, `[ ]` for pending, `[~]` for in progress
- Feature name: Clear, concise description
- Brief explanation: One-line description of what the feature does
- Acceptance criteria: Specific, measurable criteria in format (Criteria: <criteria description>)

**CRITICAL:** Features must NEVER span multiple lines. All information must fit on one line.

**REQUIRED SECTIONS:**
1. Important Note (if project has special characteristics)
2. Core Features (main functionality modules)
3. Additional feature categories as needed for your project
4. Each section must have 3-10 features listed

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>
# Features

## Important Note
{{project_special_note}}

## Core {{module_name}}
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})

## {{additional_module_name}}
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
</template>

**EXAMPLE:** (Do NOT include `<example>` tags in actual documentation)
<example>
# Features

## Important Note
**Agent3D is a documentation-only framework.** It does not contain any implementations, libraries, or code to import.

## Core Authentication
- [x] User Registration - Allow new users to create accounts with email verification (Criteria: Users can register with email/password and receive verification email within 30 seconds)
- [ ] Password Reset - Enable users to reset forgotten passwords securely (Criteria: Users receive reset link via email and can set new password within 24 hours)
- [~] Multi-Factor Authentication - Add SMS and authenticator app support (Criteria: Users can enable 2FA with 99.9% success rate for authentication)

## Payment Processing
- [ ] Credit Card Integration - Process payments through Stripe API (Criteria: Handle payments with 99.9% uptime and full PCI compliance)
- [ ] Subscription Management - Manage recurring billing cycles (Criteria: Automatically charge subscriptions with 95% success rate and handle failed payments)
</example>

**VALIDATION CHECKLIST:**
- [ ] All features are on a SINGLE LINE (no multi-line entries)
- [ ] All features follow the exact format: - {{status}} {{feature_name}} - {{brief_description}} (Criteria: {{acceptance_criteria}})
- [ ] Each feature includes acceptance criteria in (Criteria: <>) format
- [ ] Acceptance criteria are specific and measurable
- [ ] Features are grouped logically by module/category
- [ ] Status indicators are accurate and up-to-date
- [ ] No duplicate features across sections
