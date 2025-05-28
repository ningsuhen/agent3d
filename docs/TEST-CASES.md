# Test Cases

This document outlines the test cases for the Agent3D framework, organized by features using FT-* identifiers for traceability.

## 📊 Summary
- **Total Test Cases:** 106 (61 main + 45 sub-test cases)
- **Completed:** 61 ✅ (35 main + 26 sub-test cases)
- **Pending:** 45 ⏸️ (26 main + 19 sub-test cases)
- **Skipped:** 0 ⏭️
- **Automated:** 54 (51%)
- **Partial:** 22 (21%)
- **Manual:** 30 (28%)

## 🔧 Test Execution Framework

### Manual Testing Procedures
- **Documentation Review:** Systematic validation of documentation completeness and accuracy
- **Workflow Validation:** Step-by-step verification of DDD pass execution
- **Cross-Reference Checking:** Validation of links and references between documents

### Automated Testing Integration
- **CI/CD Validation:** Automated checks for documentation-code alignment
- **Link Validation:** Automated verification of internal and external links
- **Format Validation:** Automated checking of markdown formatting and structure

### Integration Testing with LLM Agents
- **End-to-End Workflow:** Complete DDD pass execution with real agents
- **Guideline Compliance:** Verification that agents follow documented procedures
- **Output Validation:** Checking that agent outputs match expected documentation standards

## 🏗️ Core Documentation Framework

### **FT-CORE-001** Agent Guideline Protocol
- [x] **TC-0001** - Agent retrieves and caches guidelines (Manual, High)
  - [x] **TC-0001a** - Initial guideline fetch from remote URL (Manual, High)
  - [x] **TC-0001b** - Local cache creation and storage (Manual, High)
  - [x] **TC-0001c** - Cache validation and integrity check (Manual, Medium)
- [x] **TC-0002** - Agent updates cached guidelines when remote changes (Manual, High)
  - [x] **TC-0002a** - Periodic remote change detection (Manual, High)
  - [x] **TC-0002b** - Automatic cache update on changes (Manual, High)
  - [x] **TC-0002c** - Update logging and error handling (Manual, Medium)
- [x] **TC-0003** - Agent follows cached guidelines for decisions (Manual, High)
  - [x] **TC-0003a** - Decision-making based on cached guidelines (Manual, High)
  - [x] **TC-0003b** - Fallback behavior when cache is unavailable (Manual, Medium)

### **FT-CORE-002** DDD Pass System
- [x] **TC-0101** - Foundation Pass creates architecture docs (Manual, High)
  - [x] **TC-0101a** - README.md creation and validation (Manual, High)
  - [x] **TC-0101b** - HIGH-LEVEL-DESIGN.md documentation (Manual, High)
  - [x] **TC-0101c** - FEATURES.md with acceptance criteria (Manual, High)
  - [x] **TC-0101d** - TASKS.md prioritization and structure (Manual, Medium)
- [x] **TC-0102** - Documentation Pass resolves ambiguities (Manual, High)
  - [x] **TC-0102a** - Feature specification completeness (Manual, High)
  - [x] **TC-0102b** - Test case documentation coverage (Manual, High)
  - [x] **TC-0102c** - Acceptance criteria validation (Manual, Medium)
- [ ] **TC-0103** - Implementation Pass follows documentation (Manual, High)
  - [ ] **TC-0103a** - Feature implementation matches specifications (Manual, High)
  - [ ] **TC-0103b** - Basic test coverage for core functionality (Manual, High)
  - [ ] **TC-0103c** - Code quality standards compliance (Manual, Medium)
- [ ] **TC-0104** - Testing Pass adds comprehensive coverage (Manual, Medium)
  - [ ] **TC-0104a** - Test framework setup and configuration (Automated, High)
  - [ ] **TC-0104b** - Edge case and boundary testing (Manual, Medium)
  - [ ] **TC-0104c** - Integration test implementation (Manual, Medium)
- [ ] **TC-0105** - Refactoring Pass improves code without losing features (Manual, Medium)
  - [ ] **TC-0105a** - Code structure and style improvements (Manual, Medium)
  - [ ] **TC-0105b** - Performance optimization without breaking changes (Manual, Low)
  - [ ] **TC-0105c** - Functionality preservation validation (Automated, High)
- [ ] **TC-0106** - Code Review Pass provides meaningful feedback (Manual, High)
  - [ ] **TC-0106a** - PR review process execution (Manual, High)
  - [ ] **TC-0106b** - Feedback template usage and consistency (Manual, Medium)
  - [ ] **TC-0106c** - Review automation integration (Automated, Medium)
