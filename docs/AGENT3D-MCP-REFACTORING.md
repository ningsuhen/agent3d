# Agent3D MCP-First Architecture Refactoring

## Overview

This document outlines the major architectural refactoring of Agent3D from direct file access to a **MCP-First Architecture** where all external agents communicate through the `agent3d-mcp` server instead of directly accessing `~/.agent3d` files.

## Architecture Diagrams

- **Main Architecture**: [agent3d-mcp-architecture.mmd](diagrams/agent3d-mcp-architecture.mmd)
- **Sequence Flow**: [agent3d-mcp-sequence.mmd](diagrams/agent3d-mcp-sequence.mmd)
- **Before/After Comparison**: [agent3d-architecture-comparison.mmd](diagrams/agent3d-architecture-comparison.mmd)

## Problems with Previous Architecture

### ❌ **Direct File Access Issues**

1. **Location Dependency**: Agents had to know about `~/.agent3d` location
2. **Hardcoded Paths**: Shell commands like `cat ~/.agent3d/templates/README.md`
3. **Inconsistent Access**: Different agents used different file access patterns
4. **No Semantic Search**: Only basic file system operations available
5. **Difficult Integration**: New agents needed to implement file access logic
6. **No Centralized Control**: No way to monitor or control framework access

### 📝 **Example of Old Pattern**

```bash
# Agents had to use direct shell commands
cat ~/.agent3d/templates/REQUIREMENTS.template.md
grep "python" ~/.agent3d/rules/python.md
ls ~/.agent3d/passes.yml/
```

## New MCP-First Architecture

### ✅ **Benefits**

1. **Location-Agnostic Agents**: No knowledge of `~/.agent3d` required
2. **Standardized API**: All access through JSON-RPC MCP protocol
3. **Semantic Search**: Vector database-powered intelligent search
4. **Centralized Access**: Single point of control for all framework operations
5. **Easy Integration**: Standard MCP tools for any agent
6. **Automatic Drift Detection**: Built-in analysis capabilities
7. **Consistent Interface**: Same tools for all agents

### 🔧 **MCP Tools Available**

#### **Framework Access Tools**
| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `get_template` | Get documentation templates | `get_template("REQUIREMENTS")` |
| `get_language_rules` | Get coding standards | `get_language_rules("python")` |
| `get_pass_definition` | Get DDD pass workflows | `get_pass_definition("development")` |
| `get_project_config` | Get project configuration | `get_project_config()` |

#### **Workflow Management Tools** 🆕
| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `next_action` | Get intelligent workflow guidance | `next_action()` |
| `save_exec_plan` | Save execution plans | `save_exec_plan("implement-auth", {...})` |
| `update_exec_plan` | Update execution progress | `update_exec_plan("implement-auth", status="completed")` |

#### **Search and Analysis Tools**
| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `search_files` | Semantic file search | `search_files("HTTP client implementation")` |
| `search_test_cases` | Find test cases (TC-*) | `search_test_cases("authentication")` |
| `search_features` | Find features (FT-*) | `search_features("user management")` |
| `find_feature_test_mapping` | Map features to tests | `find_feature_test_mapping()` |
| `analyze_drift` | Detect doc-code drift | `analyze_drift("all")` |
| `validate_code_locations` | Verify code paths | `validate_code_locations()` |
| `get_vector_stats` | Database statistics | `get_vector_stats()` |

## Agent Integration Examples

### 🤖 **LLM Coding Agent**

```python
# OLD WAY (Direct file access)
import subprocess
result = subprocess.run(["cat", "~/.agent3d/templates/README.template.md"],
                       capture_output=True, text=True)
template = result.stdout

# NEW WAY (MCP tools)
template_result = mcp_client.call_tool("get_template", {"template_name": "README"})
template = template_result["content"]
```

### 🚀 **Autonomous Agent Workflow** 🆕

```python
# Autonomous agent with intelligent workflow guidance
class AutonomousAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client

    def autonomous_work_session(self):
        while True:
            # Get intelligent guidance on what to do next
            guidance = self.mcp.call_tool("next_action")

            if guidance["action"] == "maintenance":
                break  # Project is in good state

            # Get project configuration
            config = self.mcp.call_tool("get_project_config")

            # Save execution plan for this action
            plan_name = f"execute-{guidance['action']}"
            self.mcp.call_tool("save_exec_plan", {
                "plan_name": plan_name,
                "plan_data": {
                    "action": guidance["action"],
                    "priority": guidance["priority"],
                    "next_steps": guidance["next_steps"],
                    "status": "started"
                }
            })

            # Execute the recommended action
            self.execute_action(guidance)

            # Update execution plan with completion
            self.mcp.call_tool("update_exec_plan", {
                "plan_name": plan_name,
                "update_status": "completed"
            })

    def execute_action(self, guidance):
        # Use suggested tools from guidance
        for tool in guidance.get("suggested_tools", []):
            if tool == "get_template":
                # Get appropriate template
                pass
            elif tool == "analyze_drift":
                # Run drift analysis
                pass
            # ... implement other actions
```

