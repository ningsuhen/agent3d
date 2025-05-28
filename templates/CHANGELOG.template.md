# Changelog

**FORMAT SPECIFICATION:** This document must provide a comprehensive record of all changes made to the project, organized chronologically and categorized by change type. It must include:

- Clear versioning scheme (Semantic Versioning recommended)
- Chronological organization with most recent changes first
- Categorized changes (Added, Changed, Deprecated, Removed, Fixed, Security)
- DDD pass execution tracking with specific pass types
- Links to relevant documentation, issues, or pull requests
- Breaking change notifications
- Migration guidance for significant changes

**REQUIRED SECTIONS:**

1. Unreleased - Changes not yet released
2. Version Entries - Released versions with dates
3. Change Categories - Organized by type of change
4. DDD Pass Tracking - Record of pass executions
5. Breaking Changes - Significant compatibility changes
6. Migration Notes - Guidance for upgrading

**TEMPLATE:** (Do NOT include `<template>` tags in actual documentation)
<template>

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- {{new_feature_description}}
- {{new_component_description}}

### Changed

- {{modified_feature_description}}
- {{updated_behavior_description}}

### Deprecated

- {{deprecated_feature_description}}

### Removed

- {{removed_feature_description}}

### Fixed

- {{bug_fix_description}}
- {{issue_resolution_description}}

### Security

- {{security_improvement_description}}

### DDD Pass Executions

- **{{pass_date}}**: {{pass_type}} Pass - {{pass_description}}
- **{{pass_date}}**: {{pass_type}} Pass - {{pass_description}}

## [{{version}}] - {{release_date}}

### Added

- {{feature_description}} ([#{{issue_number}}]({{issue_link}}))
- {{component_description}} - {{detailed_explanation}}

### Changed

- **BREAKING**: {{breaking_change_description}}
- {{improvement_description}} ([#{{pr_number}}]({{pr_link}}))

### Fixed

- {{bug_description}} ([#{{issue_number}}]({{issue_link}}))

### DDD Pass Executions

- **{{pass_date}}**: Full Pass - {{comprehensive_update_description}}
- **{{pass_date}}**: Foundation Pass - {{foundation_changes}}
- **{{pass_date}}**: Documentation Pass - {{documentation_updates}}
- **{{pass_date}}**: Planning Pass - {{planning_activities}}
- **{{pass_date}}**: Implementation Pass - {{implementation_changes}}
- **{{pass_date}}**: Testing Pass - {{testing_improvements}}
- **{{pass_date}}**: Refactoring Pass - {{refactoring_changes}}
- **{{pass_date}}**: Code Review Pass - {{review_outcomes}}
- **{{pass_date}}**: Synchronization Pass - {{sync_changes}}
- **{{pass_date}}**: Quality Pass - {{quality_improvements}}
- **{{pass_date}}**: Prune Pass - {{cleanup_actions}}
- **{{pass_date}}**: Reverse Pass - {{reverse_drift_fixes}}

### Migration Notes

- {{migration_instruction_1}}
- {{migration_instruction_2}}

## [{{previous_version}}] - {{previous_date}}

### Added

- {{previous_feature_description}}

### Changed

- {{previous_change_description}}

### Fixed

- {{previous_fix_description}}

### DDD Pass Executions

- **{{pass_date}}**: {{pass_type}} Pass - {{pass_description}}
</template>

**EXAMPLE:** See the actual CHANGELOG.md file in the local repository: `~/.agent3d/CHANGELOG.md`

**VALIDATION CHECKLIST:**

- [ ] All universal validation rules from [Common Procedures](../docs/COMMON-PROCEDURES.md#common-validation-checklist) are met
- [ ] All changes are categorized appropriately (Added, Changed, Fixed, etc.)
- [ ] DDD pass executions are recorded with dates and descriptions
- [ ] Breaking changes are clearly marked and explained
- [ ] Version numbers follow semantic versioning
- [ ] Most recent changes appear first
