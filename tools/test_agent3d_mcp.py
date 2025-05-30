#!/usr/bin/env python3
"""
Test script for Agent3D MCP Server

This script tests the comprehensive Agent3D MCP server with its intelligent search
and analysis capabilities.
"""

import json
import subprocess
import sys
import time
import logging
from pathlib import Path

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s'
    )
    return logging.getLogger(__name__)

def send_mcp_request(request_data):
    """Send a request to the MCP server and get response"""
    try:
        # Start the MCP server
        process = subprocess.Popen(
            [sys.executable, "tools/agent3d_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path.cwd()
        )
        
        # Send request
        request_json = json.dumps(request_data)
        stdout, stderr = process.communicate(input=request_json, timeout=30)
        
        if stderr:
            print(f"Server stderr: {stderr}")
        
        # Parse response
        if stdout.strip():
            return json.loads(stdout.strip())
        else:
            return {"error": "No response from server"}
            
    except subprocess.TimeoutExpired:
        process.kill()
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": str(e)}

def test_initialize():
    """Test MCP server initialization"""
    logger = setup_logging()
    logger.info("🧪 Testing MCP Server Initialization")
    
    request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": 1
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Initialization failed: {response['error']}")
        return False
    
    if response.get("result", {}).get("serverInfo", {}).get("name") == "agent3d-mcp":
        logger.info("✅ Server initialized successfully")
        return True
    else:
        logger.error(f"❌ Unexpected response: {response}")
        return False

def test_tools_list():
    """Test tools/list endpoint"""
    logger = setup_logging()
    logger.info("🧪 Testing Tools List")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 2
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Tools list failed: {response['error']}")
        return False
    
    tools = response.get("result", {}).get("tools", [])
    expected_tools = [
        "search_files", "search_test_cases", "search_features",
        "find_feature_test_mapping", "analyze_drift", 
        "validate_code_locations", "get_vector_stats"
    ]
    
    tool_names = [tool["name"] for tool in tools]
    
    for expected_tool in expected_tools:
        if expected_tool in tool_names:
            logger.info(f"  ✅ {expected_tool}")
        else:
            logger.error(f"  ❌ Missing tool: {expected_tool}")
            return False
    
    logger.info(f"✅ All {len(expected_tools)} tools available")
    return True

def test_search_files():
    """Test search_files tool"""
    logger = setup_logging()
    logger.info("🧪 Testing Search Files")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 3,
        "params": {
            "name": "search_files",
            "arguments": {
                "query": "drift scanner test",
                "file_type": "python",
                "top_k": 5
            }
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Search files failed: {response['error']}")
        return False
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "results" in result:
            logger.info(f"✅ Found {len(result['results'])} files")
            for i, file_result in enumerate(result['results'][:3]):
                logger.info(f"  {i+1}. {file_result['file_path']} (score: {file_result['similarity_score']})")
            return True
        else:
            logger.error(f"❌ Unexpected result format: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to parse response: {e}")
        return False

def test_search_test_cases():
    """Test search_test_cases tool"""
    logger = setup_logging()
    logger.info("🧪 Testing Search Test Cases")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 4,
        "params": {
            "name": "search_test_cases",
            "arguments": {
                "query": "drift analysis test",
                "top_k": 5
            }
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Search test cases failed: {response['error']}")
        return False
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "results" in result:
            logger.info(f"✅ Found {len(result['results'])} test case results")
            for i, tc_result in enumerate(result['results'][:3]):
                logger.info(f"  {i+1}. {tc_result['type']}: {tc_result['file_path']} (score: {tc_result['similarity_score']})")
                if tc_result.get('tc_ids_found'):
                    logger.info(f"      TC IDs: {tc_result['tc_ids_found']}")
            return True
        else:
            logger.error(f"❌ Unexpected result format: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to parse response: {e}")
        return False

def test_search_features():
    """Test search_features tool"""
    logger = setup_logging()
    logger.info("🧪 Testing Search Features")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 5,
        "params": {
            "name": "search_features",
            "arguments": {
                "query": "vector database",
                "top_k": 5
            }
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Search features failed: {response['error']}")
        return False
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "results" in result:
            logger.info(f"✅ Found {len(result['results'])} feature results")
            for i, ft_result in enumerate(result['results'][:3]):
                logger.info(f"  {i+1}. {ft_result['type']}: {ft_result['file_path']} (score: {ft_result['similarity_score']})")
                if ft_result.get('ft_ids_found'):
                    logger.info(f"      FT IDs: {ft_result['ft_ids_found']}")
            return True
        else:
            logger.error(f"❌ Unexpected result format: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to parse response: {e}")
        return False

def test_get_vector_stats():
    """Test get_vector_stats tool"""
    logger = setup_logging()
    logger.info("🧪 Testing Vector Stats")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 6,
        "params": {
            "name": "get_vector_stats",
            "arguments": {}
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Get vector stats failed: {response['error']}")
        return False
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "vector_database_stats" in result:
            stats = result["vector_database_stats"]
            logger.info(f"✅ Vector database stats retrieved")
            logger.info(f"  Total chunks: {stats.get('total_chunks', 0)}")
            logger.info(f"  Total files: {stats.get('total_files', 0)}")
            logger.info(f"  Index time: {stats.get('index_time', 0):.2f}s")
            return True
        else:
            logger.error(f"❌ Unexpected result format: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to parse response: {e}")
        return False

def main():
    """Run all MCP server tests"""
    logger = setup_logging()
    logger.info("🚀 Starting Agent3D MCP Server Tests")
    
    tests = [
        ("Initialize Server", test_initialize),
        ("Tools List", test_tools_list),
        ("Search Files", test_search_files),
        ("Search Test Cases", test_search_test_cases),
        ("Search Features", test_search_features),
        ("Vector Stats", test_get_vector_stats),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {test_name}")
        logger.info('='*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info('='*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {status} - {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All Agent3D MCP server tests passed!")
        return 0
    else:
        logger.error("💥 Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    exit(main())
