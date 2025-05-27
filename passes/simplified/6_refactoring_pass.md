# Refactoring Pass

**Purpose:** Cleaning up and improving code structure without changing functionality, focusing on maintainability, readability, and performance. For documentation projects, includes LLM-focused compression to remove verbose explanations of tasks that LLMs inherently understand.

**Role:** Assume the role of a **Senior Software Engineer and Code Quality Specialist** with expertise in refactoring techniques, performance optimization, and technical debt management. Focus on improving code quality while preserving functionality. Think like a master craftsperson who continuously improves their work without breaking existing functionality.

## When to Use
- After features are fully implemented and tested
- When technical debt has accumulated
- Before adding new features to existing code
- When performance improvements are needed
- During regular maintenance cycles
- When preparing for a major release

## Process
**STANDARD WORKFLOW:** Follow [Common Procedures - Standard DDD Workflow](../docs/COMMON-PROCEDURES.md#standard-ddd-workflow)

**REFACTORING-SPECIFIC FOCUS:**
1. **Scan:** Repository-wide DRY audit, modularization opportunities, LLM compression targets
2. **Draft:** Consolidation plan, DRY implementation strategy, compression approach
3. **Ask:** Structural changes approval, priority alignment, breaking change discussion
4. **Sync:** Incremental implementation, duplication elimination, testing verification

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Repository Optimization:** Streamlined repository structure with improved organization
- **Documentation Clarity:** Consolidated and modularized documentation with eliminated redundancy
- **LLM-Optimized Content:** Compressed documentation focused on essential information for LLM consumption
- **DRY Compliance:** Zero duplication across code, documentation, and configuration
- **Improved Maintainability:** Enhanced code quality and reduced technical debt
- **Modular Architecture:** Better organized components with clear separation of concerns
- **Performance Improvements:** Optimized code and documentation for better performance
- **Preserved Functionality:** All existing functionality maintained with passing tests
- **Enhanced Clarity:** Improved readability and understanding across all repository content
- **Consistent Structure:** Unified patterns and conventions throughout the codebase

## Example Commit Message
`DDD: Refactoring Pass - Improved authentication service performance and reduced code complexity`

## Refactoring Focus Areas

### Repository-Wide Optimization
- **File Consolidation:** Combine related files for clarity and brevity
- **Directory Structure:** Optimize folder organization for logical grouping
- **Cross-Repository Consistency:** Ensure uniform patterns across all components

### DRY Principle Implementation
- **Code Duplication Elimination:** Remove all duplicated code patterns
- **Documentation Deduplication:** Merge redundant documentation sections
- **Configuration Consolidation:** Combine similar configuration patterns
- **Template Optimization:** Eliminate overlapping template functionality

### Modularization and Organization
- **Component Separation:** Split large components into focused modules
- **Logical Grouping:** Organize related functionality together
- **Interface Simplification:** Reduce complexity in public interfaces
- **Dependency Management:** Optimize component dependencies

### Code Quality Enhancement
- **Complexity Reduction:** Simplify overly complex code structures
- **Performance Optimization:** Improve execution speed and resource usage
- **Naming Improvements:** Enhance variable, function, and class names
- **Error Handling Consistency:** Standardize error handling patterns

### Documentation and Testing
- **Documentation Clarity:** Improve readability and eliminate redundancy
- **LLM-Focused Compression:** Remove verbose explanations of basic tasks that LLMs inherently understand
- **Test Consolidation:** Combine overlapping test cases
- **Language-Specific Compliance:** Follow language-specific guidelines consistently
- **Cross-Reference Optimization:** Ensure all links and references are efficient

### LLM-Focused Documentation Compression
- **Language-Specific Rules:** Apply compression rules from `~/.agent3d/rules/markdown.md`
- **Review Guidelines:** Follow `~/.agent3d/rules/markdown-review-guidelines.md` for optimization criteria
- **Basic Task Compression:** Remove detailed explanations of standard development tasks
- **Command Simplification:** Replace verbose command explanations with concise references
- **Essential Information Only:** Keep only commands, parameters, and project-specific details

## Guidelines
**UNIVERSAL STANDARDS:** Follow [Common Procedures - Quality Standards](../docs/COMMON-PROCEDURES.md#quality-standards)

**REFACTORING PRINCIPLES:**
- **DRY Enforcement:** Eliminate all duplication (code, documentation, configuration)
- **Incremental Changes:** Small, testable changes with frequent verification
- **Functionality Preservation:** All existing functionality must remain intact
- **Performance Mindset:** Consider performance implications of all changes

## LLM Documentation Compression Guidelines

### Language-Specific Compression Rules
**REFERENCE:** See [Language-Specific Rules](../../AGENT-GUIDELINES.md#language-specific-rules) for compression guidelines

**COMPRESSION PRINCIPLES:**
- **Assume LLM Competency:** Remove explanations of standard development tools
- **Command-Centric:** Provide commands/parameters, not installation instructions
- **Project-Specific Focus:** Keep project details, remove generic explanations
