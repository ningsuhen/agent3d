#!/usr/bin/env python3
"""
Agent3D Drift Scanner MCP Server

A Model Context Protocol (MCP) server that provides drift analysis capabilities
for Agent3D Documentation-Driven Development projects.

This server implements the MCP JSON-RPC protocol and provides a single tool
for comprehensive drift detection across multiple modes.

Features:
- Live code reloading (auto-restart on code changes)
- Fresh scan mode (no caching)
- Multi-mode drift detection
- Automatic server restart
- File watching for live reloading (requires 'watchdog' package)
- Support for merged FT-TC structure

Installation:
    pip install -r tools/requirements.txt

Dependencies:
- Required: pyyaml (for YAML processing)
- Optional: watchdog (for file watching and live reloading)

Author: Agent3D Framework
"""

import json
import sys
import os
import subprocess
import logging
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None

# Configure logging to stderr only (MCP protocol uses stdout for JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class DriftFileWatcher(FileSystemEventHandler if WATCHDOG_AVAILABLE else object):
    """File system event handler for drift scanner files"""

    def __init__(self, server):
        if WATCHDOG_AVAILABLE:
            super().__init__()
        self.server = server

    def on_modified(self, event):
        """Handle file modification events"""
        if not WATCHDOG_AVAILABLE:
            return

        if event.is_directory:
            return

        # Check if it's a relevant file (documentation, code, config)
        relevant_extensions = {'.md', '.py', '.yaml', '.yml', '.json', '.txt'}
        file_path = Path(event.src_path)

        if file_path.suffix.lower() in relevant_extensions:
            logger.info(f"📝 File change detected: {file_path.name}")
            self.server.invalidate_cache()

class CodeReloader:
    """Monitors MCP server code files for changes and triggers restart"""

    def __init__(self, server_file: Path):
        self.server_file = server_file
        self.drift_scanner_file = server_file.parent / "drift_scanner.py"
        self.last_mtime = {}
        self.running = False
        self.check_interval = 1.0  # Check every second

        # Initialize modification times
        self._update_mtimes()

    def _update_mtimes(self):
        """Update stored modification times for watched files"""
        for file_path in [self.server_file, self.drift_scanner_file]:
            if file_path.exists():
                self.last_mtime[str(file_path)] = file_path.stat().st_mtime

    def _check_for_changes(self) -> bool:
        """Check if any watched files have been modified"""
        for file_path in [self.server_file, self.drift_scanner_file]:
            if file_path.exists():
                current_mtime = file_path.stat().st_mtime
                if str(file_path) in self.last_mtime:
                    if current_mtime > self.last_mtime[str(file_path)]:
                        logger.info(f"� Code change detected in: {file_path.name}")
                        return True
        return False

    def start_monitoring(self):
        """Start monitoring for code changes in a separate thread"""
        self.running = True

        def monitor_loop():
            while self.running:
                try:
                    if self._check_for_changes():
                        logger.info("� Restarting MCP server due to code changes...")
                        # Restart the server process
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    time.sleep(self.check_interval)
                except Exception as e:
                    logger.error(f"Error in code monitoring: {e}")
                    time.sleep(self.check_interval)

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("🔄 Live code reloading enabled - server will restart on code changes")

    def stop_monitoring(self):
        """Stop monitoring for code changes"""
        self.running = False

