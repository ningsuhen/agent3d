# FT-CORE - Core Documentation Framework

## FT-CORE-001 - Agent Guideline Protocol
- **Description:** Guidelines for agents to retrieve and follow DDD principles automatically
- **Criteria:** Agents can fetch, cache, and follow remote guidelines automatically
- **Code Location:** tools/drift_scanner.py#DriftScanner.analyze_code_locations
- **Dependencies:** Git repository access, .agent3d-config.yaml file
- **Impact:** High - Core framework functionality
- **Test Coverage:** 4 test cases, 12 sub-tests
- **Related Features:** [FT-PASS-001](passes.md#ft-pass-001) (Foundation Pass), [FT-TMPL-002](templates.md#ft-tmpl-002) (Template Access)
- **Test Cases:**
    - [ ] **TC-CORE-001** - Remote Guidelines Retrieval (Automated, High) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-001a** - SSH Repository Access - Test git clone via SSH
        - [ ] **TC-CORE-001b** - HTTPS Repository Access - Test git clone via HTTPS
        - [ ] **TC-CORE-001c** - Repository Caching - Test local cache management
        - [ ] **TC-CORE-001d** - Update Detection - Test git pull for updates
    - [ ] **TC-CORE-002** - Configuration Loading (Automated, High) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-002a** - YAML Parsing - Test .agent3d-config.yaml parsing
        - [ ] **TC-CORE-002b** - Default Values - Test fallback configuration
        - [ ] **TC-CORE-002c** - Validation - Test configuration validation
    - [ ] **TC-CORE-003** - Guideline Following (Manual, Medium) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-003a** - Pass Execution - Test DDD pass execution
        - [ ] **TC-CORE-003b** - Template Usage - Test template application
        - [ ] **TC-CORE-003c** - Rule Compliance - Test language rule following
    - [ ] **TC-CORE-004** - Error Handling (Automated, Medium) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-004a** - Network Failures - Test offline scenarios
        - [ ] **TC-CORE-004b** - Invalid Repositories - Test error handling

---

## FT-CORE-002 - DDD Pass System
- **Description:** Structured approach to documentation-driven development with 12 numbered passes
- **Criteria:** All 12 numbered passes plus Full Pass are documented and executable
- **Dependencies:** Pass templates, execution framework
- **Impact:** High - Core methodology
- **Code Location:** passes.yml/ | passes.yml/full_pass.yml
- **Test Coverage:** 3 test cases, 8 sub-tests
- **Related Features:** [FT-PASS-001](passes.md#ft-pass-001) (Foundation Pass), [FT-IMPL-009](implementation.md#ft-impl-009) (Full Pass)
- **Test Cases:**
    - [ ] **TC-CORE-005** - Pass Documentation (Manual, High) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-005a** - Pass Templates - Verify all passes have templates
        - [ ] **TC-CORE-005b** - Pass Sequence - Test correct pass ordering
        - [ ] **TC-CORE-005c** - Pass Dependencies - Test prerequisite handling
    - [ ] **TC-CORE-006** - Pass Execution (Automated, High) 📋 **DOCUMENTED**
        - [ ] **TC-CORE-006a** - Individual Pass Execution - Test single pass runs
        - [ ] **TC-CORE-006b** - Full Pass Execution - Test complete workflow
        - [ ] **TC-CORE-006c** - Pass Coordination - Test multi-pass workflows
    - [ ] **TC-CORE-007** - Pass Integration (Manual, Medium) � **DOCUMENTED**
        - [ ] **TC-CORE-007a** - Pass Dependencies - Test prerequisite handling
        - [ ] **TC-CORE-007b** - Pass Coordination - Test multi-pass workflows

---

## FT-CORE-003 - Documentation Standards
- **Description:** Guidelines for documentation completeness and accuracy across all project types
- **Criteria:** All required documentation files have templates and validation criteria
- **Dependencies:** Template system, validation rules
- **Impact:** Medium - Quality assurance
- **Code Location:** N/A (Documentation standards and guidelines)
- **Test Coverage:** 2 test cases, 5 sub-tests
- **Related Features:** [FT-TMPL-003](templates.md#ft-tmpl-003) (Validation Framework)
- **Test Cases:**
    - [x] **TC-CORE-008** - Documentation Validation (Automated, Medium) ✅ **PRODUCTION**
        - [x] **TC-CORE-008a** - Template Compliance - Test template usage
        - [x] **TC-CORE-008b** - Content Quality - Test documentation quality metrics
        - [x] **TC-CORE-008c** - Consistency Checks - Test cross-document consistency
    - [x] **TC-CORE-009** - Standards Enforcement (Manual, Low) ✅ **PRODUCTION**
        - [x] **TC-CORE-009a** - Review Process - Test documentation review workflow
        - [x] **TC-CORE-009b** - Quality Gates - Test quality checkpoint enforcement
