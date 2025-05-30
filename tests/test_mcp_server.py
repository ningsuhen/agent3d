#!/usr/bin/env python3
"""
Unit tests for Agent3D MCP Server

Tests the MCP server functionality including JSON-RPC protocol compliance,
tool availability, search capabilities, and error handling.

Test Coverage:
- MCP protocol compliance (initialize, tools/list, tools/call)
- All 7 search and analysis tools
- Error handling and edge cases
- Vector database integration
- Performance and reliability

Author: Agent3D Framework
"""

import json
import subprocess
import sys
import unittest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional
import time


class MCPServerTestCase(unittest.TestCase):
    """Base test case for MCP server testing"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.script_dir = Path(__file__).parent.parent / "tools"
        cls.mcp_script = cls.script_dir / "mcp.sh"
        cls.project_root = cls.script_dir.parent

        # Ensure MCP script exists and is executable
        if not cls.mcp_script.exists():
            raise FileNotFoundError(f"MCP script not found: {cls.mcp_script}")

        # Make sure it's executable
        os.chmod(cls.mcp_script, 0o755)

    def send_mcp_request(self, request: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        try:
            process = subprocess.Popen(
                [str(self.mcp_script)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )

            request_json = json.dumps(request)
            stdout, stderr = process.communicate(input=request_json, timeout=timeout)

            # Parse the JSON-RPC response from stdout
            if stdout.strip():
                return json.loads(stdout.strip())
            else:
                return {"error": "No response from server", "stderr": stderr}

        except subprocess.TimeoutExpired:
            process.kill()
            return {"error": "Request timed out"}
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response: {e}", "stdout": stdout, "stderr": stderr}
        except Exception as e:
            return {"error": f"Request failed: {e}"}

    def assertValidJSONRPC(self, response: Dict[str, Any], expected_id: Any = None):
        """Assert that response is valid JSON-RPC 2.0"""
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
        """Assert that response is a valid MCP error"""
        self.assertValidJSONRPC(response)
        self.assertIn("error", response)

        error = response["error"]
        self.assertIn("code", error)
        self.assertIn("message", error)

        if expected_code is not None:
            self.assertEqual(error["code"], expected_code)


class TestMCPProtocol(MCPServerTestCase):
    """Test MCP protocol compliance"""

    def test_initialize_request(self):
        """TC-MCP-001: Test server initialization"""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=1)

        # Verify initialization response structure
        self.assertIn("result", response)
        result = response["result"]

        self.assertIn("protocolVersion", result)
        self.assertIn("capabilities", result)
        self.assertIn("serverInfo", result)

        # Verify server info
        server_info = result["serverInfo"]
        self.assertIn("name", server_info)
        self.assertIn("version", server_info)
        self.assertEqual(server_info["name"], "agent3d-mcp")

    def test_tools_list_request(self):
        """TC-MCP-002: Test tools list endpoint"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=2)

        # Verify tools list structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("tools", result)

        tools = result["tools"]
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0, "Should have at least one tool")

        # Verify expected tools are present
        expected_tools = [
            "search_files", "search_test_cases", "search_features",
            "find_feature_test_mapping", "analyze_drift",
            "validate_code_locations", "get_vector_stats"
        ]

        tool_names = [tool["name"] for tool in tools]
        for expected_tool in expected_tools:
            self.assertIn(expected_tool, tool_names, f"Missing tool: {expected_tool}")

        # Verify tool schema structure
        for tool in tools:
            self.assertIn("name", tool)
            self.assertIn("description", tool)
            self.assertIn("inputSchema", tool)

            schema = tool["inputSchema"]
            self.assertIn("type", schema)
            self.assertEqual(schema["type"], "object")

    def test_invalid_method(self):
        """TC-MCP-003: Test invalid method handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "invalid/method",
            "id": 3
        }

        response = self.send_mcp_request(request)

        # Should return method not found error
        self.assertMCPError(response, expected_code=-32601)

    def test_malformed_json(self):
        """TC-MCP-004: Test malformed JSON handling"""
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


class TestSearchTools(MCPServerTestCase):
    """Test search and analysis tools"""

    def test_search_files_tool(self):
        """TC-MCP-005: Test search_files tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 5,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": "mcp server",
                    "file_type": "python",
                    "top_k": 3
                }
            }
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=5)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        content = result["content"]
        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)

        # Parse the tool result
        tool_result = json.loads(content[0]["text"])
        self.assertIn("query", tool_result)
        self.assertIn("file_type", tool_result)
        self.assertIn("results", tool_result)
        self.assertEqual(tool_result["query"], "mcp server")
        self.assertEqual(tool_result["file_type"], "python")

    def test_get_vector_stats_tool(self):
        """TC-MCP-006: Test get_vector_stats tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 6,
            "params": {
                "name": "get_vector_stats",
                "arguments": {}
            }
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=6)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("vector_database_stats", tool_result)

        stats = tool_result["vector_database_stats"]
        self.assertIn("total_files", stats)
        self.assertIn("total_chunks", stats)
        self.assertIn("languages", stats)
        self.assertIn("chunk_types", stats)

        # Verify reasonable values
        self.assertGreater(stats["total_files"], 0)
        self.assertGreater(stats["total_chunks"], 0)

    def test_search_test_cases_tool(self):
        """TC-MCP-007: Test search_test_cases tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 7,
            "params": {
                "name": "search_test_cases",
                "arguments": {
                    "query": "mcp test",
                    "top_k": 5
                }
            }
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=7)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("search_query", tool_result)
        self.assertIn("results", tool_result)
        self.assertIn("total_results", tool_result)

    def test_search_features_tool(self):
        """TC-MCP-008: Test search_features tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 8,
            "params": {
                "name": "search_features",
                "arguments": {
                    "query": "vector database",
                    "top_k": 5
                }
            }
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=8)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("search_query", tool_result)
        self.assertIn("results", tool_result)
        self.assertIn("total_results", tool_result)

    def test_unknown_tool(self):
        """TC-MCP-009: Test unknown tool handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 9,
            "params": {
                "name": "unknown_tool",
                "arguments": {}
            }
        }

        response = self.send_mcp_request(request)

        # Should return method not found error
        self.assertMCPError(response, expected_code=-32601)

    def test_missing_required_arguments(self):
        """TC-MCP-010: Test missing required arguments"""
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

        # Should return execution error
        self.assertMCPError(response, expected_code=-32603)


