# Agent3D MCP Server

A comprehensive Model Context Protocol (MCP) server that provides intelligent search, analysis, and drift detection capabilities for Agent3D Documentation-Driven Development projects.

## Overview

The Agent3D MCP Server leverages vector database technology for semantic search and provides a rich set of tools for DDD workflow automation. It replaces the previous drift scanner MCP with enhanced capabilities and intelligent file discovery.

## Features

### 🔍 **Intelligent Search Capabilities**
- **Semantic File Search**: Find files based on content meaning, not just patterns
- **Test Case Discovery**: Search for TC-* identifiers in documentation and implementation
- **Feature Discovery**: Search for FT-* identifiers across the codebase
- **Feature-Test Mapping**: Intelligent mapping between features and test cases

### 🧠 **Vector-Enhanced Analysis**
- **Drift Analysis**: Comprehensive drift detection with semantic understanding
- **Code Location Validation**: Validate and suggest better code locations for features
- **Test Quality Assessment**: Evaluate test relevance using similarity scores
- **Coverage Analysis**: Find missing tests using semantic similarity

### 🚀 **Advanced Capabilities**
- **Multi-Root Support**: Handle multiple DDD projects simultaneously
- **Live File Watching**: Automatic cache invalidation on file changes
- **Performance Optimization**: Fast indexing and intelligent caching
- **Graceful Fallback**: Works without vector dependencies

## Installation

### Prerequisites

```bash
# Required dependencies
pip install pyyaml sentence-transformers faiss-cpu numpy

# Optional dependencies (for enhanced features)
pip install watchdog  # For file watching and live reloading
```

### Setup

```bash
# Install all dependencies
pip install -r tools/requirements.txt

# Test the server
python3 tools/test_agent3d_mcp.py
```

## Available Tools

### 1. **search_files**
Search for files using semantic search with various filters.

**Parameters:**
- `query` (required): Search query
- `file_type`: Filter by type (`any`, `python`, `test`, `doc`, `config`)
- `top_k`: Number of results (default: 10)
- `min_similarity`: Minimum similarity score (default: 0.3)
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "search_files",
  "arguments": {
    "query": "drift scanner test",
    "file_type": "python",
    "top_k": 5
  }
}
```

### 2. **search_test_cases**
Search for test cases with TC-* identifiers in both documentation and implementation.

**Parameters:**
- `query`: Search query for test cases
- `tc_id`: Specific TC-* identifier (without TC- prefix)
- `top_k`: Number of results (default: 10)
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "search_test_cases",
  "arguments": {
    "tc_id": "CORE-001",
    "top_k": 10
  }
}
```

### 3. **search_features**
Search for features with FT-* identifiers in documentation and implementation.

**Parameters:**
- `query`: Search query for features
- `ft_id`: Specific FT-* identifier (without FT- prefix)
- `top_k`: Number of results (default: 10)
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "search_features",
  "arguments": {
    "query": "vector database integration",
    "top_k": 5
  }
}
```

### 4. **find_feature_test_mapping**
Find mapping between features (FT-*) and test cases (TC-*) using semantic search.

**Parameters:**
- `feature_query`: Feature search query
- `ft_id`: Specific FT-* identifier (without FT- prefix)
- `top_k`: Number of results (default: 10)
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "find_feature_test_mapping",
  "arguments": {
    "ft_id": "IMPL-001",
    "top_k": 10
  }
}
```

### 5. **analyze_drift**
Perform comprehensive drift analysis with vector enhancement.

**Parameters:**
- `mode`: Analysis mode (`tc-mapping`, `ft-mapping`, `ft-tc-mapping`, `code-coverage`, `test-quality`, `code-location`, `all`)
- `quiet`: Suppress verbose output (default: false)
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "analyze_drift",
  "arguments": {
    "mode": "all",
    "quiet": false
  }
}
```

### 6. **validate_code_locations**
Validate and suggest code locations for features using vector search.

**Parameters:**
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "validate_code_locations",
  "arguments": {}
}
```

### 7. **get_vector_stats**
Get vector database statistics and indexing information.

**Parameters:**
- `ddd_root`: DDD project root (optional)

**Example:**
```json
{
  "name": "get_vector_stats",
  "arguments": {}
}
```

## Usage Examples

### Basic File Search
```bash
# Search for Python test files
echo '{"jsonrpc":"2.0","method":"tools/call","id":1,"params":{"name":"search_files","arguments":{"query":"test drift analysis","file_type":"test","top_k":5}}}' | python3 tools/agent3d_mcp_server.py
```

