# Documentation-Driven Development (DDD) for LLM Coding Agents
## MCP-First Architecture

*"Write the docs, then write the code—keep it lean, test it for real."*

## Configuration

All Agent3D resources are accessed through the **Agent3D MCP Server**. Agents should never directly access file systems or know about specific locations like `~/.agent3d`.

**🚨 CRITICAL ACCESS RULE**: Always use MCP tools to access DDD framework resources. Never use direct file system commands. All operations go through the `agent3d-mcp` server:

### Available MCP Tools:

#### Framework Access Tools:
- `get_template` - Get documentation templates (README, REQUIREMENTS, etc.)
- `get_language_rules` - Get coding standards for specific languages
- `get_pass_definition` - Get DDD pass workflows and procedures
- `get_project_config` - Get project configuration (.agent3d-config.yml)

#### Workflow Management Tools:
- `next_action` - Get intelligent guidance on what to do next
- `save_exec_plan` - Save execution plans to docs/runs directory
- `update_exec_plan` - Update existing execution plans with progress

#### Search and Analysis Tools:
- `search_files` - Semantic file search across repository
- `search_test_cases` - Find test cases (TC-*) in documentation
- `search_features` - Find feature specifications (FT-*)
- `find_feature_test_mapping` - Map features to test cases
- `analyze_drift` - Detect documentation-code inconsistencies
- `validate_code_locations` - Verify feature code locations
- `get_vector_stats` - Get repository indexing statistics

**Project Configuration:** Each project uses `.agent3d-config.yml` in the project root to define project-specific settings, enabled passes, and quality standards.

## Project Root Detection

**CRITICAL**: The MCP server automatically detects project roots by looking for `.agent3d-config.yml` files. Agents don't need to know about specific paths.

## Prime Directive

**Documentation leads, code follows.** Always update docs before implementing code. Documentation is the single source of truth.

## Core Workflow

| Phase | Action | Human Role |
|-------|--------|-----------|
| **Scan** | Detect missing/outdated docs via MCP | — |
| **Draft** | Create/update documentation | — |
| **Ask** | Clarify gaps and decisions | Provide input |
| **Sync** | Implement code matching docs | Review & approve |

**Project Setup**: Configure project with `.agent3d-config.yml` in project root
**DDD Pass**: Execute Scan → Draft → Ask → Sync → Confirm (if git_workflow.require_commit_confirmation=true), commit with `DDD: <description>`

### DDD Passes

Access pass definitions through MCP `search_files` tool:
- Full Pass - Comprehensive pass encompassing all aspects
- 0. Requirements Pass - Documenting comprehensive requirements and business objectives
- 1. Foundation Pass - Project configuration and foundational setup
- 2. Documentation Pass - Documenting features, requirements, and priorities
- 3. Development Pass - Step-by-step feature implementation with checkpoints and execution plans
- 4. Testing Pass - Adding comprehensive tests and verifying edge cases
- 5. Refactoring Pass - Cleaning up code without changing functionality
- 6. Code Review Pass - Reviewing PR changes and providing feedback
- 7. Synchronization Pass - Aligning documentation with code at any scale
- 8. Prune Pass - Removing outdated or redundant content
- 9. Reverse Pass - Detecting and addressing reverse drift (implementation without documentation)

---

## Development Principles

| Principle | Rule |
|-----------|------|
| **Requirements-Driven** | Implement only documented requirements from `docs/REQUIREMENTS.md` |
| **Lean Code** | Build only what is specified in requirements and acceptance criteria |
| **Real Tests** | **CRITICAL**: Tests MUST import and call actual project code - never test only mock data |
| **Project Code Testing** | **CRITICAL**: Every test must import from project source and call project functions |
| **Integration Focus** | Prefer integration tests over pure unit tests; avoid mocks except for external APIs |
| **Judicious Testing** | **CRITICAL**: Select test cases based on feature needs and risk - quality over quantity |
| **Full Traceability** | Link requirements (`REQ-####`) to features to test cases (`TC-####`) |
| **Requirements Validation** | Ensure all features trace back to business objectives |
| **Fast Feedback** | Run critical tests in CI |
| **Language Rules** | Use MCP to fetch language-specific rules, apply consistently |
| **LLM-Friendly Docs** | Use clear, concise language; consistent structure; no legacy references |