- [ ] **TC-0107** - Synchronization Pass aligns docs with code (Manual, High)
  - [ ] **TC-0107a** - Documentation-code drift detection (Manual, High)
  - [ ] **TC-0107b** - Cross-reference validation and updates (Manual, Medium)
  - [ ] **TC-0107c** - Version consistency verification (Manual, Medium)
- [ ] **TC-0108** - Quality Pass improves documentation clarity (Manual, Medium)
  - [ ] **TC-0108a** - Content quality assessment and improvement (Manual, Medium)
  - [ ] **TC-0108b** - Formatting consistency validation (Manual, Low)
  - [ ] **TC-0108c** - Clarity and readability enhancement (Manual, Medium)
- [ ] **TC-0109** - Prune Pass removes outdated content safely (Manual, Low)
  - [ ] **TC-0109a** - Outdated content identification (Manual, Low)
  - [ ] **TC-0109b** - Safe removal without breaking references (Manual, Medium)
  - [ ] **TC-0109c** - Archive and backup procedures (Manual, Low)
- [ ] **TC-0110** - Full Pass maintains doc-code alignment across all aspects (Manual, High)
  - [ ] **TC-0110a** - All passes execution in sequence (Manual, High)
  - [ ] **TC-0110b** - Alignment level balancing across passes (Manual, High)
  - [ ] **TC-0110c** - Overall drift reduction validation (Manual, High)

### **FT-CORE-003** Documentation Standards
- [ ] **TC-0311** - Documentation matches current implementation (Manual, High)
- [ ] **TC-0312** - All features documented in FEATURES.md (Manual, High)
- [ ] **TC-0313** - Test cases reference TC-#### format (Manual, Medium)

## 🔤 Language-Specific Rules

### **FT-LANG-001** Python Rules
- [ ] **TC-0201** - Python code follows PEP 8 and project rules (Partial, Medium)
  - [ ] **TC-0201a** - Line length and formatting compliance (Automated, Medium)
  - [ ] **TC-0201b** - Import organization and style (Automated, Medium)
  - [ ] **TC-0201c** - Naming conventions adherence (Partial, Medium)
- [ ] **TC-0202** - Virtual environment setup at project root (Manual, High)
  - [ ] **TC-0202a** - Virtual environment creation and activation (Manual, High)
  - [ ] **TC-0202b** - Dependencies installation and management (Manual, High)
- [ ] **TC-0203** - Type hints used for function args and returns (Partial, Medium)
  - [ ] **TC-0203a** - Function parameter type annotations (Partial, Medium)
  - [ ] **TC-0203b** - Return type annotations (Partial, Medium)
- [ ] **TC-0204** - Dataclasses preferred over dict objects (Manual, Medium)

### **FT-LANG-002** JavaScript Rules
- [ ] **TC-0211** - JavaScript code follows style guide (Partial, Medium)
  - [ ] **TC-0211a** - ESLint configuration and compliance (Automated, Medium)
  - [ ] **TC-0211b** - Code formatting with Prettier (Automated, Medium)
- [ ] **TC-0212** - Consistent package management (npm/yarn) (Manual, High)
  - [ ] **TC-0212a** - Package manager selection and configuration (Manual, High)
  - [ ] **TC-0212b** - Lock file management and consistency (Manual, Medium)
- [ ] **TC-0213** - ES6+ features used appropriately (Manual, Medium)

### **FT-LANG-003** Java Rules
- [ ] **TC-0221** - Java code follows Google style guide (Partial, Medium)
- [ ] **TC-0222** - Proper exception handling patterns (Manual, Medium)
- [ ] **TC-0223** - Thread safety considerations (Manual, High)

### **FT-LANG-004** Go Rules
- [x] **TC-0231** - Go code follows standard formatting (Automated, High)
- [ ] **TC-0232** - Proper package organization (Partial, Medium)
- [ ] **TC-0233** - Error handling patterns (Partial, High)

### **FT-LANG-005** Markdown Rules
- [ ] **TC-0241** - Markdown follows linting standards (Automated, High)
- [ ] **TC-0242** - Documentation quality validation (Manual, Medium)
- [ ] **TC-0243** - Cross-reference consistency (Manual, Medium)

## 📋 Enhanced Template System

### **FT-TMPL-001** Template Engine
- [x] **TC-0801** - Template inheritance system validation (Manual, High)
  - [x] **TC-0801a** - BASE template provides common structure and validation (Manual, High)
  - [x] **TC-0801b** - Specialized templates properly extend base template (Manual, High)
  - [x] **TC-0801c** - Template metadata is complete and accurate (Manual, Medium)