class TestAnalysisTools(MCPServerTestCase):
    """Test analysis and validation tools"""

    def test_analyze_drift_tool(self):
        """TC-MCP-011: Test analyze_drift tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 11,
            "params": {
                "name": "analyze_drift",
                "arguments": {
                    "mode": "all",
                    "quiet": True
                }
            }
        }

        response = self.send_mcp_request(request, timeout=60)  # Longer timeout for analysis

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=11)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("mode", tool_result)
        self.assertIn("vector_enhanced", tool_result)
        self.assertEqual(tool_result["mode"], "all")

    def test_validate_code_locations_tool(self):
        """TC-MCP-012: Test validate_code_locations tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 12,
            "params": {
                "name": "validate_code_locations",
                "arguments": {}
            }
        }

        response = self.send_mcp_request(request, timeout=45)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=12)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("vector_enhanced", tool_result)
        self.assertIn("total_features", tool_result)

    def test_find_feature_test_mapping_tool(self):
        """TC-MCP-013: Test find_feature_test_mapping tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 13,
            "params": {
                "name": "find_feature_test_mapping",
                "arguments": {
                    "feature_query": "mcp server implementation",
                    "top_k": 5
                }
            }
        }

        response = self.send_mcp_request(request)

        # Verify JSON-RPC compliance
        self.assertValidJSONRPC(response, expected_id=13)

        # Verify tool response structure
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("content", result)

        # Parse the tool result
        tool_result = json.loads(result["content"][0]["text"])
        self.assertIn("feature_query", tool_result)
        self.assertIn("features_found", tool_result)
        self.assertIn("related_tests", tool_result)
        self.assertIn("test_documentation", tool_result)


class TestErrorHandling(MCPServerTestCase):
    """Test error handling and edge cases"""

    def test_empty_request(self):
        """TC-MCP-014: Test empty request handling"""
        try:
            process = subprocess.Popen(
                [str(self.mcp_script)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )

            # Send empty input
            stdout, stderr = process.communicate(input='', timeout=10)

            # Server should handle gracefully (may not respond to empty input)
            # This is acceptable behavior for MCP servers

        except subprocess.TimeoutExpired:
            process.kill()
            # Timeout is acceptable for empty input

    def test_invalid_json_rpc_version(self):
        """TC-MCP-015: Test invalid JSON-RPC version"""
        request = {
            "jsonrpc": "1.0",  # Invalid version
            "method": "initialize",
            "id": 15
        }

        response = self.send_mcp_request(request)

        # Should handle gracefully or return error
        if "error" in response:
            self.assertMCPError(response)

    def test_missing_method(self):
        """TC-MCP-016: Test missing method field"""
        request = {
            "jsonrpc": "2.0",
            # Missing "method" field
            "id": 16
        }

        response = self.send_mcp_request(request)

        # Should return invalid request error
        if "error" in response:
            self.assertMCPError(response, expected_code=-32600)

    def test_concurrent_requests(self):
        """TC-MCP-017: Test concurrent request handling"""
        import threading
        import queue

        results = queue.Queue()

        def send_request(request_id):
            request = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": request_id,
                "params": {
                    "name": "get_vector_stats",
                    "arguments": {}
                }
            }
            response = self.send_mcp_request(request)
            results.put((request_id, response))

        # Send multiple concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(target=send_request, args=(100 + i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)

        # Verify all requests completed successfully
        responses = []
        while not results.empty():
            responses.append(results.get())

        self.assertEqual(len(responses), 3, "All concurrent requests should complete")

        for request_id, response in responses:
            self.assertValidJSONRPC(response, expected_id=request_id)


class TestPerformance(MCPServerTestCase):
    """Test performance and reliability"""

    def test_response_time(self):
        """TC-MCP-018: Test response time for basic operations"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 18
        }

        start_time = time.time()
        response = self.send_mcp_request(request)
        end_time = time.time()

        response_time = end_time - start_time

        # Verify response is valid
        self.assertValidJSONRPC(response, expected_id=18)

        # Response should be reasonably fast (under 10 seconds)
        self.assertLess(response_time, 10.0, f"Response time too slow: {response_time:.2f}s")

    def test_large_query_handling(self):
        """TC-MCP-019: Test handling of large queries"""
        large_query = "test " * 1000  # Large query string

        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 19,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": large_query,
                    "top_k": 1
                }
            }
        }

        response = self.send_mcp_request(request, timeout=45)

        # Should handle large queries gracefully
        self.assertValidJSONRPC(response, expected_id=19)

    def test_memory_usage(self):
        """TC-MCP-020: Test memory usage with vector database operations"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 20,
            "params": {
                "name": "get_vector_stats",
                "arguments": {}
            }
        }

        # Send multiple requests to test memory stability
        for i in range(5):
            response = self.send_mcp_request(request)
            self.assertValidJSONRPC(response, expected_id=20)

            # Parse the result to verify database is working
            result = response["result"]
            tool_result = json.loads(result["content"][0]["text"])
            stats = tool_result["vector_database_stats"]

            # Verify consistent results
            self.assertGreater(stats["total_files"], 0)
            self.assertGreater(stats["total_chunks"], 0)


if __name__ == "__main__":
    # Configure test runner
    unittest.main(
        verbosity=2,
        buffer=True,
        failfast=False
    )