### Language-Specific Rules

Use MCP `search_files` tool to access language-specific rules:
- Markdown - Rules for Markdown documentation and LLM optimization
- Python - Rules for Python development
- JavaScript - Rules for JavaScript development
- Java - Rules for Java development
- Go - Rules for Go development

---

## Required Documentation

| File | Purpose | Access Method |
|------|---------|---------------|
| `README.md` | Project overview | Use MCP `search_files` for template |
| `docs/BUSINESS-OBJECTIVES.md` | Business goals, metrics, and success criteria | Use MCP `search_files` for template |
| `docs/REQUIREMENTS.md` | Comprehensive functional and non-functional requirements | Use MCP `search_files` for template |
| `docs/USER-STORIES.md` | User personas, stories, and use cases | Use MCP `search_files` for template |
| `docs/ACCEPTANCE-CRITERIA.md` | Testable acceptance criteria for all requirements | Use MCP `search_files` for template |
| `docs/FEATURES.md` | Feature checklist with acceptance criteria | Use MCP `search_features` tool |
| `docs/HIGH-LEVEL-DESIGN.md` | System design with diagrams and decisions | Use MCP `search_files` for template |
| `docs/TASKS.md` | Work backlog organized by priority | Use MCP `search_files` for template |
| `docs/TEST-CASES.md` | Test specifications with TC-#### format | Use MCP `search_test_cases` tool |
| `docs/TC-SUBTEST-GUIDELINES.md` | Test Case and Sub-Test implementation guidelines | Use MCP `search_files` |
| `docs/DDD-STATUS.yml` | DDD Pass Status, Drift and Health tracking | Use MCP `analyze_drift` tool |
| `docs/designs/*.md` | Component design specifications | Use MCP `search_files` for template |
| `docs/proposals/*.md` | Design proposals for unimplemented features | Use MCP `search_files` for template |
| `docs/migrations/*.yml` | Migration workflows and execution tracking | Use MCP `search_files` |
| `docs/ux/*.md` | UI/UX specifications, wireframes, and user flows (for UI projects) | Use MCP `search_files` for template |
| `CHANGELOG.md` | Chronological record of all project changes | Use MCP `search_files` for template |

**🚨 CRITICAL**: All documentation creation and standards are accessed through MCP tools.

---

## Operational Standards

**Documentation-Code Alignment:**

- Each commit must update documentation OR include `docs-n/a` tag
- **MEMORIZE ENTIRE .agent3d-config.yml** at session start using MCP tools
- **Use memorized git_workflow settings** for commit confirmation behavior
- CI/CD pipelines must validate documentation-code alignment using MCP drift analysis
- Agents must reject tasks that violate DDD principles

## Agent Instructions

**Workflow:**

1. **Always Use MCP Tools:** Use MCP `search_files`, `search_features`, `search_test_cases` etc. - never use direct file system access
2. **Create Mental Memory Map:** Build comprehensive understanding of Agent3D framework through MCP
3. **Check Migration Status:** Use MCP tools to identify applicable migrations
4. **Execute Required Migrations:** Apply any pending migrations before proceeding with development
5. Configure project (`.agent3d-config.yml` in project root)
6. Follow MCP-based DDD guidelines
7. Run DDD pass for missing/outdated documentation using MCP drift analysis
8. **Write Real Tests:** Every test MUST import project code and call project functions
9. **Update Guidelines Regularly:** MCP server automatically stays current with framework updates
10. **Use System Date Commands:** Always use `date +%Y-%m-%d` or `date +%Y-%m-%d\ %H:%M:%S` for timestamps

**MCP Tool Usage Examples:**

```bash
# Get intelligent workflow guidance
next_action()

# Get project configuration
get_project_config()

# Get documentation templates
get_template(template_name="REQUIREMENTS")

# Get language-specific rules
get_language_rules(language="python")

# Save execution plan
save_exec_plan(plan_name="implement-user-auth", plan_data={...})

# Update execution plan with progress
update_exec_plan(plan_name="implement-user-auth", update_status="in_progress")

# Search for templates
search_files(query="README template", file_type="doc")

# Find test cases
search_test_cases(query="authentication tests")

# Find features
search_features(query="user authentication")

# Check drift
analyze_drift(mode="all")

# Validate code locations
validate_code_locations()
```

