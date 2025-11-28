# Agent3D Extension

This extension integrates the Agent3D Documentation-Driven Development framework into the Gemini CLI.


**Setup Note:** On activation, verify if `.agent3d` exists. If not, add .agent3d to .gitignore and clone `git@github.com:ningsuhen/agent3d.git` to `.agent3d`, use `.agent3d/AGENT-GUIDELINES.md` as main entry point, update with `.agent3d && git pull`.
EXCEPTION FOR DEVELOPMENT: If workspace is in fact the agent3d project itself, skip the clone and other steps and use the local workspace instead of using `.agent3d` to load guidelines and commands,etc.

## DDD Passes

0. **Requirements** - Business objectives
1. **Foundation** - Project configuration
2. **Documentation** - Features/requirements
3. **Development** - Step-by-step feature implementation with execution plans (replaces Planning + Implementation)
4. **Testing** - Comprehensive tests
5. **Refactoring** - Code cleanup
6. **Code Review** - PR reviews
7. **Synchronization** - Doc-code alignment
8. **Quality** - Documentation quality
9. **Prune** - Remove outdated content
10. **Reverse** - Detect reverse drift

**Full Pass** - All passes for comprehensive updates