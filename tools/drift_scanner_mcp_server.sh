#!/bin/bash
#
# MCP Server Shell Wrapper for Agent3D Drift Scanner
#
# This shell script only handles virtual environment activation and then
# delegates to the Python MCP server implementation.
#
# Usage:
# - Called by MCP clients as a server
# - Automatically activates virtual environment if available
# - Delegates all MCP protocol handling to Python
#
# Author: Agent3D Framework
#

# Set strict error handling
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT3D_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$AGENT3D_DIR/venv"
PYTHON_MCP_SERVER="$SCRIPT_DIR/drift_scanner_mcp_server.py"

# Logging function - log to stderr to avoid breaking MCP JSON-RPC protocol
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Check if virtual environment exists and activate it
activate_venv() {
    if [[ -d "$VENV_PATH" ]]; then
        log "Activating virtual environment: $VENV_PATH"
        source "$VENV_PATH/bin/activate"
        log "Virtual environment activated"
    else
        log "No virtual environment found at $VENV_PATH, using system Python"
    fi
}

# Check dependencies
check_dependencies() {
    if ! python3 -c "import yaml" 2>/dev/null; then
        log "WARNING: PyYAML not available. Installing..."
        pip3 install pyyaml
    fi
    log "Dependencies verified"
}

# Main function
main() {
    # Check if called with command line arguments (incorrect usage)
    if [[ $# -gt 0 ]]; then
        echo "ERROR: MCP server should not be called with command-line arguments" >&2
        echo "Usage: echo '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\"}' | $0" >&2
        echo "This is an MCP server that communicates via JSON-RPC over stdin/stdout" >&2
        exit 1
    fi
    
    log "Starting Agent3D Drift Scanner MCP Server (Shell Wrapper)"
    
    # Activate virtual environment
    activate_venv
    
    # Check dependencies
    check_dependencies
    
    # Delegate to Python MCP server
    log "Delegating to Python MCP server: $PYTHON_MCP_SERVER"
    exec python3 "$PYTHON_MCP_SERVER"
}

# Run main function
main "$@"