### 🔧 **VS Code Extension**

```typescript
// OLD WAY (File system API)
const templatePath = path.join(os.homedir(), '.agent3d', 'templates', 'README.template.md');
const template = fs.readFileSync(templatePath, 'utf8');

// NEW WAY (MCP JSON-RPC)
const template = await mcpClient.callTool('get_template', { template_name: 'README' });
```

### 🚀 **CI/CD Pipeline**

```yaml
# OLD WAY (Shell commands)
- name: Get Python rules
  run: cat ~/.agent3d/rules/python.md > python_rules.txt

# NEW WAY (MCP tools)
- name: Get Python rules
  run: echo '{"method":"tools/call","params":{"name":"get_language_rules","arguments":{"language":"python"}}}' | python3 agent3d_mcp_server.py
```

## Migration Guide

### 📋 **Step 1: Update Agent Guidelines**

Replace `AGENT-GUIDELINES.md` with `AGENT-GUIDELINES-MCP.md`:

- ❌ Remove: `cat ~/.agent3d/[filename]` instructions
- ✅ Add: MCP tool usage examples
- ✅ Add: JSON-RPC communication patterns

### 🔧 **Step 2: Update MCP Server**

Enhanced `agent3d_mcp_server.py` with new tools:

- ✅ `get_template()` - Template access
- ✅ `get_language_rules()` - Language standards
- ✅ `get_pass_definition()` - DDD pass workflows
- ✅ `get_project_config()` - Project configuration

### 🤖 **Step 3: Update Agents**

For each external agent:

1. **Remove direct file system access**
2. **Implement MCP client communication**
3. **Replace shell commands with MCP tool calls**
4. **Update documentation and examples**

### 📚 **Step 4: Update Documentation**

- ✅ New agent guidelines (MCP-first)
- ✅ Architecture diagrams
- ✅ Integration examples
- ✅ Migration instructions

## Communication Protocol

### 📡 **JSON-RPC over stdin/stdout**

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_template",
    "arguments": {
      "template_name": "REQUIREMENTS"
    }
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"template_name\": \"REQUIREMENTS\", \"content\": \"...\", \"found\": true}"
      }
    ]
  }
}
```

## Implementation Status

### ✅ **Completed**

- [x] New MCP-first agent guidelines
- [x] Enhanced MCP server with framework access tools
- [x] Architecture diagrams and documentation
- [x] Migration guide and examples

### 🔄 **In Progress**

- [ ] Update existing agents to use MCP tools
- [ ] Remove direct file access from codebase
- [ ] Update VS Code extension integration
- [ ] Update CI/CD pipeline examples

### 📋 **Next Steps**

1. **Test MCP server** with new tools
2. **Update orchestrator** to use MCP for framework access
3. **Migrate VS Code extension** to MCP communication
4. **Update all documentation** to reflect MCP-first approach
5. **Remove legacy file access patterns**

## Benefits Realized

### 🎯 **For Agents**

- **Simplified Integration**: Standard MCP protocol
- **No Path Dependencies**: Location-agnostic operation
- **Rich Capabilities**: Semantic search and drift analysis
- **Consistent Interface**: Same tools across all agents

### 🏗️ **For Framework**

- **Centralized Control**: Single access point
- **Better Monitoring**: Track all framework usage
- **Enhanced Security**: Controlled access patterns
- **Easier Maintenance**: Update framework without breaking agents

### 🚀 **For Users**

- **Better Agent Ecosystem**: Easier to build and integrate agents
- **More Reliable**: Consistent behavior across tools
- **Enhanced Features**: Semantic search and analysis
- **Future-Proof**: Extensible architecture

## Conclusion

The MCP-First Architecture refactoring transforms Agent3D from a file-based system to a modern, API-driven framework that provides:

- **Better separation of concerns**
- **Easier agent development**
- **Enhanced capabilities through semantic search**
- **Consistent, reliable access patterns**
- **Future-ready extensible design**

This architecture positions Agent3D as a robust, scalable platform for LLM-powered development tools.
