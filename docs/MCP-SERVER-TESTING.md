# Agent3D MCP Server Testing

Comprehensive testing documentation for the Agent3D MCP server implementation.

## Test Overview

The Agent3D MCP server includes a comprehensive test suite with **20 test cases** covering:

- **MCP Protocol Compliance** (4 tests)
- **Search and Analysis Tools** (6 tests) 
- **Analysis Tools** (3 tests)
- **Error Handling** (4 tests)
- **Performance and Reliability** (3 tests)

## Test Structure

### Test Files
- **`tests/test_mcp_server.py`** - Main test suite with 20 comprehensive test cases
- **`test_mcp.sh`** - Test runner script with virtual environment activation

### Test Categories

#### 1. MCP Protocol Compliance (`TestMCPProtocol`)
- **TC-MCP-001**: Server initialization with proper JSON-RPC handshake
- **TC-MCP-002**: Tools list endpoint with all 7 tools
- **TC-MCP-003**: Invalid method handling with proper error codes
- **TC-MCP-004**: Malformed JSON handling with parse error responses

#### 2. Search Tools (`TestSearchTools`)
- **TC-MCP-005**: `search_files` tool with semantic file search
- **TC-MCP-006**: `get_vector_stats` tool with database statistics
- **TC-MCP-007**: `search_test_cases` tool with TC-* identifier discovery
- **TC-MCP-008**: `search_features` tool with FT-* identifier discovery
- **TC-MCP-009**: Unknown tool handling with method not found errors
- **TC-MCP-010**: Missing required arguments with execution errors

#### 3. Analysis Tools (`TestAnalysisTools`)
- **TC-MCP-011**: `analyze_drift` tool with comprehensive drift analysis
- **TC-MCP-012**: `validate_code_locations` tool with location validation
- **TC-MCP-013**: `find_feature_test_mapping` tool with relationship mapping

#### 4. Error Handling (`TestErrorHandling`)
- **TC-MCP-014**: Empty request handling with graceful degradation
- **TC-MCP-015**: Invalid JSON-RPC version handling
- **TC-MCP-016**: Missing method field with invalid request errors
- **TC-MCP-017**: Concurrent request handling with thread safety

#### 5. Performance (`TestPerformance`)
- **TC-MCP-018**: Response time validation (under 10 seconds)
- **TC-MCP-019**: Large query handling with timeout protection
- **TC-MCP-020**: Memory usage stability with repeated operations

## Test Execution

### Quick Test Run
```bash
# Run individual test
cd /path/to/agent3d
source venv/bin/activate
python3 -m unittest tests.test_mcp_server.TestMCPProtocol.test_initialize_request -v

# Run test category
python3 -m unittest tests.test_mcp_server.TestSearchTools -v

# Run all tests
python3 -m unittest tests.test_mcp_server -v
```

### Using Test Runner
```bash
# Run comprehensive test suite
./test_mcp.sh
```

### Test Results Format
```
test_initialize_request (tests.test_mcp_server.TestMCPProtocol)
TC-MCP-001: Test server initialization ... ok

----------------------------------------------------------------------
Ran 1 test in 2.669s

OK
```

## Test Validation

### JSON-RPC Compliance
Each test validates:
- ✅ **Protocol Version**: `"jsonrpc": "2.0"`
- ✅ **Request ID**: Proper ID echoing in responses
- ✅ **Result/Error Structure**: Mutually exclusive result or error fields
- ✅ **Error Codes**: Standard JSON-RPC error codes (-32601, -32603, etc.)

### Tool Response Validation
Each tool test validates:
- ✅ **Response Structure**: Proper MCP tool response format
- ✅ **Content Format**: JSON content in text field
- ✅ **Tool-Specific Fields**: Expected fields for each tool type
- ✅ **Data Integrity**: Reasonable values and data consistency

### Performance Validation
Performance tests validate:
- ✅ **Response Time**: Under 10 seconds for basic operations
- ✅ **Memory Stability**: Consistent results across multiple requests
- ✅ **Concurrent Handling**: Thread-safe operation with multiple requests
- ✅ **Large Query Handling**: Graceful handling of large inputs

## Test Coverage

