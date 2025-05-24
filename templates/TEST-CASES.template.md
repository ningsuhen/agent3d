# Test Cases

**FORMAT SPECIFICATION:** This document must organize all test cases by logical modules with clear tracking. Each test case must include:
- Unique ID: `TC-NNNN` format (e.g., TC-0001)
- Status: `[x]` completed, `[ ]` pending, `[~]` in progress, `[s]` skipped
- Test name: Clear description of what is being tested
- Execution type: Manual, Automated, or Partial
- Priority: High, Medium, or Low

**REQUIRED SECTIONS:**
1. Summary - Statistical overview of all test cases
2. Test Execution Framework - How tests are run
3. Test case modules organized by feature area
4. Each test case must follow the format: `- [status] **TC-NNNN** - Test description (Execution Type, Priority)`

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

## {{module_name}}
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
- {{status}} **{{test_id}}** - {{test_description}} ({{execution_type}}, {{priority}})
</template>

**EXAMPLE:** See the actual TEST-CASES.md file in this project: [docs/TEST-CASES.md]({{DDD_REMOTE_BASE}}/docs/TEST-CASES.md)

**VALIDATION CHECKLIST:**
- [ ] All test cases have unique TC-NNNN identifiers
- [ ] Test cases are grouped logically by module/feature
- [ ] Each test case specifies execution type and priority
- [ ] Summary statistics match the actual test case counts
- [ ] Test execution framework is clearly defined
