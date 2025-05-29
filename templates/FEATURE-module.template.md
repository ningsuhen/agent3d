# Feature Module Template

**PURPOSE:** Template for new feature section files in `docs/features/`.

**NAMING:** File: `{{section_name}}.md`, FT IDs: `FT-{{SECTION}}-NNN`, TC IDs: `TC-{{SECTION}}-NNN`

**TEST STRATEGY:** Emphasize multiple test cases per feature. Use sub-tests ONLY for parameterized testing (same test logic, different parameters).

**CRITICAL:** Follow [Common Procedures](../docs/COMMON-PROCEDURES.md#merged-ft-tc-structure-new).

<template>
# FT-{{SECTION}} - {{Module Title}}

## FT-{{SECTION}}-001 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Test Coverage:** {{5-8}} test cases covering all aspects
- **Related Features:** [FT-{{RELATED_SECTION}}-{{NNN}}]({{related_file}}.md#ft-{{related_section}}-{{nnn}})
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-001** - {{Core Functionality Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-002** - {{Edge Case Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-003** - {{Error Handling Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-004** - {{Integration Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-005** - {{Performance Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-006** - {{Parameterized Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
        - [{{status}}] **TC-{{SECTION}}-006a** - {{Parameter Set 1}} - {{Same test logic, different input}}
        - [{{status}}] **TC-{{SECTION}}-006b** - {{Parameter Set 2}} - {{Same test logic, different input}}
        - [{{status}}] **TC-{{SECTION}}-006c** - {{Parameter Set 3}} - {{Same test logic, different input}}

## FT-{{SECTION}}-002 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Test Coverage:** {{4-6}} test cases covering key scenarios
- **Related Features:** [FT-{{SECTION}}-001]({{current_file}}.md#ft-{{section}}-001)
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-007** - {{Basic Functionality Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-008** - {{Validation Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-009** - {{Boundary Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-010** - {{Security Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-011** - {{Cross-Platform Test}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
        - [{{status}}] **TC-{{SECTION}}-011a** - {{Platform 1}} - {{Same test on different platform}}
        - [{{status}}] **TC-{{SECTION}}-011b** - {{Platform 2}} - {{Same test on different platform}}
</template>

**EXAMPLES:** `security.md` → FT-SEC-001, `performance.md` → FT-PERF-001

**REPLACEMENTS:** `{{SECTION}}` = SEC/PERF, `{{status}}` = [x]/[~]/[ ], `{{5-8}}` = actual numbers

**TEST STRATEGY GUIDELINES:**

**✅ PREFERRED - Multiple Test Cases per Feature:**
- Core functionality test
- Edge case test
- Error handling test
- Integration test
- Performance test
- Security test
- Validation test
- Boundary test

**✅ WHEN TO USE SUB-TESTS:**
- **Parameterized testing:** Same test logic with different inputs/parameters
- **Cross-platform testing:** Same test on different platforms/environments
- **Data-driven testing:** Same test with different data sets
- **Configuration testing:** Same test with different configuration values

**❌ AVOID SUB-TESTS FOR:**
- Different test logic or functionality
- Unrelated test scenarios
- Different types of validation
- Separate feature aspects

**EXAMPLE GOOD SUB-TEST USAGE:**
```
TC-SEC-001 - Password Validation Test
  - TC-SEC-001a - Valid password (8+ chars, mixed case, numbers)
  - TC-SEC-001b - Invalid password (too short)
  - TC-SEC-001c - Invalid password (no numbers)
  - TC-SEC-001d - Invalid password (no uppercase)
```

**EXAMPLE BAD SUB-TEST USAGE:**
```
TC-SEC-001 - Security Test
  - TC-SEC-001a - Password validation  ❌ (should be separate TC)
  - TC-SEC-001b - Authentication test  ❌ (should be separate TC)
  - TC-SEC-001c - Authorization test   ❌ (should be separate TC)
```

**POST-CREATION:** Replace placeholders, remove template tags, update `docs/FEATURES.md`, run drift scanner

**VALIDATION:** See [Base Template System](BASE.template.md#universal-validation-rules)
