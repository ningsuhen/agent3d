# Feature Module Template

**PURPOSE:** Template for new feature section files in `docs/features/`.

**NAMING:** File: `{{section_name}}.md`, FT IDs: `FT-{{SECTION}}-NNN`, TC IDs: `TC-{{SECTION}}-NNN`

**CRITICAL:** Follow [Common Procedures](../docs/COMMON-PROCEDURES.md#merged-ft-tc-structure-new).

<template>
# FT-{{SECTION}} - {{Module Title}}

## FT-{{SECTION}}-001 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Test Coverage:** {{N}} test cases, {{N}} sub-tests
- **Related Features:** [FT-{{RELATED_SECTION}}-{{NNN}}]({{related_file}}.md#ft-{{related_section}}-{{nnn}})
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-001** - {{Test Name}} ({{Automated/Manual}}, {{High/Medium/Low}}) {{✅/🚧/📋}}
        - [{{status}}] **TC-{{SECTION}}-001a** - {{Sub-test}} - {{Description}}
        - [{{status}}] **TC-{{SECTION}}-001b** - {{Sub-test}} - {{Description}}
    - [{{status}}] **TC-{{SECTION}}-002** - {{Test Name}} ({{Type}}, {{Priority}}) {{Status}}

## FT-{{SECTION}}-002 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Test Coverage:** {{N}} test cases, {{N}} sub-tests
- **Related Features:** [FT-{{SECTION}}-001]({{current_file}}.md#ft-{{section}}-001)
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-003** - {{Test Name}} ({{Type}}, {{Priority}}) {{Status}}
        - [{{status}}] **TC-{{SECTION}}-003a** - {{Sub-test}} - {{Description}}
</template>

**EXAMPLES:** `security.md` → FT-SEC-001, `performance.md` → FT-PERF-001

**REPLACEMENTS:** `{{SECTION}}` = SEC/PERF, `{{status}}` = [x]/[~]/[ ], `{{N}}` = numbers

**POST-CREATION:** Replace placeholders, remove template tags, update `docs/FEATURES.md`, run drift scanner

**VALIDATION:** See [Base Template System](BASE.template.md#universal-validation-rules)
