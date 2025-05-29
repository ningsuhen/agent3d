# Features Index

This document provides an index of all Agent3D features organized by module with FT-* identifiers for traceability.

## Important Note

**Agent3D is a documentation-only framework.** It does not contain any implementations, libraries, or code to import. The features listed below refer to the documentation guidelines and principles defined in this repository, not to functional components.

## New Merged FT-TC Structure

**As of 2025-01-27**, Agent3D has migrated to a **merged FT-TC structure** where features and their associated test cases are documented together in modular section files located in `docs/features/`. This replaces the previous separate `FEATURES.md` and `TEST-CASES.md` files.

### Structure Benefits:
- **Modular Organization:** Features organized by logical sections (core, passes, implementation, etc.)
- **Integrated Testing:** Test cases directly associated with their features
- **Better Traceability:** Clear FT-TC relationships in a single location
- **Scalability:** Easy to add new feature sections without modifying multiple files
- **Code Location Linking:** Direct links from features to implementation code for better analysis

### Migration Guide:
- **Old:** Single `docs/FEATURES.md` file with separate `docs/TEST-CASES.md`
- **New:** Multiple section files in `docs/features/` directory with merged FT-TC content
- **Compatibility:** Drift scanner supports both structures with automatic fallback

## Feature Modules

### Core Documentation Framework
- [FT-CORE](features/core.md) - Core Documentation Framework (3 features) ✅ **PRODUCTION**

### Documentation Passes
- [FT-PASS](features/passes.md) - Documentation Passes (6 features) ✅ **PRODUCTION**

### Implementation Passes
- [FT-IMPL](features/implementation.md) - Implementation Passes (9 features) ✅ **PRODUCTION**

### Language-Specific Rules
- [FT-LANG](features/language-rules.md) - Language-Specific Rules (5 features) ✅ **PRODUCTION**

### Enhanced Template System
- [FT-TMPL](features/templates.md) - Enhanced Template System (4 features) ✅ **PRODUCTION**

### Proposal System
- [FT-PROP](features/proposals.md) - Proposal System (2 features) ✅ **PRODUCTION**

### Integration Guidelines
- [FT-INTG](features/integration.md) - Integration Guidelines (5 features) ✅ **PRODUCTION**

### Status Tracking
- [FT-STAT](features/status-tracking.md) - Status Tracking (4 features) ✅ **PRODUCTION**

## Quick Reference

- **Total Features:** 38 features across 8 modules
- **Status:** All modules in production
- **Documentation:** Each module has detailed feature specifications with test cases
- **Navigation:** Click any module link above to view detailed features and test cases

## Working with the New Structure

### For Developers:
```bash
# View all features by section
ls docs/features/

# View specific feature section
cat docs/features/core.md

# Run drift analysis on new structure
python3 tools/drift_scanner.py --mode ft-mapping
```

### For Documentation:
- **Add new features:** Edit appropriate section file in `docs/features/`
- **Create new sections:** Add new `.md` file in `docs/features/` directory
- **Test case integration:** Include test cases directly under each feature
- **Validation:** Use drift scanner to verify FT-TC relationships

### Template Usage:
- **Individual features:** Use `templates/FEATURES.template.md`
- **New modules:** Use `templates/FEATURE-module.template.md`

## Code Location Field

**New Enhancement (2025-01-27):** All features now include a **Code Location** field that links features to their actual implementation code. This enhancement improves:

- **Feature-Implementation Analysis:** Automated verification of feature-code alignment
- **Test Writing:** Clear guidance on what code to import and test
- **Quality Assessment:** Better code review and maintenance capabilities
- **Drift Detection:** Enhanced accuracy in feature-implementation mapping

**Documentation:** See [CODE-LOCATION-FIELD.md](CODE-LOCATION-FIELD.md) for complete documentation and examples.

## Related Documentation

- **[Code Location Field](CODE-LOCATION-FIELD.md)** - Complete guide to the new Code Location field
- **[High-Level Design](HIGH-LEVEL-DESIGN.md)** - System architecture and component designs
- **[Requirements](REQUIREMENTS.md)** - Functional and non-functional requirements
- **[Tasks](TASKS.md)** - Implementation backlog and priorities
- **[Test Case Guidelines](../procedures.yml/test-case-guidelines.yml)** - Comprehensive YAML guidelines for test case selection and implementation
- **[DDD Procedures](../procedures.yml/)** - Feature completion criteria and validation procedures
