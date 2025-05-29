# Test Cases

**FORMAT SPECIFICATION:** Test cases with unique TC-NNNN IDs, status `[x]`/`[ ]`/`[~]`/`[s]`, execution type, and priority. Use `## Groups`/`### Sub-Groups` structure.

**REQUIRED SECTIONS:**

1. Summary - Statistical overview of all test cases
2. Test Execution Framework - How tests are run
3. Test case modules organized by feature area
4. Format: `- [status] **TC-NNNN** - Test description (Execution Type, Priority)`
5. **DESCRIPTION LENGTH:** **CRITICAL** - Keep TC descriptions as short as possible when the linked feature provides sufficient detail for LLM understanding. Add detailed descriptions only when the linked feature lacks clarity

**IMPLEMENTATION MAPPING REQUIREMENTS:**

- **1:1 Mapping:** Each TC-NNNN MUST have exactly one corresponding test implementation
- **TC ID in Code:** Test function/method name or description MUST include the TC-NNNN identifier
- **Traceability:** Test file path MUST be documented or easily discoverable from TC-NNNN
- **Bidirectional Navigation:** Use VS Code DDD Navigator for seamless documentation ↔ code navigation

**SUB-TEST CASES:** Use indented bullets (2 spaces) with unique TC-NNNN IDs.

**🔗 CRITICAL:** Follow documentation structure from [Common Procedures](../docs/COMMON-PROCEDURES.md#structure-requirements).

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>

# Test Cases

## 📊 Summary

- **Total Test Cases:** {{total_count}}
- **Completed:** {{completed_count}} ✅
- **Pending:** {{pending_count}} ⏸️
- **In Progress:** {{in_progress_count}} 🔄
- **Skipped:** {{skipped_count}} ⏭️
- **Automated:** {{automated_count}} ({{automated_percentage}}%)
- **Partial:** {{partial_count}} ({{partial_percentage}}%)
- **Manual:** {{manual_count}} ({{manual_percentage}}%)

## 🔧 Test Execution Framework

- **Manual Testing:** {{manual_testing_description}}
- **Automated Testing:** {{automated_testing_description}}
- **Integration Testing:** {{integration_testing_description}}

## {{module_name}} (e.g., Authentication & Security Tests)

### {{sub_module_name}} (e.g., Login & Authentication)

- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
  - {{status}} **{{sub_test_id}}** - {{sub_test_description}} ({{execution_type}}, {{priority}})
  - {{status}} **{{sub_test_id}}** - {{sub_test_description}} ({{execution_type}}, {{priority}})

**DESCRIPTION LENGTH EXAMPLES:**

**SHORT (when linked feature provides sufficient detail for LLM understanding):**
- [ ] **TC-AUTH-001** - User login with valid credentials (Automated, High Priority) [Links to FT-AUTH-001]

**DETAILED (when linked feature lacks clarity for LLM understanding):**
- [ ] **TC-HTTP-003** - Content Negotiation - Verify generated client request encoding changes based on ProtoEncodingType and ProtoEncodingOptions configuration (Encoding, Medium Priority)
    - Encoding types: JSON vs BINARY affects request body serialization and Content-Type headers (application/json vs application/x-protobuf)
    - Encoding options: preserve_proto_field_names and ignore_unknown_fields affect JSON serialization behavior and header propagation
    - Default behavior: Verify encoding when no options specified
    - Test scenarios: All combinations of encoding types and options with validation of headers, body format, and field name handling

### {{sub_module_name}} (e.g., Authorization & Permissions)

- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})

## {{module_name}} (e.g., User Interface Tests)

### {{sub_module_name}} (e.g., Form Validation)

- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
  - {{status}} **{{sub_test_id}}** - {{sub_test_description}} ({{execution_type}}, {{priority}})
</template>

**EXAMPLE:** See the actual TEST-CASES.md file in the local repository: `~/.agent3d/docs/TEST-CASES.md`

**VALIDATION CHECKLIST:**

- [ ] All universal validation rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist) are met
- [ ] All test cases and sub-test cases have unique TC-NNNN identifiers
- [ ] Each test case specifies execution type (Manual/Automated/Partial) and priority (High/Medium/Low)
- [ ] Summary statistics match the actual test case counts (including sub-test cases)
- [ ] Test execution framework is clearly defined
- [ ] **1:1 MAPPING:** Each TC-NNNN has exactly one corresponding test implementation
- [ ] **TC ID IN CODE:** All test implementations include TC-NNNN in function name or description
- [ ] **TRACEABILITY:** Test file paths are documented or discoverable via VS Code DDD Navigator
- [ ] **APPROPRIATE DESCRIPTION LENGTH:** TC descriptions are as short as possible when linked features provide sufficient detail for LLM understanding, or detailed when features lack clarity
