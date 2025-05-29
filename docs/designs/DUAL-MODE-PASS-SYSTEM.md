# Dual-Mode Pass System Design

## Overview

The DDD framework now supports two execution modes for each pass: **Complete** and **Incremental**. This provides flexibility for different scenarios and project needs.

## Execution Modes

### Complete Mode
- **Purpose**: Comprehensive execution of the entire pass
- **Scope**: Complete workflow with all phases
- **Use Cases**:
  - New project initialization
  - Major overhauls or migrations
  - Complete documentation reviews
  - First-time pass execution
- **Phases**: `SCAN → DRAFT → ASK → SYNC → CONFIRM`

### Incremental Mode
- **Purpose**: Targeted updates to specific areas
- **Scope**: Focused changes without complete workflow
- **Use Cases**:
  - Minor updates or corrections
  - Specific feature additions
  - Configuration adjustments
  - Quick fixes or improvements
- **Phases**: `SCAN → DRAFT → SYNC`

## Mode Selection Logic

### Automatic Detection
The system automatically determines the appropriate mode based on:

1. **Project State**:
   - New project → Complete Mode
   - Existing project with minor changes → Incremental Mode

2. **Change Scope**:
   - Major changes (>30% of content) → Complete Mode
   - Minor changes (<30% of content) → Incremental Mode

3. **User Intent**:
   - Explicit mode specification in request
   - Context clues from user language

### Manual Override
Users can explicitly specify the mode:
- `Run Foundation Pass --mode=complete`
- `Run Documentation Pass --mode=incremental`

## Phase Differences by Mode

### SCAN Phase
**Complete Mode:**
- Comprehensive project assessment
- Complete gap analysis
- Full dependency review
- Thorough validation checks

**Incremental Mode:**
- Targeted assessment of specific areas
- Focused gap identification
- Minimal dependency validation
- Quick integrity checks

### DRAFT Phase
**Complete Mode:**
- Complete documentation creation/update
- Comprehensive structure establishment
- Full template application
- Complete workflow execution

**Incremental Mode:**
- Targeted updates only
- Preserve existing structure
- Minimal template usage
- Focused workflow execution

### ASK Phase
**Complete Mode:**
- Complete stakeholder engagement
- Comprehensive question flow
- Full validation and confirmation
- Detailed decision documentation

**Incremental Mode:**
- Skipped (streamlined workflow)
- Automatic decisions where possible
- Minimal user interaction
- Quick validation only

### SYNC Phase
**Complete Mode:**
- Complete alignment validation
- Full quality gate execution
- Comprehensive status updates
- Complete documentation sync

**Incremental Mode:**
- Targeted alignment checks
- Essential quality gates only
- Focused status updates
- Minimal documentation sync

### CONFIRM Phase
**Complete Mode:**
- Complete change review
- Full commit preparation
- Comprehensive validation
- Detailed confirmation process

**Incremental Mode:**
- Skipped (auto-commit if configured)
- Quick validation only
- Streamlined confirmation
- Automatic processing

## Implementation Strategy

### 1. Pass File Structure
Each pass file will include:

```yaml
execution_modes:
  complete:
    description: "Complete pass execution"
    phases: ["scan", "draft", "ask", "sync", "confirm"]
    use_cases: ["new_project", "major_changes"]

  incremental:
    description: "Targeted updates only"
    phases: ["scan", "draft", "sync"]
    use_cases: ["minor_updates", "quick_fixes"]

process:
  workflow_patterns:
    complete: "SCAN → DRAFT → ASK → SYNC → CONFIRM"
    incremental: "SCAN → DRAFT → SYNC"

  phases:
    scan:
      complete_mode:
        actions: [comprehensive_actions]
      incremental_mode:
        actions: [targeted_actions]
```

### 2. Mode Detection Algorithm
```yaml
mode_detection:
  criteria:
    project_state:
      new_project: "complete"
      existing_project: "auto_detect"

    change_scope:
      major_changes: "complete"
      minor_changes: "incremental"

    user_intent:
      explicit_mode: "use_specified"
      context_clues: "analyze_request"
```

### 3. Quality Gates by Mode
```yaml
quality_gates:
  complete_mode:
    - "complete_validation"
    - "comprehensive_checks"
    - "full_alignment_verification"

  incremental_mode:
    - "essential_validation"
    - "targeted_checks"
    - "minimal_alignment_verification"
```

## Benefits

### For Users
- **Flexibility**: Choose appropriate level of thoroughness
- **Efficiency**: Faster execution for minor changes
- **Control**: Explicit mode selection when needed
- **Adaptability**: System adapts to project needs

### For Development Teams
- **Productivity**: Reduced overhead for small changes
- **Quality**: Full validation when needed
- **Consistency**: Standardized approach across passes
- **Maintainability**: Clear separation of concerns

### For LLM Agents
- **Decision Making**: Clear criteria for mode selection
- **Efficiency**: Optimized workflows for different scenarios
- **Consistency**: Standardized patterns across passes
- **Adaptability**: Context-aware execution

## Migration Plan

### Phase 1: Framework Design ✅
- Define dual-mode architecture
- Create implementation guidelines
- Document mode selection criteria

### Phase 2: Core Pass Updates
- Update Foundation Pass
- Update Requirements Pass
- Update Documentation Pass
- Update Development Pass

### Phase 3: Advanced Pass Updates
- Update Testing Pass
- Update Refactoring Pass
- Update Code Review Pass
- Update Synchronization Pass

### Phase 4: Integration and Testing
- Update AGENT-GUIDELINES.yml
- Test mode detection logic
- Validate workflow execution
- Performance optimization

## Usage Examples

### Complete Mode Examples
```bash
# New project setup
"Initialize a new Python web application project"
→ Foundation Pass (Complete Mode)

# Major documentation overhaul
"Complete documentation review and update"
→ Documentation Pass (Complete Mode)

# Comprehensive testing implementation
"Implement complete test suite for all features"
→ Testing Pass (Complete Mode)
```

### Incremental Mode Examples
```bash
# Add single feature
"Add user authentication feature documentation"
→ Documentation Pass (Incremental Mode)

# Update configuration
"Add new quality threshold for code coverage"
→ Foundation Pass (Incremental Mode)

# Fix specific test
"Fix failing test for user login functionality"
→ Testing Pass (Incremental Mode)
```

## Success Metrics

### Performance Metrics
- **Execution Time**: 50% reduction for incremental mode
- **User Interaction**: 70% reduction in questions for incremental mode
- **File Changes**: Minimal changes for incremental updates

### Quality Metrics
- **Accuracy**: Maintain quality standards in both modes
- **Completeness**: Full coverage in complete mode, targeted coverage in incremental mode
- **Consistency**: Uniform behavior across all passes

### User Experience Metrics
- **Satisfaction**: Improved user experience with appropriate mode selection
- **Efficiency**: Faster completion for routine tasks
- **Flexibility**: Better adaptation to different use cases
