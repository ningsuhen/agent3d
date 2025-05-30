# Vector Database Integration for Drift MCP

This document describes the integration of vector database capabilities into the Agent3D Drift Scanner MCP server for enhanced file discovery and analysis.

## Overview

The vector database integration enhances the Drift MCP with intelligent file discovery capabilities, replacing traditional file system scanning with semantic search. This allows for more accurate and context-aware drift analysis.

## Features

### 1. Multi-Root Vector Database Management
- **Multiple DDD_ROOT Support**: Each DDD_ROOT directory gets its own vector database instance
- **Automatic Caching**: Vector databases are cached and reused across requests
- **Cache Invalidation**: Automatic cache invalidation when files change
- **Performance Tracking**: Detailed performance metrics for indexing and search operations

### 2. Enhanced File Discovery
- **Semantic Search**: Find files based on content similarity rather than just file patterns
- **Language Filtering**: Filter results by programming language (Python, JavaScript, etc.)
- **Chunk Type Filtering**: Filter by code structure (functions, classes, tests, documentation)
- **Relevance Scoring**: Results ranked by semantic similarity

### 3. Intelligent Drift Analysis
- **Context-Aware Scanning**: Use vector search to find related test files and implementations
- **Feature-Test Mapping**: Automatically discover relationships between features and tests
- **Code Location Analysis**: Enhanced validation of Code Location fields using semantic search

## Architecture

### Components

1. **MultiRootVectorDBManager** (`tools/vector_db_manager.py`)
   - Manages multiple vector databases for different DDD_ROOT directories
   - Handles caching, persistence, and cache invalidation
   - Provides search and statistics APIs

2. **Enhanced Drift Scanner** (`tools/drift_scanner.py`)
   - Integrates vector database capabilities into existing drift analysis
   - Provides new search methods for finding related files
   - Maintains backward compatibility with traditional file scanning

3. **Enhanced MCP Server** (`tools/drift_scanner_mcp_server.py`)
   - Initializes vector databases for each DDD_ROOT
   - Handles cache invalidation on file changes
   - Provides vector database statistics and management

### Dependencies

The vector database integration requires optional dependencies:

```bash
pip install sentence-transformers faiss-cpu numpy
```

If these dependencies are not available, the system gracefully falls back to traditional file scanning.

## Usage

### Command Line

Enable vector database in the drift scanner:

```bash
python3 tools/drift_scanner.py --enable-vector-db --mode all
```

### MCP Server

The MCP server automatically initializes vector databases when available:

```bash
python3 tools/drift_scanner_mcp_server.py
```

### Programmatic Usage

```python
from tools.drift_scanner import MultiModeDriftAnalyzer

# Initialize with vector database enabled
analyzer = MultiModeDriftAnalyzer(
    root_dir='/path/to/project',
    enable_vector_db=True
)

# Search for related files
results = analyzer.search_related_files("authentication test cases", top_k=5)

# Find test files for a feature
test_files = analyzer.find_related_test_files("user login functionality", top_k=3)

# Find implementation files
impl_files = analyzer.find_implementation_files("password validation", top_k=3)

# Get vector database statistics
stats = analyzer.get_vector_db_stats()
print(f"Indexed {stats['total_chunks']} chunks from {stats['total_files']} files")
```

## Configuration

### Cache Directory

Vector database cache is stored in `.agent3d-tmp/vector-cache/` by default. This can be customized:

```python
from tools.vector_db_manager import MultiRootVectorDBManager

manager = MultiRootVectorDBManager(cache_dir="/custom/cache/path")
```

### Exclusion Patterns

Files matching these patterns are excluded from indexing:
- `.git`, `__pycache__`, `.pytest_cache`, `node_modules`
- `.venv`, `venv`, `.env`, `.agent3d-tmp`, `.DS_Store`
- Binary files: `*.pyc`, `*.pyo`, `*.pyd`, `*.so`, `*.dll`, `*.dylib`

### Supported File Types

The vector database indexes these file types:
- **Code**: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.go`, `.rs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`
- **Documentation**: `.md`, `.rst`, `.txt`
- **Configuration**: `.yml`, `.yaml`, `.json`, `.xml`, `.html`, `.css`, `.scss`, `.sql`, `.sh`, `.bash`, `.zsh`

## Performance

### Indexing Performance
- **Initial Indexing**: ~1-5 seconds for typical Agent3D projects
- **Incremental Updates**: Automatic cache invalidation on file changes
- **Memory Usage**: ~10-50MB for typical projects

### Search Performance
- **Query Time**: <100ms for most searches
- **Accuracy**: High semantic similarity matching
- **Scalability**: Efficient for projects up to 10,000+ files

## Cache Management

### Automatic Cache Invalidation
- File changes detected via watchdog (if available)
- Content hash validation on database load
- Automatic reindexing when content changes

### Manual Cache Management
```python
# Invalidate cache for specific DDD_ROOT
manager.invalidate_cache("/path/to/project")

# Invalidate all caches
manager.invalidate_cache()

# Clean up old cache files (older than 1 week)
manager.cleanup_old_caches(max_age_hours=168)
```

## Troubleshooting

### Common Issues

1. **Dependencies Not Available**
   ```
   ⚠️  Vector database dependencies not available, using traditional file scanning
   ```
   **Solution**: Install dependencies with `pip install sentence-transformers faiss-cpu numpy`

2. **Indexing Fails**
   ```
   ❌ Failed to create vector database for /path/to/project: [error]
   ```
   **Solution**: Check file permissions and available disk space

3. **Search Returns No Results**
   ```
   ⚠️  No chunks indexed, skipping search tests
   ```
   **Solution**: Ensure the project directory contains supported file types

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Testing

Run the integration tests to verify everything works:

```bash
python3 tools/test_vector_integration.py
```

This will test:
- Vector database manager initialization
- Drift scanner integration
- MCP server integration
- Search functionality
- Cache management

## Future Enhancements

- **Incremental Indexing**: Update only changed files instead of full reindexing
- **Distributed Caching**: Share vector databases across team members
- **Custom Embeddings**: Fine-tuned embeddings for code-specific tasks
- **Advanced Filtering**: More sophisticated filtering options
- **Performance Optimization**: Further optimization for large codebases
