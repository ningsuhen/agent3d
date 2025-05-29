# Agent3D Guidelines

This directory contains YAML-formatted guidelines for the Agent3D Documentation-Driven Development framework.

## 📁 Directory Structure

```
guidelines/
├── README.md                    # This file
└── test-case-guidelines.yml     # Comprehensive test case selection and implementation guidelines
```

## 🎯 Purpose

The guidelines directory provides:

1. **Structured Guidelines**: YAML-formatted guidelines optimized for LLM processing
2. **Comprehensive Coverage**: Unified guidelines replacing multiple markdown documents
3. **Machine Readability**: Structured data for automated validation and processing
4. **Consistent Standards**: Standardized approach across all Agent3D projects

## 📋 Available Guidelines

### `test-case-guidelines.yml`
- **Purpose**: Comprehensive test case selection and implementation guidelines
- **Replaces**: `docs/TEST-CASE-SELECTION-GUIDELINES.md`, `docs/TC-SUBTEST-GUIDELINES.md`
- **Version**: 2.0.0
- **Features**:
  - Quality over quantity philosophy
  - Feature complexity-based selection criteria
  - Sub-test usage guidelines
  - Decision frameworks and trees
  - Implementation examples
  - Quality indicators
  - Agent instructions

## 🎯 Key Principles

### Quality Over Quantity
- Select test cases based on feature needs and risk
- Avoid arbitrary numerical goals
- Focus on critical paths and failure modes
- Maintain efficient, maintainable test coverage

### Judicious Sub-Test Usage
- Use sub-tests only for parameterized testing
- Same logic with different input values
- Avoid sub-tests for different functionality
- Prefer separate test cases for different logic

## 📊 Feature Complexity Guidelines

### Simple Features (1-2 Test Cases)
- Basic CRUD operations
- Simple validations
- Configuration loading

### Moderate Features (2-4 Test Cases)
- API endpoints
- Data processing
- User authentication

### Complex Features (3-6 Test Cases)
- Multi-step workflows
- Integration systems
- Advanced algorithms

## 🔍 Decision Framework

### Test Case Decision Tree
1. Is this core functionality? → Yes: Create test case
2. Does failure impact users significantly? → Yes: Create test case
3. Is this complex or error-prone logic? → Yes: Create test case
4. Is this already covered by other tests? → Yes: Skip test case
5. Is this trivial or framework code? → Yes: Skip test case

### Sub-Test Decision Tree
1. Same test logic with different inputs? → Yes: Use sub-tests
2. Testing boundary conditions? → Yes: Use sub-tests
3. Different logic or setup required? → No: Use separate test cases
4. Unrelated functionality? → No: Use separate test cases

## 🎯 Integration with DDD Framework

### Template Integration
- `templates/FEATURE-module.template.yml` references these guidelines
- Test strategy field includes judicious selection guidance

### Procedure Integration
- `procedures.yml/ft-tc-structure.yml` references these guidelines
- `procedures.yml/language-rules.yml` includes testing requirements

### Configuration Integration
- `AGENT-GUIDELINES.yml` includes test_case_requirements section
- `.agent3d-config.yml` includes guidelines_directory structure

## 📖 Usage

### For LLM Agents
1. Load guidelines at session start
2. Apply selection criteria systematically
3. Use decision frameworks for test case evaluation
4. Follow implementation examples for consistency

### For Human Developers
1. Reference guidelines for test planning
2. Use quality indicators to assess coverage
3. Apply decision trees for systematic evaluation
4. Follow examples for implementation patterns

## 🔄 Future Guidelines

Additional YAML guidelines may be added to this directory for:
- Code review standards
- Documentation quality criteria
- Architecture decision frameworks
- Quality gate definitions

---

**Note**: These guidelines are optimized for both machine processing and human understanding, providing structured data for automated workflows while maintaining clarity for human developers.