### Protocol Coverage
- **Initialize**: ✅ Server handshake and capabilities
- **Tools List**: ✅ All 7 tools with proper schemas
- **Tools Call**: ✅ All tool execution paths
- **Error Handling**: ✅ All major error scenarios

### Tool Coverage
1. **search_files**: ✅ Semantic file search with type filtering
2. **search_test_cases**: ✅ TC-* identifier discovery
3. **search_features**: ✅ FT-* identifier discovery
4. **find_feature_test_mapping**: ✅ Feature-test relationship mapping
5. **analyze_drift**: ✅ Comprehensive drift analysis
6. **validate_code_locations**: ✅ Code location validation
7. **get_vector_stats**: ✅ Vector database statistics

### Edge Case Coverage
- ✅ **Empty Requests**: Graceful handling of empty input
- ✅ **Invalid JSON**: Parse error responses
- ✅ **Missing Fields**: Invalid request error handling
- ✅ **Large Queries**: Timeout and memory protection
- ✅ **Concurrent Access**: Thread safety validation

## Test Environment

### Requirements
- **Python 3.7+**: Test runner compatibility
- **Virtual Environment**: Isolated dependency management
- **MCP Script**: Executable `tools/mcp.sh` wrapper
- **Dependencies**: PyYAML (required), sentence-transformers (optional)

### Test Data
- **Project Files**: Uses actual Agent3D project files for realistic testing
- **Vector Database**: Tests with real repository indexing (~2,800 chunks)
- **Search Queries**: Realistic search terms and patterns
- **Performance Metrics**: Real-world response time measurements

## Continuous Integration

### Test Automation
```bash
#!/bin/bash
# CI test script
set -e

# Setup environment
source venv/bin/activate
chmod +x tools/mcp.sh

# Run tests
python3 -m unittest tests.test_mcp_server -v

# Verify critical functionality
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | ./tools/mcp.sh > /dev/null
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | ./tools/mcp.sh > /dev/null

echo "✅ MCP server tests passed"
```

### Quality Gates
- **All Tests Pass**: 20/20 test cases must pass
- **Response Time**: Basic operations under 10 seconds
- **Memory Stability**: Consistent results across multiple runs
- **Protocol Compliance**: Full JSON-RPC 2.0 compliance

## Test Maintenance

### Adding New Tests
1. **Extend Test Classes**: Add methods to appropriate test class
2. **Follow Naming**: Use `TC-MCP-XXX` format for test case IDs
3. **Validate Protocol**: Use `assertValidJSONRPC()` helper
4. **Test Error Cases**: Include both success and failure scenarios

### Test Data Updates
- **Vector Database**: Tests adapt to project file changes automatically
- **Search Results**: Tests validate structure, not specific content
- **Performance Baselines**: Adjust timeouts based on hardware capabilities

### Debugging Tests
```bash
# Run single test with verbose output
python3 -m unittest tests.test_mcp_server.TestMCPProtocol.test_initialize_request -v

# Debug MCP communication
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | ./tools/mcp.sh 2>&1

# Check test environment
python3 -c "import tests.test_mcp_server; print('Test imports OK')"
```

## Test Results Summary

### Current Status
- **✅ Protocol Tests**: 4/4 passing
- **✅ Search Tools**: 6/6 passing  
- **✅ Analysis Tools**: 3/3 passing
- **✅ Error Handling**: 4/4 passing
- **✅ Performance**: 3/3 passing

### Performance Metrics
- **Initialization**: ~2.7 seconds
- **Tools List**: ~1.9 seconds
- **Vector Stats**: ~2.9 seconds
- **Search Operations**: ~3-5 seconds
- **Analysis Operations**: ~10-60 seconds (depending on mode)

### Reliability
- **✅ Thread Safety**: Concurrent requests handled properly
- **✅ Memory Stability**: Consistent performance across multiple operations
- **✅ Error Recovery**: Graceful handling of invalid inputs
- **✅ Protocol Compliance**: Full JSON-RPC 2.0 specification adherence

The Agent3D MCP server demonstrates excellent test coverage, performance, and reliability for production use with AI assistants and MCP-compatible tools.
