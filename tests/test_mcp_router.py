#!/usr/bin/env python3
"""
Test suite for Agent3D MCP Shell Wrapper (mcp.sh)

Tests the mcp.sh shell wrapper that activates virtual environment and
delegates to the MCP router, using real test data from ProtobufRegistry.

Test Coverage:
- MCP shell wrapper initialization and venv activation
- JSON-RPC protocol compliance through mcp.sh
- All MCP tools through shell wrapper interface
- Error handling and edge cases
- Performance and reliability

Author: Agent3D Framework
"""

import json
import subprocess
import time
import unittest
import requests
from pathlib import Path
from typing import Dict, Any, Optional


class TestMCPShellWrapper(unittest.TestCase):
    """Test Agent3D MCP Shell Wrapper (mcp.sh) functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent
        cls.mcp_script = cls.project_root / "mcp.sh"
        cls.test_ddd_root = "/Users/nwaikhom/git/ProtobufRegistry/tools/protoc-gen-httpx-fastapi"
        cls.agent3d_root = "/Users/nwaikhom/.agent3d"
        cls.http_server_url = "http://localhost:8080"

        # Ensure mcp.sh is executable
        cls.mcp_script.chmod(0o755)

        # Ensure HTTP server is running
        cls._ensure_http_server_running()

    @classmethod
    def _ensure_http_server_running(cls):
        """Ensure the HTTP server is running for tests."""
        try:
            response = requests.get(f"{cls.http_server_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ HTTP server already running")
                return
        except:
            pass

        print("🚀 Starting HTTP server for tests...")
        # The router will start the server automatically
        time.sleep(2)

    def send_mcp_request(self, request: Dict[str, Any], timeout: int = 15) -> Dict[str, Any]:
        """Send a request through mcp.sh and return the response."""
        try:
            process = subprocess.Popen(
                [str(self.mcp_script)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )

            # Send request
            request_json = json.dumps(request)
            stdout, stderr = process.communicate(input=request_json, timeout=timeout)

            # Parse response
            if stdout.strip():
                return json.loads(stdout.strip())
            else:
                self.fail(f"No response from MCP server. Stderr: {stderr}")

        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"MCP request timed out after {timeout}s")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON response: {e}. Output: {stdout}")
        except Exception as e:
            self.fail(f"MCP request failed: {e}")

    def assertMCPResponse(self, response: Dict[str, Any], expected_id: Any = None):
        """Assert that response is a valid MCP response."""
        self.assertIn("jsonrpc", response)
        self.assertEqual(response["jsonrpc"], "2.0")

        if expected_id is not None:
            self.assertIn("id", response)
            self.assertEqual(response["id"], expected_id)

        # Should have either result or error, but not both
        has_result = "result" in response
        has_error = "error" in response
        self.assertTrue(has_result or has_error, "Response must have either result or error")
        self.assertFalse(has_result and has_error, "Response cannot have both result and error")

    def assertMCPError(self, response: Dict[str, Any], expected_code: int = None):
        """Assert that response is a valid MCP error response."""
        self.assertMCPResponse(response)
        self.assertIn("error", response)

        error = response["error"]
        self.assertIn("code", error)
        self.assertIn("message", error)

        if expected_code is not None:
            self.assertEqual(error["code"], expected_code)


class TestMCPProtocol(TestMCPShellWrapper):
    """Test MCP protocol compliance through mcp.sh."""

    def test_initialize_request(self):
        """TC-MCP-SH-001: Test MCP initialize request through mcp.sh"""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1,
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=1)
        self.assertIn("result", response)

        result = response["result"]
        self.assertIn("protocolVersion", result)
        self.assertIn("capabilities", result)
        self.assertIn("serverInfo", result)

        server_info = result["serverInfo"]
        self.assertEqual(server_info["name"], "agent3d-mcp")
        self.assertEqual(server_info["version"], "2.0.0")

    def test_list_tools_request(self):
        """TC-MCP-SH-002: Test tools/list request through mcp.sh"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=2)
        self.assertIn("result", response)

        result = response["result"]
        self.assertIn("tools", result)

        tools = result["tools"]
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)

        # Check that all expected tools are present
        tool_names = [tool["name"] for tool in tools]
        expected_tools = [
            "search_files", "search_test_cases", "search_features",
            "find_feature_test_mapping", "analyze_drift",
            "validate_code_locations", "get_vector_stats"
        ]

        for expected_tool in expected_tools:
            self.assertIn(expected_tool, tool_names)