- [x] **TC-0802** - Context-aware template selection (Manual, High)
  - [x] **TC-0802a** - Language detection works for supported languages (Manual, High)
  - [x] **TC-0802b** - Framework detection identifies common frameworks (Manual, High)
  - [x] **TC-0802c** - Project type detection categorizes projects correctly (Manual, Medium)
- [x] **TC-0803** - Dynamic content generation (Manual, High)
  - [x] **TC-0803a** - Templates adapt content based on project context (Manual, High)
  - [x] **TC-0803b** - Auto-detection variables are populated correctly (Manual, Medium)
  - [x] **TC-0803c** - Intelligent suggestions are relevant and helpful (Manual, Medium)

### **FT-TMPL-002** Simple Template Access
- [x] **TC-0811** - Template registry configuration (Manual, High)
  - [x] **TC-0811a** - Registry contains all template metadata (Manual, High)
  - [x] **TC-0811b** - Template relationships are properly defined (Manual, Medium)
  - [x] **TC-0811c** - Selection algorithm configuration is complete (Manual, Medium)
- [x] **TC-0812** - Template selection algorithm (Manual, High)
  - [x] **TC-0812a** - Algorithm scores templates based on project analysis (Manual, High)
  - [x] **TC-0812b** - Recommendations are ranked by relevance (Manual, Medium)
  - [x] **TC-0812c** - Fallback templates work when no good matches found (Manual, Medium)

### **FT-TMPL-003** Validation Framework
- [x] **TC-0821** - Multi-level validation system (Manual, High)
  - [x] **TC-0821a** - Base validation rules apply to all templates (Manual, High)
  - [x] **TC-0821b** - Context-specific validation adapts to project type (Manual, High)
  - [x] **TC-0821c** - Quality assurance checks maintain Agent3D standards (Manual, Medium)
- [ ] **TC-0822** - Template validation integration (Manual, High)
  - [ ] **TC-0822a** - Validation runs during template generation (Manual, High)
  - [ ] **TC-0822b** - Validation errors provide actionable feedback (Manual, Medium)
  - [ ] **TC-0822c** - Validation passes for properly generated content (Manual, Medium)

### **FT-TMPL-004** System Date Commands
- [ ] **TC-0831** - Date command integration (Manual, High)
- [ ] **TC-0832** - Template timestamp accuracy (Manual, Medium)
- [ ] **TC-0833** - LLM independence validation (Manual, Medium)

## 🏗️ Proposal System

### **FT-PROP-001** Proposal Framework
- [x] **TC-0601** - Proposal template validation (Manual, High)
  - [x] **TC-0601a** - PROPOSAL template includes all required sections (Manual, High)
  - [x] **TC-0601b** - Proposal status tracking works correctly (Manual, Medium)
- [x] **TC-0602** - Proposal directory structure validation (Manual, High)
  - [x] **TC-0602a** - docs/proposals/active/ directory exists (Manual, High)
  - [x] **TC-0602b** - docs/proposals/archive/ subdirectories exist (Manual, Medium)
- [ ] **TC-0603** - Proposal lifecycle workflow (Manual, High)
  - [ ] **TC-0603a** - Proposal moves from Draft to Under Review (Manual, High)
  - [ ] **TC-0603b** - Approved proposals integrate into main docs (Manual, High)
  - [ ] **TC-0603c** - Implemented proposals archive correctly (Manual, Medium)

### **FT-PROP-002** Component Design System
- [x] **TC-0611** - DETAILED-DESIGN template validation (Manual, High)
  - [x] **TC-0611a** - Template includes all technical specifications (Manual, High)
  - [x] **TC-0611b** - Migration checklist for existing projects (Manual, Medium)
- [x] **TC-0612** - Component integration workflow (Manual, High)
  - [x] **TC-0612a** - Proposals integrate into docs/designs/ with {COMPONENT}.md naming (Manual, High)
  - [x] **TC-0612b** - HIGH-LEVEL-DESIGN.md links to component design docs (Manual, Medium)
  - [x] **TC-0612c** - All documentation files use CAPS naming convention (Manual, Medium)
  - [x] **TC-0612d** - Component designs contain specifications for project parts (Manual, Medium)

## 🔄 Integration Guidelines

