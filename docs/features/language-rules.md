# FT-LANG - Language-Specific Rules

## FT-LANG-001 - Python Rules
- **Description:** Development guidelines for Python projects covering environment, style, and testing
- **Criteria:** Complete rules covering environment, style, and testing for Python
- **Dependencies:** Python development environment, linting tools
- **Impact:** High - Python project quality
- **Code Location:** rules.yml/python.yml
- **Test Coverage:** 3 test cases, 9 sub-tests
- **Related Features:** [FT-IMPL-003](implementation.md#ft-impl-003) (Refactoring Pass), [FT-STAT-004](status-tracking.md#ft-stat-004) (Drift Detection)
- **Test Cases:**
    - [x] **TC-LANG-001** - Environment Setup (Manual, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-001a** - Virtual Environment - Test Python venv configuration
        - [x] **TC-LANG-001b** - Dependency Management - Test requirements.txt and pip usage
        - [x] **TC-LANG-001c** - Version Compatibility - Test Python version requirements
    - [x] **TC-LANG-002** - Code Style (Automated, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-002a** - PEP 8 Compliance - Test Python style guide adherence
        - [x] **TC-LANG-002b** - Linting Integration - Test flake8/pylint usage
        - [x] **TC-LANG-002c** - Formatting Standards - Test black/autopep8 integration
    - [x] **TC-LANG-003** - Testing Framework (Automated, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-003a** - Pytest Configuration - Test pytest setup and usage
        - [x] **TC-LANG-003b** - Test Structure - Test test organization and naming
        - [x] **TC-LANG-003c** - Coverage Reporting - Test coverage.py integration

---

## FT-LANG-002 - JavaScript Rules
- **Description:** Development guidelines for JavaScript projects covering environment, style, and testing
- **Criteria:** Complete rules covering environment, style, and testing for JavaScript
- **Dependencies:** Node.js environment, JavaScript tooling
- **Impact:** High - JavaScript project quality
- **Code Location:** rules.yml/javascript.yml
- **Test Coverage:** 3 test cases, 9 sub-tests
- **Related Features:** [FT-IMPL-003](implementation.md#ft-impl-003) (Refactoring Pass), [FT-STAT-004](status-tracking.md#ft-stat-004) (Drift Detection)
- **Test Cases:**
    - [x] **TC-LANG-004** - Environment Setup (Manual, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-004a** - Node.js Configuration - Test Node.js and npm setup
        - [x] **TC-LANG-004b** - Package Management - Test package.json and dependency management
        - [x] **TC-LANG-004c** - Build Tools - Test webpack/rollup/vite configuration
    - [x] **TC-LANG-005** - Code Style (Automated, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-005a** - ESLint Configuration - Test JavaScript linting rules
        - [x] **TC-LANG-005b** - Prettier Integration - Test code formatting standards
        - [x] **TC-LANG-005c** - TypeScript Support - Test TypeScript configuration when applicable
    - [x] **TC-LANG-006** - Testing Framework (Automated, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-006a** - Jest Configuration - Test Jest testing framework setup
        - [x] **TC-LANG-006b** - Test Structure - Test test organization and naming conventions
        - [x] **TC-LANG-006c** - Coverage Reporting - Test code coverage integration

---

## FT-LANG-003 - Java Rules
- **Description:** Development guidelines for Java projects covering environment, style, and testing
- **Criteria:** Complete rules covering environment, style, and testing for Java
- **Dependencies:** Java development environment, build tools
- **Impact:** Medium - Java project quality
- **Code Location:** rules.yml/java.yml
- **Test Coverage:** 3 test cases, 9 sub-tests
- **Related Features:** [FT-IMPL-003](implementation.md#ft-impl-003) (Refactoring Pass), [FT-STAT-004](status-tracking.md#ft-stat-004) (Drift Detection)
- **Test Cases:**
    - [x] **TC-LANG-007** - Environment Setup (Manual, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-007a** - JDK Configuration - Test Java Development Kit setup
        - [x] **TC-LANG-007b** - Build Tools - Test Maven/Gradle configuration
        - [x] **TC-LANG-007c** - IDE Integration - Test IntelliJ/Eclipse setup
    - [x] **TC-LANG-008** - Code Style (Automated, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-008a** - Checkstyle Rules - Test Java style guide enforcement
        - [x] **TC-LANG-008b** - PMD Integration - Test code quality analysis
        - [x] **TC-LANG-008c** - SpotBugs Usage - Test bug detection tools
    - [x] **TC-LANG-009** - Testing Framework (Automated, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-009a** - JUnit Configuration - Test JUnit testing framework
        - [x] **TC-LANG-009b** - Mockito Integration - Test mocking framework usage
        - [x] **TC-LANG-009c** - Coverage Reporting - Test JaCoCo coverage integration

---

## FT-LANG-004 - Go Rules
- **Description:** Development guidelines for Go projects covering environment, style, and testing
- **Criteria:** Complete rules covering environment, style, and testing for Go
- **Dependencies:** Go development environment, Go tooling
- **Impact:** Medium - Go project quality
- **Code Location:** rules.yml/go.yml
- **Test Coverage:** 3 test cases, 9 sub-tests
- **Related Features:** [FT-IMPL-003](implementation.md#ft-impl-003) (Refactoring Pass), [FT-STAT-004](status-tracking.md#ft-stat-004) (Drift Detection)
- **Test Cases:**
    - [x] **TC-LANG-010** - Environment Setup (Manual, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-010a** - Go Installation - Test Go compiler and tools setup
        - [x] **TC-LANG-010b** - Module Management - Test go.mod and dependency handling
        - [x] **TC-LANG-010c** - Workspace Configuration - Test GOPATH and module workspace
    - [x] **TC-LANG-011** - Code Style (Automated, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-011a** - Go Format - Test gofmt code formatting
        - [x] **TC-LANG-011b** - Go Vet - Test go vet static analysis
        - [x] **TC-LANG-011c** - Golint Integration - Test golint style checking
    - [x] **TC-LANG-012** - Testing Framework (Automated, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-012a** - Go Test - Test built-in testing framework
        - [x] **TC-LANG-012b** - Benchmark Tests - Test performance testing capabilities
        - [x] **TC-LANG-012c** - Coverage Reporting - Test go test coverage integration

---

## FT-LANG-005 - Markdown Rules
- **Description:** Development guidelines for markdown documentation projects with comprehensive quality standards
- **Criteria:** Complete rules covering linting, validation, and quality standards for markdown
- **Dependencies:** Markdown linting tools, validation framework
- **Impact:** Medium - Documentation quality
- **Code Location:** rules.yml/markdown.yml
- **Test Coverage:** 3 test cases, 9 sub-tests
- **Related Features:** [FT-TMPL-003](templates.md#ft-tmpl-003) (Validation Framework), [FT-IMPL-006](implementation.md#ft-impl-006) (Quality Pass)
- **Test Cases:**
    - [x] **TC-LANG-013** - Markdown Linting System (Automated, High) ✅ **PRODUCTION**
        - [x] **TC-LANG-013a** - Markdownlint Configuration - Test .markdownlint.yaml config with 120-character line length
        - [x] **TC-LANG-013b** - Automated Fixing - Test automatic markdown formatting correction
        - [x] **TC-LANG-013c** - CI Integration - Test continuous linting in build pipeline
    - [x] **TC-LANG-014** - Validation Priority System (Manual, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-014a** - Primary Linting - Test markdown linting as primary validation check
        - [x] **TC-LANG-014b** - Secondary Validation - Test additional validation layers
        - [x] **TC-LANG-014c** - Manual Review - Test manual review workflow integration
    - [x] **TC-LANG-015** - Quality Standards (Manual, Medium) ✅ **PRODUCTION**
        - [x] **TC-LANG-015a** - Development Rules - Test complete markdown development rules
        - [x] **TC-LANG-015b** - LLM Optimization - Test LLM optimization guidelines
        - [x] **TC-LANG-015c** - Best Practices - Test comprehensive quality best practices
