# Agent3D Tools

This directory contains tools for the Agent3D Documentation-Driven Development framework.

## Drift Scanner

The drift scanner analyzes documentation drift, feature-test relationships, and code quality.

### Standalone Usage

```bash
# Basic drift analysis
python3 tools/drift_scanner.py

# Specific analysis modes
python3 tools/drift_scanner.py --mode ft-mapping
python3 tools/drift_scanner.py --mode tc-drift
python3 tools/drift_scanner.py --mode code-coverage

# Output to specific file
python3 tools/drift_scanner.py --output my-report.yaml

# Quiet mode (minimal output)
python3 tools/drift_scanner.py --quiet
```

### MCP Server Usage

**⚠️ DISABLED BY DEFAULT:** The MCP server is disabled in the current configuration (`.agent3d-config.yml: mcp_server.enabled = false`).

The MCP server provides drift analysis capabilities to AI assistants through the Model Context Protocol, but is currently disabled per user preference.

#### Installation

```bash
# Install required dependencies
pip install -r tools/requirements.txt

# Or install minimal dependencies
pip install pyyaml

# Optional: Install watchdog for file watching
pip install watchdog
```

#### Running the MCP Server

```bash
# Start the MCP server
python3 tools/drift_scanner_mcp_server.py
```

The server communicates via JSON-RPC over stdin/stdout and provides:
- Real-time drift analysis
- Multiple scanning modes
- Fresh scan mode (no caching)
- File watching (if watchdog is installed)
- Support for merged FT-TC structure

#### Dependencies

**Required:**
- `pyyaml` - For YAML configuration and report processing

**Optional:**
- `watchdog` - For file watching and live reloading in MCP server

If optional dependencies are missing, the server will continue to function with reduced capabilities and show appropriate warnings.

## Features

### Supported Analysis Modes

- **ft-mapping** - Feature mapping analysis (NEW: supports merged FT-TC structure)
- **tc-drift** - Test case drift detection
- **ft-tc-mapping** - Feature-test case relationship analysis
- **code-coverage** - Code coverage analysis
- **feature-impl** - Feature implementation analysis
- **test-quality** - Test quality validation
- **all** - Comprehensive analysis (all modes)

### Merged FT-TC Structure Support

The tools now support the new merged FT-TC structure where features and test cases are documented together in `docs/features/` directory files, while maintaining backward compatibility with legacy `FEATURES.md` and `TEST-CASES.md` files.

### Output Formats

- YAML reports with detailed analysis
- Structured data for programmatic processing
- Human-readable summaries
- Integration with Agent3D documentation framework

## Troubleshooting

### Missing Dependencies

If you see warnings about missing packages:

```bash
# Install all dependencies
pip install -r tools/requirements.txt

# Or install specific packages
pip install watchdog  # For file watching
pip install pyyaml    # For YAML processing
```

### MCP Server Issues

If the MCP server doesn't start:

1. Check that you're using Python 3.7+
2. Ensure required dependencies are installed
3. Verify the server is being called correctly (no command-line arguments)
4. Check stderr for error messages

### File Watching Not Working

If file watching is disabled:

1. Install the watchdog package: `pip install watchdog`
2. Restart the MCP server
3. Check that the server shows file watching enabled in the logs

## Development

### Adding New Analysis Modes

1. Add the mode to `drift_scanner.py`
2. Update the MCP server tool definitions
3. Add documentation and tests
4. Update this README

### Testing

```bash
# Test drift scanner
python3 tools/drift_scanner.py --mode all --output test-report.yaml

# Test MCP server initialization
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python3 tools/drift_scanner_mcp_server.py
```