**Autonomous Agent Workflow:**

1. **Start with guidance**: `next_action()` - Get intelligent next step
2. **Get configuration**: `get_project_config()` - Understand project setup
3. **Follow recommendations**: Use suggested tools from `next_action` response
4. **Save progress**: `save_exec_plan()` - Document execution plan
5. **Update as you go**: `update_exec_plan()` - Track progress and changes
6. **Repeat**: Call `next_action()` again for continuous guidance

**Test Quality Requirements:**

**CRITICAL**: All tests must meet these quality standards:

1. **Import Project Code**: Every test file MUST import modules/classes/functions from actual project source directories
2. **Call Project Functions**: Tests MUST call actual project functions from imported modules
3. **Meaningful Assertions**: Tests MUST validate actual behavior, not trivial comparisons
4. **Integration Focus**: Prefer testing real data flows over pure mock scenarios
5. **TC ID Mapping**: Include TC-NNNN identifier in test function name or docstring for traceability
6. **FT-TC Validation**: **CRITICAL** - When TC is linked to an FT, the test MUST actually use and validate that specific feature functionality
7. **Appropriate TC Description Length**: **CRITICAL** - Keep TC descriptions concise when features provide sufficient detail

**Prohibited Test Patterns:**
- Tests that only use mock data without calling actual project code
- Tests that only assert against hardcoded expected values without importing project modules
- Tests that import only test libraries without importing from project source directories
- Tests with trivial assertions like `assert True`
- Tests that don't import any modules from the actual project codebase
- Tests that use try-except blocks around imports
- Tests linked to an FT that don't actually use or validate the specific feature functionality

**Mental Memory Map Creation:**

- **CRITICAL**: Before starting any work, create a comprehensive mental map using MCP tools
- **Framework Understanding**: Map out DDD passes and their relationships through MCP search
- **Project Context**: Understand project type, configuration, enabled passes through MCP
- **Resource Mapping**: Know how to access templates, rules, procedures through MCP tools
- **Workflow Integration**: Understand how MCP tools work together for effective project execution

**Question Protocol:**

- **CRITICAL**: When asking user questions, ask ONE question at a time
- Wait for user response before asking the next question
- Do not present multiple questions in a single interaction

## LLM Memory Optimization Framework

### Core Memory Map (MEMORIZE)

**CRITICAL:** Internalize these patterns to avoid excessive MCP calls during execution

| Component | Pattern |
|-----------|---------|
| **Execution** | SCAN → DRAFT → ASK → SYNC |
| **Sequence** | REQ → FOUND → DOC → PLAN → IMPL → TEST → REFACT → REVIEW → SYNC → QUAL → PRUNE → REV |
| **MCP Tools** | search_files, search_features, search_test_cases, analyze_drift, validate_code_locations |
| **Quality Gates** | Requirements(objectives), Foundation(config), Documentation(criteria), Planning(checkpoints), Implementation(matches), Testing(passes), Review(rules) |

### Speed Optimization (MEMORIZE)

**CONFIGURATION STRUCTURE:**

```yaml
project: {type, language, quality_level}
enabled_passes: [list]
pass_config: {specific settings}
```

**STATUS PATTERNS:** `[x]` = Complete, `[~]` = In progress, `[ ]` = Not started

**EXECUTION RULES:**

- **ALWAYS** use MCP tools to access DDD framework resources
- **NEVER** use direct file system commands like `cat ~/.agent3d/[filename]`
- **CACHE** frequently used information in working memory
- **MINIMIZE** redundant MCP calls
- **FIRST** check project config through MCP, **THEN** target documents

**DECISION TREE:** Missing requirements→Requirements Pass, No config→Foundation Pass, Features unclear→Documentation Pass, etc.

**MCP Server Connection:**

The MCP server handles all framework access automatically. Agents should focus on the task at hand and use MCP tools as needed.
