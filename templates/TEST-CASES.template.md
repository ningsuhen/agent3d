# Test Cases

**FORMAT SPECIFICATION:** This document must organize all test cases by logical modules with clear tracking. Each test case must include:
- Unique ID: `TC-NNNN` format (e.g., TC-0001)
- Status: `[x]` completed, `[ ]` pending, `[~]` in progress, `[s]` skipped
- Test name: Clear description of what is being tested
- Execution type: Manual, Automated, or Partial
- Priority: High, Medium, or Low

**SUB-TEST CASES:** Complex test scenarios can have sub-test cases using indented bullets (2 spaces):
- Main test case covering a broad scenario
  - Sub-test case 1 - Specific test condition or edge case
  - Sub-test case 2 - Another specific test condition

**REQUIRED SECTIONS:**
1. Summary - Statistical overview of all test cases
2. Test Execution Framework - How tests are run
3. Test case modules organized by feature area
4. Each test case must follow the format: `- [status] **TC-NNNN** - Test description (Execution Type, Priority)`
5. Sub-test cases use 2-space indentation and follow the same format with unique TC-NNNN IDs

**🔗 CRITICAL - Documentation Structure:**
- **ALWAYS use `## Groups (Modules)` for main functional areas or test categories**
- **ALWAYS use `### Sub-Groups (Sub-modules)` for specific test scenarios within each module**

**GROUPING STRATEGY:** Use a two-level hierarchy to organize test cases by logical modules and functional areas:
- **## Groups (Modules):** Main functional areas or test categories
- **### Sub-Groups (Sub-modules):** Specific test scenarios within each module
- **By Feature Area:** Group tests that validate the same feature or functionality
- **By Component:** Group tests that target the same system component
- **By User Journey:** Group tests that validate the same user workflow or use case
- **By Test Type:** Group tests by type (unit, integration, end-to-end, performance)
- **By Priority/Risk:** Group tests by business priority or risk level

**EXAMPLES OF GOOD GROUPING:**
- **## Authentication & Security Tests** → ### Login & Authentication, ### Authorization & Permissions
- **## User Interface Tests** → ### Form Validation, ### Navigation & Layout
- **## API & Integration Tests** → ### External APIs, ### Internal Services
- **## Data Validation Tests** → ### Input Validation, ### Data Processing
- **## Performance & Load Tests** → ### Response Time, ### Scalability
- **## Error Handling & Edge Cases** → ### Error Conditions, ### Boundary Testing

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
- [ ] All test cases and sub-test cases have unique TC-NNNN identifiers
- [ ] **CRITICAL**: Uses `## Groups (Modules)` and `### Sub-Groups (Sub-modules)` heading structure
- [ ] Test cases are grouped logically by module/feature with clear section headers
- [ ] Sub-modules within each main module group related test scenarios
- [ ] Sub-test cases use 2-space indentation and are logically related to parent test cases
- [ ] Each test case and sub-test case specifies execution type and priority
- [ ] Summary statistics match the actual test case counts (including sub-test cases)
- [ ] Test execution framework is clearly defined
- [ ] Complex test scenarios are appropriately broken down into sub-test cases
- [ ] Related test cases are grouped together for easy identification
- [ ] Module and sub-module names clearly indicate the functional area being tested
- [ ] Each sub-module has 2-8 test cases for optimal readability
