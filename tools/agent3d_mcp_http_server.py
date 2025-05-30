#!/usr/bin/env python3
"""
Agent3D MCP HTTP Server

A persistent HTTP-based Model Context Protocol server that provides intelligent search,
analysis, and drift detection capabilities for Agent3D Documentation-Driven Development projects.

This server runs as a persistent HTTP service, maintaining vector database state
and providing fast response times for repeated queries.

Features:
- Persistent vector database with model caching
- HTTP REST API for MCP protocol
- Fast search and analysis capabilities
- Live reloading and file watching
- Multi-root project support

Usage:
    python3 agent3d_mcp_http_server.py [--port 8080] [--host localhost]

Author: Agent3D Framework
"""

import json
import sys
import os
import logging
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import argparse

# File watching for live reloading (optional dependency)
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None

# Vector database manager for enhanced file discovery
try:
    from vector_db_manager import MultiRootVectorDBManager
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    MultiRootVectorDBManager = None

# Drift scanner for analysis
try:
    from drift_scanner import MultiModeDriftAnalyzer
    DRIFT_SCANNER_AVAILABLE = True
except ImportError:
    DRIFT_SCANNER_AVAILABLE = False
    MultiModeDriftAnalyzer = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class Agent3DMCPHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Agent3D MCP server."""

    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            self._send_json_response({"status": "healthy", "server": "agent3d-mcp"})
        elif parsed_path.path == '/tools':
            self._handle_tools_list()
        else:
            self._send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/tools/call':
            self._handle_tools_call()
        elif parsed_path.path == '/rpc':
            self._handle_jsonrpc()
        else:
            self._send_error(404, "Not Found")

    def _handle_tools_list(self):
        """Handle tools list request."""
        response = self.server.mcp_server.handle_tools_list(1)
        self._send_json_response(response.get('result', {}))

    def _handle_tools_call(self):
        """Handle tools call request."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            response = self.server.mcp_server.handle_tools_call(1, request_data)

            if 'error' in response:
                self._send_error(500, response['error']['message'])
            else:
                result = response.get('result', {})
                content = result.get('content', [])
                if content and len(content) > 0:
                    # Extract the actual result from MCP format
                    text_content = content[0].get('text', '{}')
                    actual_result = json.loads(text_content)
                    self._send_json_response(actual_result)
                else:
                    self._send_json_response(result)

        except Exception as e:
            logger.error(f"Error handling tools call: {e}")
            self._send_error(500, str(e))

    def _handle_jsonrpc(self):
        """Handle JSON-RPC requests (compatible with stdin/stdout MCP)."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            response = self.server.mcp_server.handle_request(request_data)
            self._send_json_response(response)

        except Exception as e:
            logger.error(f"Error handling JSON-RPC: {e}")
            self._send_error(500, str(e))

    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """Send JSON response."""
        response_json = json.dumps(data, indent=2)

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_json)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        self.wfile.write(response_json.encode('utf-8'))

    def _send_error(self, status_code: int, message: str):
        """Send error response."""
        error_data = {
            "error": {
                "code": status_code,
                "message": message
            }
        }
        self._send_json_response(error_data, status_code)

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


class Agent3DMCPHTTPServer(HTTPServer):
    """HTTP server for Agent3D MCP."""

    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

        # Import the MCP server class
        from tools.agent3d_mcp_server import Agent3DMCPServer
        self.mcp_server = Agent3DMCPServer()

        logger.info(f"🚀 Agent3D MCP HTTP Server initialized")
        logger.info(f"📡 Server will listen on http://{server_address[0]}:{server_address[1]}")


def main():
    """Main entry point for agent3d-mcp-http command."""
    parser = argparse.ArgumentParser(
        description='Agent3D MCP HTTP Server - Persistent vector database and search capabilities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agent3d-mcp-http                    # Start on localhost:8080
  agent3d-mcp-http --port 9000        # Start on port 9000
  agent3d-mcp-http --host 0.0.0.0     # Listen on all interfaces
  agent3d-mcp-http --debug            # Enable debug logging

Endpoints:
  GET  /health      - Health check
  GET  /tools       - List available tools
  POST /tools/call  - Call a tool
  POST /rpc         - JSON-RPC endpoint
        """
    )
    parser.add_argument('--host', default='localhost',
                       help='Host to bind to (default: localhost)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port to bind to (default: 8080)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--ddd-root',
                       help='DDD project root directory (default: auto-detect)')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Set DDD_ROOT environment variable if provided
    if args.ddd_root:
        os.environ['DDD_ROOT'] = args.ddd_root
        logger.info(f"🎯 DDD_ROOT set to: {args.ddd_root}")

    try:
        server = Agent3DMCPHTTPServer((args.host, args.port), Agent3DMCPHTTPHandler)

        logger.info(f"🌐 Starting Agent3D MCP HTTP Server on http://{args.host}:{args.port}")
        logger.info("📋 Available endpoints:")
        logger.info("   GET  /health - Health check")
        logger.info("   GET  /tools - List available tools")
        logger.info("   POST /tools/call - Call a tool")
        logger.info("   POST /rpc - JSON-RPC endpoint")
        logger.info("🔧 Press Ctrl+C to stop the server")

        server.serve_forever()

    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        if 'server' in locals():
            server.server_close()
            logger.info("✅ Server stopped")


if __name__ == "__main__":
    main()