### **FT-INTG-001** LLM Agent Integration
- [ ] **TC-0411** - Agent follows Scan → Draft → Ask → Sync workflow (Manual, High)
- [ ] **TC-0412** - Agent marks progress with ✅ during execution (Manual, Medium)
- [ ] **TC-0413** - Agent commits with proper DDD messages (Manual, Medium)

### **FT-INTG-002** CI/CD Integration
- [ ] **TC-0401** - Documentation validation in CI pipeline (Automated, Medium)
- [ ] **TC-0402** - Language-specific linting in CI (Automated, Medium)
- [x] **TC-0403** - Test execution in CI pipeline (Automated, High)

### **FT-INTG-003** Version Control Integration
- [ ] **TC-0421** - Documentation changes tracked in version control (Manual, High)
- [ ] **TC-0422** - Version control validation prevents drift (Manual, Medium)
- [ ] **TC-0423** - Documentation branching strategy (Manual, Medium)

### **FT-INTG-004** VSCode DDD Navigator Extension
- [x] **TC-0431** - VSCode extension installation and activation (Manual, High)
  - [x] **TC-0431a** - Extension builds and packages successfully (Automated, High)
  - [x] **TC-0431b** - Extension installs via install.sh script (Manual, High)
  - [x] **TC-0431c** - Extension activates in VSCode without errors (Manual, High)
- [x] **TC-0432** - Identifier navigation functionality (Manual, High)
  - [x] **TC-0432a** - Cmd+Click navigation works for TC-* identifiers (Manual, High)
  - [x] **TC-0432b** - Cmd+Click navigation works for REQ-* identifiers (Manual, High)
  - [x] **TC-0432c** - Cmd+Click navigation works for FT-* identifiers (Manual, High)
- [x] **TC-0433** - Quick pick navigation commands (Manual, High)
  - [x] **TC-0433a** - Ctrl+Shift+T opens test case picker (Manual, High)
  - [x] **TC-0433b** - Ctrl+Shift+R opens requirement picker (Manual, High)
  - [x] **TC-0433c** - Ctrl+Shift+F opens feature picker (Manual, High)
- [x] **TC-0434** - Real-time indexing and file watching (Manual, Medium)
  - [x] **TC-0434a** - Index updates when markdown files change (Manual, Medium)
  - [x] **TC-0434b** - Index updates when code files change (Manual, Medium)
  - [x] **TC-0434c** - File system watcher handles file creation/deletion (Manual, Medium)
- [x] **TC-0435** - Hover providers and rich preview (Manual, Medium)
  - [x] **TC-0435a** - Hover shows identifier status and description (Manual, Medium)
  - [x] **TC-0435b** - Hover shows related items and cross-references (Manual, Medium)
- [x] **TC-0436** - Configurable patterns and settings (Manual, Medium)
  - [x] **TC-0436a** - Custom identifier patterns work correctly (Manual, Medium)
  - [x] **TC-0436b** - Custom file locations are respected (Manual, Medium)
  - [x] **TC-0436c** - Extension settings persist across sessions (Manual, Low)

### **FT-INTG-005** MCP Server Integration
- [x] **TC-0441** - MCP server initialization and protocol (Automated, High)
  - [x] **TC-0441a** - MCP server starts and responds to initialize request (Automated, High)
  - [x] **TC-0441b** - JSON-RPC protocol compliance validation (Automated, High)
  - [x] **TC-0441c** - Error handling for malformed requests (Automated, Medium)
- [x] **TC-0442** - Multi-mode drift analysis via MCP (Automated, High)
  - [x] **TC-0442a** - tc-mapping mode works via MCP interface (Automated, High)
  - [x] **TC-0442b** - ft-mapping mode works via MCP interface (Automated, High)
  - [x] **TC-0442c** - code-coverage mode works via MCP interface (Automated, High)
  - [x] **TC-0442d** - all modes work via MCP interface (Automated, High)
- [x] **TC-0443** - Virtual environment integration (Manual, High)
  - [x] **TC-0443a** - Shell wrapper activates Python venv correctly (Manual, High)
  - [x] **TC-0443b** - PyYAML dependency is installed automatically (Manual, High)
  - [x] **TC-0443c** - MCP server works without system-wide Python packages (Manual, Medium)
- [x] **TC-0444** - Fresh scan mode validation (Automated, Medium)
  - [x] **TC-0444a** - Each MCP request performs fresh analysis (Automated, Medium)
  - [x] **TC-0444b** - No caching between MCP requests (Automated, Medium)
  - [x] **TC-0444c** - Real-time repository state reflection (Manual, Medium)

## 📊 Status Tracking