class DriftScannerMCPServer:
    """MCP Server for Agent3D Drift Scanner with Live Reloading"""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.agent3d_dir = self.script_dir.parent
        self.drift_scanner = self.script_dir / "drift_scanner.py"

        # Check if MCP server is disabled in configuration
        self._check_mcp_configuration()

        # Live reloading components
        if WATCHDOG_AVAILABLE:
            self.file_watcher = DriftFileWatcher(self)
            self.observer = None
            self.cache_invalidated = False
            self.watched_directories = set()
        else:
            self.file_watcher = None
            self.observer = None
            self.cache_invalidated = True  # Always invalidated if no watching
            self.watched_directories = set()

        logger.info("Agent3D Drift Scanner MCP Server initialized")
        logger.info("🔄 FRESH SCAN MODE: Every request performs a fresh drift analysis (no caching)")
        if WATCHDOG_AVAILABLE:
            logger.info("👁️  LIVE RELOADING: File watching enabled for automatic change detection")
        else:
            logger.warning("⚠️  WATCHDOG NOT AVAILABLE: File watching disabled (install 'watchdog' package for live reloading)")

    def _check_mcp_configuration(self):
        """Check if MCP server is disabled in configuration"""
        try:
            import yaml
            config_file = self.agent3d_dir / '.agent3d-config.yml'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)

                mcp_config = config.get('mcp_server', {})
                if not mcp_config.get('enabled', True):  # Default to True if not specified
                    logger.warning("⚠️  MCP SERVER DISABLED: Configuration shows mcp_server.enabled = false")
                    logger.warning(f"   Reason: {mcp_config.get('reason', 'Not specified')}")
                    logger.warning(f"   Alternative: {mcp_config.get('alternative', 'Use standalone drift scanner')}")
                    logger.warning("   To enable: Set mcp_server.enabled = true in .agent3d-config.yml")
        except Exception as e:
            logger.debug(f"Could not check MCP configuration: {e}")

    def find_ddd_root(self, explicit_root: Optional[str] = None) -> Optional[str]:
        """
        Find DDD project root with priority:
        1. Explicit parameter
        2. DDD_ROOT environment variable
        3. Auto-detection from current directory
        """
        if explicit_root:
            logger.info(f"Using DDD root from explicit parameter: {explicit_root}")
            return explicit_root

        if ddd_root_env := os.environ.get('DDD_ROOT'):
            logger.info(f"Using DDD root from DDD_ROOT environment variable: {ddd_root_env}")
            return ddd_root_env

        # Auto-detection: look for .agent3d-config.yaml
        current = Path.cwd()
        while current != current.parent:
            if (current / '.agent3d-config.yaml').exists():
                logger.info(f"Auto-detected DDD root: {current}")
                return str(current)
            current = current.parent

        logger.warning("No DDD root found - no .agent3d-config.yaml file located")
        return None

    def start_file_watching(self, ddd_root: str) -> None:
        """Start file watching for the DDD project directory"""
        if not WATCHDOG_AVAILABLE:
            logger.warning("⚠️  File watching not available - watchdog package not installed")
            return

        try:
            if self.observer is not None:
                self.stop_file_watching()

            self.observer = Observer()
            ddd_path = Path(ddd_root)

            # Watch the main project directory
            self.observer.schedule(self.file_watcher, str(ddd_path), recursive=True)
            self.watched_directories.add(str(ddd_path))

            self.observer.start()
            logger.info(f"👁️  Started file watching for: {ddd_path}")

        except Exception as e:
            logger.error(f"Failed to start file watching: {e}")

    def stop_file_watching(self) -> None:
        """Stop file watching"""
        if not WATCHDOG_AVAILABLE:
            return

        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watched_directories.clear()
            logger.info("👁️  Stopped file watching")

    def invalidate_cache(self) -> None:
        """Mark cache as invalidated due to file changes"""
        self.cache_invalidated = True
        logger.info("🔄 Cache invalidated due to file changes")

    def is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        return not self.cache_invalidated

    def reset_cache_status(self) -> None:
        """Reset cache invalidation status after fresh scan"""
        self.cache_invalidated = False

    def execute_drift_scanner(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the drift scanner with given arguments - ALWAYS performs fresh scan"""
        try:
            # Build command arguments for the original drift scanner
            cmd_args = [sys.executable, str(self.drift_scanner)]

            # Determine DDD root and change to that directory
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found. Ensure .agent3d-config.yaml exists or set DDD_ROOT environment variable.")

            # Add mode
            mode = args.get('mode', 'tc-mapping')
            cmd_args.extend(["--mode", mode])

            # Use consistent output file naming in .agent3d-tmp directory
            consistent_output = f".agent3d-tmp/drift-reports/{mode}-drift-report.yaml"

            # Add optional arguments
            if test_cases_file := args.get('test_cases_file'):
                cmd_args.extend(["--test-cases-file", test_cases_file])

            # Always use .agent3d-tmp directory, even for custom output paths
            if output := args.get('output'):
                # Ensure custom output is also in .agent3d-tmp directory
                if not output.startswith('.agent3d-tmp/'):
                    output = f".agent3d-tmp/drift-reports/{output}"
                cmd_args.extend(["--output", output])
            else:
                cmd_args.extend(["--output", consistent_output])

            # Add quiet flag if requested
            if args.get('quiet', False):
                cmd_args.append("--quiet")

            logger.info(f"🔄 Executing drift scanner in {ddd_root}: {' '.join(cmd_args)}")
            logger.info(f"📄 Output file: {consistent_output}")

            # Execute the command in the DDD root directory
            result = subprocess.run(
                cmd_args,
                cwd=ddd_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            logger.info(f"Drift scanner completed with return code: {result.returncode}")

            # Drift scanner exit codes: 0=low drift, 1=moderate drift, 2=high drift
            # All are successful executions, just different drift levels
            if result.returncode in [0, 1, 2]:
                # Determine drift level for reporting
                drift_level = "low" if result.returncode == 0 else "moderate" if result.returncode == 1 else "high"

                # Add drift level information to the output
                output_text = result.stdout
                if result.returncode > 0:
                    output_text += f"\n\n🎯 DRIFT LEVEL: {drift_level.upper()} (exit code {result.returncode})"

                # Report generated successfully - no cleanup needed

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": output_text
                        }
                    ]
                }
            else:
                # Only treat non-drift exit codes as errors (e.g., 1 for actual failures)
                error_msg = result.stderr or result.stdout or f"Drift scanner failed with exit code {result.returncode}"
                logger.error(f"Drift scanner execution error: {error_msg}")
                raise Exception(f"Drift scanner execution error: {error_msg}")

        except subprocess.TimeoutExpired:
            raise Exception("Drift scanner execution timed out (5 minutes)")
        except Exception as e:
            logger.error(f"Error executing drift scanner: {e}")
            raise



    def handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Handle tools/list request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "drift_scanner",
                        "description": "Agent3D Drift Scanner - Multi-mode drift detection with TC mapping, FT mapping, FT-TC relationships, code coverage, test quality validation, and feature implementation analysis. ALWAYS performs fresh scan on every request with consistent report file naming. All outputs are placed in .agent3d-tmp/ directory following DDD standards.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "ddd_root": {
                                    "type": "string",
                                    "description": "Path to DDD project root (uses DDD_ROOT env var if not specified, then auto-detection)"
                                },
                                "mode": {
                                    "type": "string",
                                    "enum": ["tc-mapping", "ft-mapping", "ft-tc-mapping", "code-coverage", "feature-impl", "test-quality", "all"],
                                    "default": "tc-mapping",
                                    "description": "Drift analysis mode"
                                },
                                "test_cases_file": {
                                    "type": "string",
                                    "description": "Custom path to TEST-CASES.md file"
                                },
                                "output": {
                                    "type": "string",
                                    "description": "Custom output file path"
                                },
                                "quiet": {
                                    "type": "boolean",
                                    "default": False,
                                    "description": "Suppress detailed output"
                                }
                            }
                        }
                    }
                ]
            }
        }

    def handle_tools_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})

        if tool_name == "drift_scanner":
            try:
                result = self.execute_drift_scanner(arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            except Exception as e:
                logger.error(f"Drift scanner execution failed: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": "Drift scanner execution failed",
                        "data": str(e)
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }

    def handle_initialize(self, request_id: Any) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "agent3d-drift-scanner",
                    "version": "1.1.0"
                }
            }
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        method = request.get('method')
        request_id = request.get('id')
        params = request.get('params', {})

        logger.info(f"Handling request: {method}")
        if method == "tools/call":
            logger.info(f"Tool call params: {params}")

        if method == "initialize":
            return self.handle_initialize(request_id)
        elif method == "tools/list":
            return self.handle_tools_list(request_id)
        elif method == "tools/call":
            return self.handle_tools_call(request_id, params)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def run(self):
        """Main server loop"""
        logger.info("MCP Server ready, waiting for requests...")
        logger.info("🔄 Fresh scan mode enabled - no stale data, every request triggers new analysis")
        logger.info("📄 Consistent file naming - reports overwrite previous versions automatically")

        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                try:
                    request = json.loads(line)
                    response = self.handle_request(request)

                    # Send response to stdout (MCP protocol)
                    print(json.dumps(response), flush=True)

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON request: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)

                except Exception as e:
                    logger.error(f"Error handling request: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32603,
                            "message": "Internal error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)

        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        print("ERROR: MCP server should not be called with command-line arguments", file=sys.stderr)
        print("Usage: echo '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\"}' | python3 drift_scanner_mcp_server.py", file=sys.stderr)
        print("This is an MCP server that communicates via JSON-RPC over stdin/stdout", file=sys.stderr)
        sys.exit(1)

    server = DriftScannerMCPServer()
    server.run()

if __name__ == "__main__":
    main()