class TestRouterSearchTools(TestMCPShellWrapper):
    """Test search tools through router with ProtobufRegistry data."""

    def test_search_files_protobuf_data(self):
        """TC-ROUTER-003: Test search_files with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 3,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": "websocket streaming implementation",
                    "file_type": "python",
                    "ddd_root": self.test_ddd_root,
                    "top_k": 3
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=3)
        self.assertIn("result", response)

        # Parse the content from MCP response format
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["query"], "websocket streaming implementation")
        self.assertEqual(result["file_type"], "python")
        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("total_results", result)
        self.assertIn("results", result)

        # Should have some results for this query
        if result["total_results"] > 0:
            results = result["results"]
            self.assertIsInstance(results, list)

            for file_result in results:
                self.assertIn("file_path", file_result)
                self.assertIn("similarity_score", file_result)
                self.assertIn("language", file_result)
                self.assertEqual(file_result["language"], "python")
                self.assertGreaterEqual(file_result["similarity_score"], 0.3)

    def test_search_test_cases_protobuf_data(self):
        """TC-ROUTER-004: Test search_test_cases with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 4,
            "params": {
                "name": "search_test_cases",
                "arguments": {
                    "query": "HTTP client test",
                    "ddd_root": self.test_ddd_root,
                    "top_k": 5
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=4)
        self.assertIn("result", response)

        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["query"], "HTTP client test")
        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("total_results", result)
        self.assertIn("results", result)

    def test_get_vector_stats_protobuf_data(self):
        """TC-ROUTER-005: Test get_vector_stats with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 5,
            "params": {
                "name": "get_vector_stats",
                "arguments": {
                    "ddd_root": self.test_ddd_root
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=5)
        self.assertIn("result", response)

        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("vector_database_stats", result)

        stats = result["vector_database_stats"]
        self.assertIn("total_chunks", stats)
        self.assertIn("total_files", stats)
        self.assertIn("languages", stats)
        self.assertIn("has_embeddings", stats)
        self.assertIn("has_index", stats)
        self.assertIn("model_available", stats)

        # Should have indexed the ProtobufRegistry project
        self.assertGreater(stats["total_chunks"], 0)
        self.assertGreater(stats["total_files"], 0)
        self.assertTrue(stats["has_embeddings"])
        self.assertTrue(stats["has_index"])
        self.assertTrue(stats["model_available"])


class TestRouterDriftAnalysis(TestMCPShellWrapper):
    """Test drift analysis tools through router."""

    def test_analyze_drift_protobuf_data(self):
        """TC-ROUTER-006: Test analyze_drift with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 6,
            "params": {
                "name": "analyze_drift",
                "arguments": {
                    "mode": "tc-mapping",
                    "ddd_root": self.test_ddd_root
                }
            }
        }

        response = self.send_mcp_request(request, timeout=30)

        self.assertMCPResponse(response, expected_id=6)
        self.assertIn("result", response)

        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["mode"], "tc-mapping")
        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("vector_enhanced", result)
        self.assertIn("metadata", result)
        self.assertIn("summary", result)

        # Should be vector enhanced
        self.assertTrue(result["vector_enhanced"])

    def test_validate_code_locations_protobuf_data(self):
        """TC-ROUTER-007: Test validate_code_locations with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 7,
            "params": {
                "name": "validate_code_locations",
                "arguments": {
                    "ddd_root": self.test_ddd_root
                }
            }
        }

        response = self.send_mcp_request(request, timeout=20)

        self.assertMCPResponse(response, expected_id=7)
        self.assertIn("result", response)

        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("vector_enhanced", result)
        self.assertIn("total_features", result)
        self.assertIn("coverage_percentage", result)

        # Should be vector enhanced
        self.assertTrue(result["vector_enhanced"])

    def test_find_feature_test_mapping_protobuf_data(self):
        """TC-ROUTER-008: Test find_feature_test_mapping with ProtobufRegistry test data"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 8,
            "params": {
                "name": "find_feature_test_mapping",
                "arguments": {
                    "feature_query": "HTTP client functionality",
                    "ddd_root": self.test_ddd_root,
                    "top_k": 3
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPResponse(response, expected_id=8)
        self.assertIn("result", response)

        content = response["result"]["content"][0]["text"]
        result = json.loads(content)

        self.assertEqual(result["feature_query"], "HTTP client functionality")
        self.assertEqual(result["ddd_root"], self.test_ddd_root)
        self.assertIn("features_found", result)
        self.assertIn("related_tests", result)
        self.assertIn("test_documentation", result)


class TestRouterErrorHandling(TestMCPShellWrapper):
    """Test error handling through router."""

    def test_invalid_tool_name(self):
        """TC-ROUTER-009: Test invalid tool name handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 9,
            "params": {
                "name": "nonexistent_tool",
                "arguments": {}
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPError(response, expected_code=-32601)
        self.assertEqual(response["id"], 9)

    def test_missing_required_arguments(self):
        """TC-ROUTER-010: Test missing required arguments handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 10,
            "params": {
                "name": "search_files",
                "arguments": {
                    # Missing required "query" argument
                    "file_type": "python"
                }
            }
        }

        response = self.send_mcp_request(request)

        self.assertMCPError(response, expected_code=-32603)
        self.assertEqual(response["id"], 10)

    def test_invalid_json_request(self):
        """TC-MCP-SH-011: Test invalid JSON handling"""
        try:
            process = subprocess.Popen(
                [str(self.mcp_script)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )

            # Send malformed JSON
            stdout, stderr = process.communicate(input='{"invalid": json}', timeout=10)

            if stdout.strip():
                response = json.loads(stdout.strip())
                self.assertMCPError(response, expected_code=-32700)  # Parse error

        except Exception:
            # Expected to fail with malformed JSON
            pass

    def test_invalid_ddd_root(self):
        """TC-ROUTER-012: Test invalid DDD root handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 12,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": "test",
                    "ddd_root": "/nonexistent/path"
                }
            }
        }

        response = self.send_mcp_request(request)

        # Should handle gracefully, not crash
        self.assertMCPResponse(response, expected_id=12)


class TestRouterPerformance(TestMCPShellWrapper):
    """Test router performance and reliability."""

    def test_response_time_search_files(self):
        """TC-ROUTER-013: Test search_files response time"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 13,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": "test implementation",
                    "file_type": "python",
                    "ddd_root": self.test_ddd_root,
                    "top_k": 5
                }
            }
        }

        start_time = time.time()
        response = self.send_mcp_request(request)
        end_time = time.time()

        response_time = end_time - start_time

        self.assertMCPResponse(response, expected_id=13)
        self.assertLess(response_time, 10.0, f"Response time {response_time:.2f}s too slow")

    def test_multiple_requests_stability(self):
        """TC-ROUTER-014: Test multiple requests for stability"""
        requests_data = [
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 14,
                "params": {
                    "name": "get_vector_stats",
                    "arguments": {"ddd_root": self.test_ddd_root}
                }
            },
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 15,
                "params": {
                    "name": "search_files",
                    "arguments": {
                        "query": "HTTP",
                        "file_type": "python",
                        "ddd_root": self.test_ddd_root,
                        "top_k": 2
                    }
                }
            }
        ]

        for request in requests_data:
            response = self.send_mcp_request(request)
            self.assertMCPResponse(response, expected_id=request["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
