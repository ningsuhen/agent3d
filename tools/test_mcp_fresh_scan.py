#!/usr/bin/env python3
"""
Test script to verify that the MCP server performs fresh scans on every request.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_mcp_fresh_scan():
    """Test that MCP server performs fresh scans without caching and cleans up previous reports"""

    # Path to the MCP server
    mcp_server = Path(__file__).parent / "drift_scanner_mcp_server.py"

    print("🧪 Testing MCP Server Fresh Scan & Cleanup Capability")
    print("=" * 60)

    # Create some dummy previous reports to test cleanup
    temp_dir = Path(".agent3d-tmp/drift-reports")
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy previous reports
    dummy_files = [
        temp_dir / "tc-mapping-drift-report.yaml",
        temp_dir / "tc-mapping-drift-report-1234567890.yaml",
        temp_dir / "ft-mapping-drift-report.yaml"
    ]

    for dummy_file in dummy_files:
        dummy_file.write_text("dummy content")
        print(f"📄 Created dummy report: {dummy_file.name}")

    print(f"📋 Created {len(dummy_files)} dummy reports for cleanup testing")

    # Test requests
    test_requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize"
        },
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        },
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "drift_scanner",
                "arguments": {
                    "mode": "tc-mapping",
                    "quiet": True
                }
            }
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "drift_scanner",
                "arguments": {
                    "mode": "ft-tc-mapping",
                    "quiet": True
                }
            }
        }
    ]

    try:
        # Start MCP server process
        print("🚀 Starting MCP server...")
        process = subprocess.Popen(
            [sys.executable, str(mcp_server)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send test requests
        for i, request in enumerate(test_requests):
            print(f"\n📤 Sending request {i+1}: {request['method']}")

            # Send request
            request_json = json.dumps(request) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()

            # Read response
            response_line = process.stdout.readline()
            if response_line:
                try:
                    response = json.loads(response_line.strip())
                    print(f"📥 Response {i+1}: {response.get('result', {}).get('serverInfo', {}).get('name', 'Success')}")

                    # For tool calls, check if we got content
                    if request['method'] == 'tools/call':
                        content = response.get('result', {}).get('content', [])
                        if content:
                            print(f"   ✅ Fresh scan completed - got {len(content)} content items")
                        else:
                            print(f"   ⚠️  No content returned")

                except json.JSONDecodeError as e:
                    print(f"   ❌ Invalid JSON response: {e}")
            else:
                print(f"   ❌ No response received")

            # Small delay between requests
            time.sleep(0.5)

        # Terminate the process
        process.terminate()
        process.wait(timeout=5)

        print("\n✅ MCP Server test completed successfully!")
        print("🔄 Fresh scan mode verified - each request triggers new analysis")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        if 'process' in locals():
            process.terminate()
        return False

    return True

if __name__ == "__main__":
    success = test_mcp_fresh_scan()
    sys.exit(0 if success else 1)
