#!/usr/bin/env python3
"""
Demo script for Agent3D MCP Server

This script demonstrates the capabilities of the Agent3D MCP server
with practical examples of intelligent search and analysis.
"""

import json
import subprocess
import sys
import logging
from pathlib import Path

def setup_logging():
    """Setup logging for the demo."""
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

def demo_server_info():
    """Demo: Get server information"""
    logger = setup_logging()
    logger.info("🚀 Demo: Agent3D MCP Server Information")
    
    # Initialize server
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": 1
    }
    
    response = send_mcp_request(init_request)
    
    if "error" in response:
        logger.error(f"❌ Failed to initialize: {response['error']}")
        return
    
    server_info = response.get("result", {}).get("serverInfo", {})
    logger.info(f"✅ Server: {server_info.get('name')} v{server_info.get('version')}")
    logger.info(f"📡 Protocol: {response.get('result', {}).get('protocolVersion')}")

def demo_available_tools():
    """Demo: List available tools"""
    logger = setup_logging()
    logger.info("🔧 Demo: Available Tools")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 2
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Failed to get tools: {response['error']}")
        return
    
    tools = response.get("result", {}).get("tools", [])
    logger.info(f"✅ Found {len(tools)} available tools:")
    
    for i, tool in enumerate(tools, 1):
        logger.info(f"  {i}. {tool['name']}")
        logger.info(f"     {tool['description']}")

def demo_vector_stats():
    """Demo: Vector database statistics"""
    logger = setup_logging()
    logger.info("📊 Demo: Vector Database Statistics")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 3,
        "params": {
            "name": "get_vector_stats",
            "arguments": {}
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Failed to get stats: {response['error']}")
        return
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        stats = result["vector_database_stats"]
        
        logger.info("✅ Vector Database Statistics:")
        logger.info(f"  📁 Total files indexed: {stats['total_files']}")
        logger.info(f"  📄 Total chunks: {stats['total_chunks']}")
        logger.info(f"  💾 Total size: {stats['total_size']:,} bytes")
        logger.info(f"  🧠 Embeddings available: {stats['has_embeddings']}")
        
        logger.info("  📊 Languages:")
        for lang, count in stats['languages'].items():
            logger.info(f"    {lang}: {count} chunks")
            
        logger.info("  🏗️  Chunk types:")
        for chunk_type, count in stats['chunk_types'].items():
            logger.info(f"    {chunk_type}: {count} chunks")
            
    except Exception as e:
        logger.error(f"❌ Failed to parse stats: {e}")

def demo_file_search():
    """Demo: Intelligent file search"""
    logger = setup_logging()
    logger.info("🔍 Demo: Intelligent File Search")
    
    search_queries = [
        ("vector database", "python"),
        ("drift analysis", "any"),
        ("test cases", "test"),
        ("documentation", "doc")
    ]
    
    for query, file_type in search_queries:
        logger.info(f"\n🔎 Searching for '{query}' in {file_type} files...")
        
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 4,
            "params": {
                "name": "search_files",
                "arguments": {
                    "query": query,
                    "file_type": file_type,
                    "top_k": 3
                }
            }
        }
        
        response = send_mcp_request(request)
        
        if "error" in response:
            logger.error(f"❌ Search failed: {response['error']}")
            continue
        
        try:
            content = response["result"]["content"][0]["text"]
            result = json.loads(content)
            
            if result["total_results"] > 0:
                logger.info(f"✅ Found {result['total_results']} results:")
                for i, file_result in enumerate(result['results'], 1):
                    logger.info(f"  {i}. {file_result['file_path']}")
                    logger.info(f"     Score: {file_result['similarity_score']}")
                    logger.info(f"     Type: {file_result['chunk_type']} ({file_result['language']})")
            else:
                logger.info("ℹ️  No results found (vector search may be disabled)")
                
        except Exception as e:
            logger.error(f"❌ Failed to parse search results: {e}")

def demo_feature_search():
    """Demo: Feature search"""
    logger = setup_logging()
    logger.info("🎯 Demo: Feature Search")
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 5,
        "params": {
            "name": "search_features",
            "arguments": {
                "query": "implementation pass",
                "top_k": 3
            }
        }
    }
    
    response = send_mcp_request(request)
    
    if "error" in response:
        logger.error(f"❌ Feature search failed: {response['error']}")
        return
    
    try:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        logger.info(f"✅ Found {result['total_results']} feature results:")
        for i, feature in enumerate(result['results'], 1):
            logger.info(f"  {i}. {feature['type']}: {feature['file_path']}")
            logger.info(f"     Score: {feature['similarity_score']}")
            if feature.get('ft_ids_found'):
                logger.info(f"     FT IDs: {feature['ft_ids_found']}")
            if feature.get('tc_ids_found'):
                logger.info(f"     TC IDs: {feature['tc_ids_found']}")
                
    except Exception as e:
        logger.error(f"❌ Failed to parse feature results: {e}")

def main():
    """Run all demos"""
    logger = setup_logging()
    logger.info("🎬 Starting Agent3D MCP Server Demo")
    logger.info("=" * 60)
    
    demos = [
        ("Server Information", demo_server_info),
        ("Available Tools", demo_available_tools),
        ("Vector Database Stats", demo_vector_stats),
        ("Intelligent File Search", demo_file_search),
        ("Feature Search", demo_feature_search),
    ]
    
    for demo_name, demo_func in demos:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Running: {demo_name}")
        logger.info('=' * 60)
        
        try:
            demo_func()
        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
    
    logger.info(f"\n{'=' * 60}")
    logger.info("🎉 Demo completed!")
    logger.info("=" * 60)
    logger.info("💡 Tips:")
    logger.info("  - Install sentence-transformers for full vector search capabilities")
    logger.info("  - Use the MCP server with your favorite AI assistant")
    logger.info("  - Explore all 7 available tools for comprehensive DDD support")

if __name__ == "__main__":
    main()
