# Refactoring Pass

**Purpose:** Cleaning up and improving code structure without changing functionality, focusing on maintainability, readability, and performance.

**Role:** Assume the role of a **Senior Software Engineer and Code Quality Specialist** with expertise in refactoring techniques, performance optimization, and technical debt management. Focus on improving code quality while preserving functionality. Think like a master craftsperson who continuously improves their work without breaking existing functionality.

## When to Use
- After features are fully implemented and tested
- When technical debt has accumulated
- Before adding new features to existing code
- When performance improvements are needed
- During regular maintenance cycles
- When preparing for a major release

## Process
1. **Scan:**
   - **Repository-Wide Review:** Examine entire repository structure for optimization opportunities
   - **Documentation Analysis:** Review all documentation for redundancy, overlap, and clarity issues
   - **Code Quality Assessment:** Identify code smells, technical debt, and maintainability issues
   - **DRY Principle Audit:** Find duplicated code, documentation, and configuration patterns
   - **Modularization Opportunities:** Identify components that can be combined or split for better organization
   - **Performance Bottlenecks:** Analyze code and documentation for performance issues
   - **Architectural Alignment:** Review overall structure and design consistency

2. **Draft:**
   - **Consolidation Plan:** Document which files/modules can be combined for clarity and brevity
   - **Modularization Strategy:** Plan how to restructure components for better organization
   - **DRY Implementation:** Design approach to eliminate duplication across code and documentation
   - **Refactoring Priorities:** Rank improvements by impact and risk
   - **Verification Approach:** Plan how to ensure functionality is preserved during changes
   - **Documentation Streamlining:** Identify redundant documentation sections to merge or remove

3. **Ask:**
   - **Consolidation Approval:** Confirm which files/modules should be combined
   - **Structural Changes:** Verify proposed modularization and reorganization
   - **DRY Implementation:** Validate approach to eliminate duplication
   - **Priority Alignment:** Ensure refactoring priorities match project goals
   - **Breaking Changes:** Discuss any changes that might affect existing workflows

4. **Sync:**
   - **Incremental Implementation:** Apply refactoring changes in small, testable increments
   - **DRY Enforcement:** Eliminate identified duplication across code and documentation
   - **Modular Restructuring:** Implement planned consolidation and modularization
   - **Testing Verification:** Run all tests to ensure functionality is preserved
   - **Documentation Updates:** Update all affected documentation to reflect changes
   - **Cross-Reference Validation:** Ensure all links and references remain functional

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Repository Optimization:** Streamlined repository structure with improved organization
- **Documentation Clarity:** Consolidated and modularized documentation with eliminated redundancy
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
- **Test Consolidation:** Combine overlapping test cases
- **Language-Specific Compliance:** Follow language-specific guidelines consistently
- **Cross-Reference Optimization:** Ensure all links and references are efficient

## Verification Approach
- Run all existing tests to ensure functionality is preserved
- Verify performance metrics before and after changes
- Review changes with team members
- Ensure documentation remains accurate
- Validate that all requirements are still met

## Guidelines

### Repository Review Principles
- **Comprehensive Audit:** Review every file in the repository for optimization opportunities
- **DRY Enforcement:** Eliminate all forms of duplication (code, documentation, configuration)
- **Modular Thinking:** Always consider if components can be combined or split for better clarity
- **Brevity Focus:** Prioritize concise, clear communication over verbose explanations

### Implementation Approach
- **Incremental Changes:** Make small, testable changes with frequent verification
- **One Area at a Time:** Focus on specific components to avoid overwhelming changes
- **Backward Compatibility:** Maintain existing functionality and interfaces
- **No Feature Addition:** Strictly refactor without adding new functionality
- **Reversible Changes:** Keep changes easily reversible when possible

### Quality Standards
- **Documentation Consistency:** Ensure uniform style and structure across all documentation
- **Code Standards:** Follow language-specific rules and best practices consistently
- **Architectural Alignment:** Maintain consistency with overall system design
- **Performance Mindset:** Always consider performance implications of changes
- **Testing Preservation:** Ensure all existing tests continue to pass

### Validation Requirements
- **Functionality Verification:** All existing functionality must remain intact
- **Performance Measurement:** Track performance metrics before and after changes
- **Documentation Accuracy:** Ensure all documentation reflects actual implementation
- **Cross-Reference Integrity:** Validate that all links and references remain functional
