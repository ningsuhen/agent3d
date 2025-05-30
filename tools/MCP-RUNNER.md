# Agent3D MCP Runner

Simple shell wrapper for the Agent3D MCP server that handles virtual environment activation and delegates to the Python MCP implementation.

## Usage

### As MCP Server
```bash
# Initialize MCP server
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | ./tools/mcp.sh

# List available tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | ./tools/mcp.sh

# Call a tool (example: get vector stats)
echo '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"get_vector_stats","arguments":{}}}' | ./tools/mcp.sh
```

### With AI Assistants
Configure your AI assistant to use `./tools/mcp.sh` as an MCP server. The script will:

1. ✅ Activate the virtual environment automatically
2. ✅ Check and install required dependencies
3. ✅ Delegate to the Python MCP server
4. ✅ Handle JSON-RPC communication over stdin/stdout

## Features

- **Automatic Environment Setup**: Activates venv if available
- **Dependency Management**: Checks and installs required packages
- **Clean Protocol**: Logs to stderr, JSON-RPC to stdout
- **Error Handling**: Proper error messages and exit codes
- **Zero Configuration**: Works out of the box

## Available Tools

The MCP server provides 7 intelligent tools:

1. **`search_files`** - Semantic file search with type filtering
2. **`search_test_cases`** - TC-* identifier discovery
3. **`search_features`** - FT-* identifier discovery  
4. **`find_feature_test_mapping`** - Feature-test relationship mapping
5. **`analyze_drift`** - Comprehensive drift analysis
6. **`validate_code_locations`** - Code location validation
7. **`get_vector_stats`** - Vector database statistics

## Requirements

- Python 3.7+
- Virtual environment at `../venv/` (optional but recommended)
- PyYAML (auto-installed if missing)

## Optional Dependencies

For enhanced functionality:
- `sentence-transformers` + `faiss-cpu` - Vector search capabilities
- `watchdog` - File watching and live reloading

## Logging

The wrapper logs to stderr with timestamps:
```
[2025-05-29 23:04:23] Starting Agent3D MCP Server (Shell Wrapper)
[2025-05-29 23:04:23] Activating virtual environment: /path/to/venv
[2025-05-29 23:04:23] Virtual environment activated
[2025-05-29 23:04:23] Dependencies verified
[2025-05-29 23:04:23] Delegating to Python MCP server: /path/to/agent3d_mcp_server.py
```

JSON-RPC responses go to stdout for proper MCP protocol compliance.

## Error Handling

- **Command Line Args**: Rejects command line arguments (MCP uses stdin/stdout)
- **Missing Dependencies**: Auto-installs PyYAML, warns about optional deps
- **Environment Issues**: Falls back to system Python if venv unavailable
- **Protocol Errors**: Proper JSON-RPC error responses

## Integration

Use with MCP-compatible AI assistants by configuring the server path:
```json
{
  "mcpServers": {
    "agent3d": {
      "command": "/path/to/agent3d/tools/mcp.sh"
    }
  }
}
```

The server will automatically handle environment setup and provide intelligent search and analysis capabilities for your DDD workflows.
