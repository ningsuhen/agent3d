#!/bin/bash
# Test runner for Agent3D MCP Server
#
# This script runs the comprehensive unit test suite for the MCP server
# with proper virtual environment activation.

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

echo -e "${PURPLE}🧪 Agent3D MCP Server Test Suite${NC}"
echo -e "${BLUE}====================================${NC}"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Virtual environment not found at $VENV_PATH${NC}"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r tools/requirements.txt"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Check activation
if [ "$VIRTUAL_ENV" != "$VENV_PATH" ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Change to project directory
cd "$SCRIPT_DIR"

# Check if MCP script exists
if [ ! -f "tools/mcp.sh" ]; then
    echo -e "${RED}❌ MCP script not found: tools/mcp.sh${NC}"
    exit 1
fi

# Make sure MCP script is executable
chmod +x tools/mcp.sh

echo -e "${BLUE}🔧 Running MCP Server Tests...${NC}"
echo

# Run the test suite
python3 -m pytest tests/test_mcp_server.py -v --tb=short

# Check test result
if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}✅ All MCP server tests passed!${NC}"
    echo -e "${BLUE}🎉 Agent3D MCP server is ready for use${NC}"
else
    echo
    echo -e "${RED}❌ Some tests failed. Check the output above for details.${NC}"
    exit 1
fi