### **FT-STAT-001** DDD Status Tracking
- [ ] **TC-0501** - Pass status monitoring (Manual, High)
- [ ] **TC-0502** - Alignment metrics calculation (Manual, High)
- [ ] **TC-0503** - Drift indicators display (Manual, Medium)

### **FT-STAT-002** Change Tracking
- [x] **TC-0701** - CHANGELOG template validation (Manual, High)
  - [x] **TC-0701a** - Template includes all required sections and categories (Manual, High)
  - [x] **TC-0701b** - DDD pass integration guidance is comprehensive (Manual, Medium)
- [x] **TC-0702** - CHANGELOG maintenance workflow (Manual, High)
  - [x] **TC-0702a** - Changes are properly categorized (Added, Changed, Fixed, etc.) (Manual, High)
  - [x] **TC-0702b** - DDD pass executions are recorded with dates and descriptions (Manual, High)
  - [x] **TC-0702c** - Semantic versioning is applied correctly (Manual, Medium)
- [ ] **TC-0703** - CHANGELOG integration with DDD passes (Manual, High)
  - [ ] **TC-0703a** - Foundation Pass updates CHANGELOG with architectural changes (Manual, High)
  - [ ] **TC-0703b** - Full Pass updates CHANGELOG with comprehensive changes (Manual, High)
  - [ ] **TC-0703c** - Breaking changes are properly documented and marked (Manual, Medium)

### **FT-STAT-003** Progress Indicators
- [ ] **TC-0711** - Visual progress bars (Manual, Medium)
- [ ] **TC-0712** - Completion statistics (Manual, Medium)
- [ ] **TC-0713** - Progress tracking accuracy (Manual, High)

### **FT-STAT-004** Drift Detection
- [ ] **TC-0501** - Forward drift detection - Documentation exists without corresponding implementation (Automated, High)
  - [ ] **TC-0501a** - Features documented but not implemented (Automated, High)
  - [ ] **TC-0501b** - API documentation without actual endpoints (Automated, High)
  - [ ] **TC-0501c** - Test cases without corresponding feature code (Manual, Medium)
- [ ] **TC-0502** - Features marked complete without verifiable tests (Automated, High)
  - [ ] **TC-0502a** - Features marked [x] without passing tests (Automated, High)
  - [ ] **TC-0502b** - Features marked [x] without manual verification (Manual, High)
- [ ] **TC-0503** - Documentation references non-existent code components (Automated, Medium)
- [ ] **TC-0504** - FT-TC relationship drift detection (Automated, High)
  - [ ] **TC-0504a** - FT-* features without corresponding TC-* test cases (Automated, High)
  - [ ] **TC-0504b** - TC-* test cases without corresponding FT-* features (Automated, High)
  - [ ] **TC-0504c** - Orphaned FT-* identifiers referenced in code but not documented (Automated, Medium)
  - [ ] **TC-0504d** - Missing FT-* ↔ TC-* cross-references in documentation (Automated, Medium)
- [ ] **TC-0505** - Identifier pattern validation (Automated, High)
  - [ ] **TC-0505a** - FT-* identifiers follow configured pattern format (Automated, High)
  - [ ] **TC-0505b** - TC-* identifiers follow configured pattern format (Automated, High)
  - [ ] **TC-0505c** - REQ-* and other identifiers follow configured patterns (Automated, Medium)
- [ ] **TC-0511** - Reverse drift detection - Implementation exists without corresponding documentation (Automated, High)
  - [ ] **TC-0511a** - Code features not documented in FEATURES.md (Automated, High)
  - [ ] **TC-0511b** - API endpoints without documentation (Automated, High)
  - [ ] **TC-0511c** - Database schema without architecture docs (Manual, Medium)
- [ ] **TC-0512** - Features implemented but marked as pending in FEATURES.md (Automated, High)
  - [ ] **TC-0512a** - Working features still marked [ ] or [~] (Automated, High)
  - [ ] **TC-0512b** - Deployed features not reflected in documentation (Manual, High)
- [ ] **TC-0513** - Code functionality exists without test case coverage (Automated, Medium)
  - [ ] **TC-0513a** - Functions/methods without corresponding test cases (Automated, Medium)
  - [ ] **TC-0513b** - Business logic without validation tests (Manual, Medium)
- [ ] **TC-0514** - Configuration or environment changes without documentation (Manual, Medium)
  - [ ] **TC-0514a** - New environment variables without README updates (Manual, Medium)
  - [ ] **TC-0514b** - Deployment changes without architecture updates (Manual, Medium)