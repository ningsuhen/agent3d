#!/usr/bin/env python3
"""
Agent3D MCP Router

A router that bridges stdin/stdout MCP protocol to the HTTP-based MCP server.
This allows MCP clients to communicate with the persistent HTTP server through
the standard stdin/stdout interface.

Features:
- Transparent routing between stdin/stdout and HTTP server
- Automatic HTTP server startup if not running
- Error handling and fallback mechanisms
- JSON-RPC protocol compliance

Usage:
    echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | python3 agent3d_mcp_router.py

Author: Agent3D Framework
"""

import json
import sys
import os
import logging
import time
import subprocess
import signal
import threading
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from urllib.parse import urljoin

# Setup logging to stderr (to avoid interfering with stdout)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class Agent3DMCPRouter:
    """Router that bridges stdin/stdout to HTTP MCP server."""

    def __init__(self, http_host: str = "localhost", http_port: int = 8080, persistent_server: bool = True):
        self.http_host = http_host
        self.http_port = http_port
        self.base_url = f"http://{http_host}:{http_port}"
        self.http_server_process = None
        self.script_dir = Path(__file__).parent
        self.agent3d_dir = self.script_dir.parent
        self.persistent_server = persistent_server  # If True, leave server running when router exits
        self.started_server = False  # Track if we started the server

    def is_server_running(self) -> bool:
        """Check if the HTTP server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def start_http_server(self) -> bool:
        """Start the HTTP server if it's not running."""
        if self.is_server_running():
            logger.info(f"✅ HTTP server already running at {self.base_url}")
            return True

        logger.info(f"🚀 Starting HTTP server at {self.base_url}")
        self.started_server = True  # Mark that we started the server

        try:
            # Start the HTTP server as a background process
            server_script = self.script_dir / "agent3d_mcp_http_server.py"

            # Check if server script exists
            if not server_script.exists():
                logger.error(f"HTTP server script not found: {server_script}")
                return False

            # Activate virtual environment if available
            venv_path = self.agent3d_dir / "venv"
            if venv_path.exists():
                python_path = venv_path / "bin" / "python3"
                if not python_path.exists():
                    logger.error(f"Python executable not found in venv: {python_path}")
                    return False
            else:
                python_path = "python3"

            cmd = [
                str(python_path),
                str(server_script),
                "--host", self.http_host,
                "--port", str(self.http_port)
            ]

            # Set DDD_ROOT environment variable
            env = os.environ.copy()
            env['DDD_ROOT'] = str(self.agent3d_dir)

            logger.info(f"Starting HTTP server with command: {' '.join(cmd)}")
            logger.info(f"Working directory: {self.agent3d_dir}")
            logger.info(f"DDD_ROOT: {env.get('DDD_ROOT')}")

            self.http_server_process = subprocess.Popen(
                cmd,
                cwd=self.agent3d_dir,
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new process group
            )

            # Wait for server to start
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.is_server_running():
                    logger.info(f"✅ HTTP server started successfully")
                    return True
                if self.http_server_process.poll() is not None:
                    # Process died
                    stderr = self.http_server_process.stderr.read().decode()
                    logger.error(f"HTTP server failed to start: {stderr}")
                    logger.error(f"HTTP server exit code: {self.http_server_process.returncode}")
                    logger.error(f"HTTP server command: {cmd}")
                    return False

            logger.error("HTTP server failed to start within timeout")
            return False

        except Exception as e:
            logger.error(f"Failed to start HTTP server: {e}")
            return False

    def stop_http_server(self):
        """Stop the HTTP server if we started it and persistent mode is disabled."""
        if self.persistent_server and self.started_server:
            logger.info("🔄 Leaving HTTP server running (persistent mode)")
            return

        if self.http_server_process:
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(self.http_server_process.pid), signal.SIGTERM)
                self.http_server_process.wait(timeout=5)
                logger.info("🛑 HTTP server stopped")
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't stop gracefully
                os.killpg(os.getpgid(self.http_server_process.pid), signal.SIGKILL)
                logger.warning("🔥 HTTP server force killed")
            except Exception as e:
                logger.warning(f"Error stopping HTTP server: {e}")

    def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route a JSON-RPC request to the HTTP server."""
        try:
            response = requests.post(
                f"{self.base_url}/rpc",
                json=request,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": f"HTTP server error: {response.status_code}"
                    }
                }

        except requests.exceptions.Timeout:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Request timeout"
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Router error: {str(e)}"
                }
            }

    def run(self):
        """Main router loop - read from stdin, route to HTTP, write to stdout."""
        logger.info("🔄 Starting Agent3D MCP Router")

        # Start HTTP server if needed
        if not self.start_http_server():
            logger.error("Failed to start HTTP server, exiting")
            sys.exit(1)

        # Setup signal handlers for cleanup
        def signal_handler(_signum, _frame):
            logger.info("🛑 Router shutdown requested")
            self.stop_http_server()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            logger.info("📡 Router ready - listening on stdin")

            # Read JSON-RPC requests from stdin
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                try:
                    # Parse JSON-RPC request
                    request = json.loads(line)
                    logger.debug(f"📨 Routing request: {request.get('method', 'unknown')}")

                    # Route to HTTP server
                    response = self.route_request(request)

                    # Send response to stdout
                    print(json.dumps(response), flush=True)
                    logger.debug(f"📤 Response sent")

                except json.JSONDecodeError as e:
                    # Send parse error response
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    logger.error(f"JSON parse error: {e}")

                except Exception as e:
                    # Send internal error response
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    logger.error(f"Router error: {e}")

        except KeyboardInterrupt:
            logger.info("🛑 Router interrupted")
        except Exception as e:
            logger.error(f"Router fatal error: {e}")
        finally:
            self.stop_http_server()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        print("ERROR: Agent3D MCP router should not be called with command-line arguments", file=sys.stderr)
        print("Usage: echo '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\"}' | python3 agent3d_mcp_router.py", file=sys.stderr)
        print("This is an MCP router that communicates via JSON-RPC over stdin/stdout", file=sys.stderr)
        sys.exit(1)

    router = Agent3DMCPRouter()
    router.run()


if __name__ == "__main__":
    main()
