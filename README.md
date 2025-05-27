# Agent3D - Documentation-Driven Development for LLM Agents

**Documentation-only** framework for LLM coding agents. DDD principles: documentation precedes code implementation.

**Core Principle:** "Write the docs, then write the code—keep it lean, test it for real."

## Features & Usage

**Features:** LLM speed optimized, memory-cached patterns (SCAN→DRAFT→ASK→SYNC), configuration-centric (`.agent3d-config.yml`), documentation as source of truth, language-specific rules, lean code principles

**Usage:** Memorize core patterns → Configure project (Foundation Pass) → Speed execution with memory-cached patterns → Follow DDD passes

**Quick Start:** [Quick Start Guide](docs/QUICK-START.md)

## Agent Guideline Protocol

**Entry point** for Agent3D system. Clone `git@github.com:ningsuhen/agent3d.git` to `~/.agent3d`, use `~/.agent3d/AGENT-GUIDELINES.md` as main entry point, update with `cd ~/.agent3d && git pull`.

## DDD Passes

0. **Requirements** - Business objectives
1. **Foundation** - Project configuration
2. **Documentation** - Features/requirements
3. **Planning** - Implementation plans with checkpoints
4. **Implementation** - Features with basic tests
5. **Testing** - Comprehensive tests
6. **Refactoring** - Code cleanup
7. **Code Review** - PR reviews
8. **Synchronization** - Doc-code alignment
9. **Quality** - Documentation quality
10. **Prune** - Remove outdated content
11. **Reverse** - Detect reverse drift

**Full Pass** - All passes for comprehensive updates

## Documentation Structure

**Core:** [AGENT-GUIDELINES.md](AGENT-GUIDELINES.md), [docs/](docs/) (BUSINESS-OBJECTIVES, REQUIREMENTS, USER-STORIES, ACCEPTANCE-CRITERIA, HIGH-LEVEL-DESIGN, DDD-STATUS)

**Passes:** [passes/simplified/](passes/simplified/) (0-11: requirements→foundation→documentation→planning→implementation→testing→refactoring→code_review→synchronization→quality→prune→reverse, [full_pass.md](passes/simplified/full_pass.md))

**Supporting:** [docs/designs/](docs/designs/) (component specs), [docs/proposals/](docs/proposals/) (unimplemented features), [rules/](rules/) (language-specific), [templates/](templates/) (format specs)

**Advanced:** [docs/ADVANCED-FEATURES.md](docs/ADVANCED-FEATURES.md), [docs/CONFIGURATION-GUIDE.md](docs/CONFIGURATION-GUIDE.md), [docs/GITHUB-CLI-INTEGRATION.md](docs/GITHUB-CLI-INTEGRATION.md)

**Note:** Documentation-only project. No implementation files, libraries, or code to import.

## License & Contributing

[MIT License](LICENSE) - Contributions welcome via Pull Request.