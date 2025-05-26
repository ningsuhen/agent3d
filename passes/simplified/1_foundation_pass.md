# Foundation Pass

**Purpose:** Establish project foundation through configuration discovery, feature selection, and initial project setup after requirements are understood. Configure Agent3D features based on requirements and establish the project's operational framework and basic structure.

**Role:** Assume the role of a **Project Setup Specialist** with expertise in project initialization, configuration management, and foundation establishment. Focus on understanding project context, configuring appropriate tooling, establishing basic project structure, and setting the foundation for all subsequent DDD passes. Think like a setup expert who ensures the project starts with the right configuration, scope, and foundational elements.

## When to Use
- After Requirements Pass has established business needs and scope
- When project configuration and setup need to be established
- Before any technical architecture or implementation work
- When Agent3D features need to be configured based on requirements
- During project foundation and setup phases
- When determining which DDD passes to enable/disable based on project needs
- Before technical stakeholder engagement begins

## Process
1. **Scan:** [Repository Management](../docs/COMMON-PROCEDURES.md#repository-management), review requirements, check `.agent3d-config.yml`, identify project type
2. **Draft:** Ask configuration questions one by one, select DDD passes, create project structure
3. **Ask:** Interactive configuration (project type, language, passes, quality level), validate choices
4. **Sync:** Save `.agent3d-config.yml`, create structure, establish docs framework, create DDD-STATUS.md

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Project configuration (`.agent3d-config.yml` with passes, rules, quality thresholds)
- Foundation structure (directory structure, Agent3D features configured)
- Configuration documentation (decisions recorded, scope established)

## Related Passes
Requirements → **Foundation** → Documentation

## Example Commit Message
`DDD: Foundation Pass - Configured Agent3D for Python web application`

## Configuration Questions Framework

### Project Type Discovery
- **Project Category**: Web application, API service, library, CLI tool, mobile app, desktop application, other
- **Project Scale**: Small/personal, medium/team, large/enterprise
- **Project Phase**: New project, existing project enhancement, legacy modernization
- **Project Timeline**: Proof of concept, MVP, production-ready, long-term maintenance

### Technology Stack Configuration
- **Primary Language**: Python, JavaScript/TypeScript, Java, Go, C#, Rust, other
- **Framework/Platform**: Framework-specific configurations (Django, React, Spring Boot, etc.)
- **Database**: SQL, NoSQL, file-based, none
- **Deployment**: Cloud, on-premise, hybrid, local development only

### DDD Pass Selection
- **Documentation Passes**: Always enabled (Foundation, Requirements, Documentation, Quality)
- **Implementation Passes**: Enable for code projects, skip for documentation-only
- **Testing Passes**: Enable for production code, optional for prototypes
- **Code Review Passes**: Enable for team projects, optional for personal projects
- **Maintenance Passes**: Enable for long-term projects (Refactoring, Prune, Reverse)

### Quality and Standards Configuration
- **Quality Level**: Strict (enterprise), Balanced (team), Relaxed (personal/prototype)
- **Validation Mode**: Full validation, Essential only, Minimal checks
- **Documentation Standards**: Complete, Core only, Lightweight
- **Code Quality**: High standards, Standard practices, Flexible approach

## Interactive Configuration Process

### Step-by-Step Question Flow
1. **Project Context**: "What type of project are you working on?"
2. **Language Selection**: "What is your primary programming language?"
3. **Team Structure**: "Is this a personal project or team project?"
4. **Quality Requirements**: "What quality level do you need? (strict/balanced/relaxed)"
5. **Pass Selection**: "Which DDD passes do you want to enable?"
6. **Custom Configuration**: "Any specific configuration requirements?"

### Configuration Validation
- Validate configuration choices for consistency
- Warn about potential conflicts or missing dependencies
- Suggest optimal configurations based on project type
- Confirm final configuration before saving

## Sample Configuration Files

### Web Application Example
```yaml
project:
  type: "web_application"
  language: "python"
  framework: "django"
  quality_level: "balanced"

enabled_passes:
  - foundation
  - requirements
  - documentation
  - implementation
  - testing
  - code_review
  - synchronization
  - quality

skip_passes:
  - prune
  - reverse
```

### Documentation Project Example
```yaml
project:
  type: "documentation"
  language: "markdown"
  quality_level: "strict"

enabled_passes:
  - foundation
  - requirements
  - documentation
  - quality

skip_passes:
  - implementation
  - testing
  - code_review
  - refactoring
```

## Quality Gates
- [ ] Project type and scope clearly defined
- [ ] Technology stack configuration completed
- [ ] DDD pass selection finalized
- [ ] Quality standards established
- [ ] Configuration file created and validated
- [ ] Project foundation structure established
- [ ] Handoff to Requirements Pass prepared
