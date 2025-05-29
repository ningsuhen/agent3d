# Feature Module Template

**PURPOSE:** Template for `docs/features/` section files.

**NAMING:** `{{section_name}}.md`, FT-{{SECTION}}-NNN, TC-{{SECTION}}-NNN

**TEST STRATEGY:** 5-8 test cases per feature. Sub-tests ONLY for parameterized testing (same logic, different parameters).

**CRITICAL:** Follow [Common Procedures](../docs/COMMON-PROCEDURES.md#merged-ft-tc-structure-new).

<template>
# FT-{{SECTION}} - {{Module Title}}

## FT-{{SECTION}}-001 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Code Location:** {{module.path}}[{{ImportedObject/Class}}] | {{file_path}} | {{N/A for documentation-only}}
- **Test Coverage:** {{5-8}} test cases covering all aspects
- **Related Features:** [FT-{{RELATED_SECTION}}-{{NNN}}]({{related_file}}.md#ft-{{related_section}}-{{nnn}})
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-001** - {{Core Functionality}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-002** - {{Edge Cases}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-003** - {{Error Handling}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-004** - {{Integration}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-005** - {{Performance}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-006** - {{Parameterized}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
        - [{{status}}] **TC-{{SECTION}}-006a** - {{Param 1}} - {{Same logic, diff input}}
        - [{{status}}] **TC-{{SECTION}}-006b** - {{Param 2}} - {{Same logic, diff input}}

## FT-{{SECTION}}-002 - {{Feature Name}}
- **Description:** {{Brief feature description}}
- **Criteria:** {{Acceptance criteria}}
- **Dependencies:** {{Related features/requirements}}
- **Impact:** {{High/Medium/Low}} - {{Impact description}}
- **Code Location:** {{module.path}}[{{ImportedObject/Class}}] | {{file_path}} | {{N/A for documentation-only}}
- **Test Coverage:** {{4-6}} test cases covering key scenarios
- **Related Features:** [FT-{{SECTION}}-001]({{current_file}}.md#ft-{{section}}-001)
- **Test Cases:**
    - [{{status}}] **TC-{{SECTION}}-007** - {{Basic Functionality}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-008** - {{Validation}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-009** - {{Boundary}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-010** - {{Security}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
    - [{{status}}] **TC-{{SECTION}}-011** - {{Cross-Platform}} ({{Auto/Manual}}, {{H/M/L}}) {{✅/🚧/📋}}
        - [{{status}}] **TC-{{SECTION}}-011a** - {{Platform 1}} - {{Same test, diff platform}}
        - [{{status}}] **TC-{{SECTION}}-011b** - {{Platform 2}} - {{Same test, diff platform}}
</template>

**EXAMPLES:** `security.md` → FT-SEC-001, `performance.md` → FT-PERF-001

**REPLACEMENTS:** `{{SECTION}}` = SEC/PERF, `{{status}}` = [x]/[~]/[ ], `{{5-8}}` = numbers

**CODE LOCATION EXAMPLES:**
- **Python:** `tools.drift_scanner[DriftScanner]` | `tools.migration_manager[MigrationManager.execute_migration]`
- **TypeScript:** `vscode-ddd-navigator/src/extension[activate]` | `src/providers/definitionProvider[DddDefinitionProvider]`
- **Shell:** `tools/drift_scanner_mcp_server.sh` | `vscode-ddd-navigator/install.sh`
- **Documentation:** `N/A` (for documentation-only features)
- **Multiple:** `tools.drift_scanner[DriftScanner], workflows.validate-sync[WorkflowSyncValidator]`

**TEST TYPES:** Core, Edge Cases, Error Handling, Integration, Performance, Security, Validation, Boundary

**SUB-TESTS:** ✅ Parameterized/Cross-platform/Data-driven (same logic, diff params) ❌ Different logic/scenarios

**GOOD:** TC-001 Password Validation → TC-001a Valid, TC-001b Too short, TC-001c No numbers
**BAD:** TC-001 Security → TC-001a Password ❌, TC-001b Auth ❌, TC-001c Authorization ❌

**POST-CREATION:** Replace placeholders, remove template tags, update `docs/FEATURES.md`, run drift scanner

**VALIDATION:** See [Base Template System](BASE.template.md#universal-validation-rules)