### Feature-Test Mapping
```bash
# Find tests related to a specific feature
echo '{"jsonrpc":"2.0","method":"tools/call","id":2,"params":{"name":"find_feature_test_mapping","arguments":{"ft_id":"IMPL-001"}}}' | python3 tools/agent3d_mcp_server.py
```

### Comprehensive Analysis
```bash
# Run full drift analysis
echo '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"analyze_drift","arguments":{"mode":"all"}}}' | python3 tools/agent3d_mcp_server.py
```

## Architecture

### Vector Database Integration
- **Multi-Root Manager**: Handles multiple DDD projects with separate vector databases
- **Intelligent Caching**: Content hash validation and automatic cache invalidation
- **Semantic Search**: Uses sentence-transformers for meaningful code relationships
- **Performance Optimization**: Fast indexing (~0.5-0.8s for typical projects)

### Search Capabilities
- **Language Filtering**: Filter results by programming language
- **Chunk Type Filtering**: Filter by code structure (functions, classes, tests)
- **Similarity Scoring**: Results ranked by semantic similarity
- **Content Preview**: Relevant code snippets in search results

### Analysis Features
- **Hybrid Analysis**: Combines traditional and vector-based approaches
- **Confidence Scoring**: Provides similarity scores for decision making
- **Multi-Modal Search**: Searches across documentation and implementation
- **Relationship Discovery**: Finds subtle connections traditional scanning misses

## Configuration

### MCP Server Configuration
The server can be disabled by setting the following in `.agent3d-config.yml`:

```yaml
mcp:
  disabled: true
```

### Vector Database Configuration
Vector database settings are automatically configured but can be customized through the drift scanner configuration.

## Performance

### Indexing Performance
- **Typical Project**: ~0.5-0.8 seconds for 2,694 chunks from 231 files
- **Memory Efficient**: Intelligent caching with content hash validation
- **Scalable**: Handles multiple DDD_ROOT directories efficiently

### Search Performance
- **Fast Semantic Search**: Sub-second response times for most queries
- **Configurable Similarity**: Adjustable thresholds for precision/recall balance
- **Result Limiting**: Configurable result counts to manage response size

## Error Handling

The server provides comprehensive error handling:
- **Graceful Degradation**: Falls back to traditional methods when vector DB unavailable
- **Detailed Error Messages**: Clear error descriptions for troubleshooting
- **Timeout Protection**: Request timeouts to prevent hanging
- **Resource Management**: Automatic cleanup and cache management

## Testing

Run the comprehensive test suite:

```bash
python3 tools/test_agent3d_mcp.py
```

The test suite covers:
- Server initialization
- Tool availability
- Search functionality
- Analysis capabilities
- Error handling
- Performance validation

## Migration from Previous MCP

The new Agent3D MCP server replaces `drift_scanner_mcp_server.py` with enhanced capabilities:

### Key Improvements
1. **Multiple Tools**: 7 specialized tools vs. 1 general tool
2. **Intelligent Search**: Semantic search vs. pattern matching
3. **Better Performance**: Vector database caching vs. fresh scans
4. **Enhanced Analysis**: Hybrid traditional + vector analysis
5. **Richer Results**: Detailed similarity scores and content previews

### Backward Compatibility
- All previous drift analysis functionality is preserved
- Enhanced with vector database capabilities
- Maintains MCP protocol compatibility
- Supports same configuration options

## Troubleshooting

### Common Issues

1. **Vector Database Not Available**
   - Install required dependencies: `pip install sentence-transformers faiss-cpu`
   - Server will fall back to traditional scanning

2. **File Watching Disabled**
   - Install watchdog: `pip install watchdog`
   - File watching provides automatic cache invalidation

3. **Slow Performance**
   - Check vector database indexing logs
   - Ensure sufficient memory for large projects
   - Consider adjusting similarity thresholds

4. **No Results Found**
   - Try broader search queries
   - Lower minimum similarity threshold
   - Check if vector database is properly indexed

### Debug Mode
Enable detailed logging by setting log level to DEBUG in the server code.

## Future Enhancements

- **GPU Acceleration**: FAISS GPU support for larger projects
- **Custom Models**: Support for domain-specific embedding models
- **Advanced Filtering**: More sophisticated search filters
- **Real-time Updates**: Live indexing of file changes
- **Integration APIs**: REST API endpoints for web interfaces
