#!/usr/bin/env python3
"""
Comprehensive tests for enhanced MCP tools with validation and error handling.
"""

import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

def test_mcp_tool(tool_name, arguments=None):
    """Test an MCP tool by calling the server directly"""
    if arguments is None:
        arguments = {}

    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }

    try:
        # Run the MCP server with the request
        process = subprocess.run(
            ["python3", "tools/agent3d_mcp_server.py"],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/Users/nwaikhom/.agent3d"
        )

        if process.returncode != 0:
            return {"error": f"MCP server error: {process.stderr}"}

        # Parse the response
        response = json.loads(process.stdout)

        if "error" in response:
            return {"error": response["error"]["message"]}

        # Extract the result from MCP response format
        result_text = response["result"]["content"][0]["text"]
        result = json.loads(result_text)

        return result

    except subprocess.TimeoutExpired:
        return {"error": f"Timeout testing {tool_name}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}
    except Exception as e:
        return {"error": f"Error testing {tool_name}: {e}"}

class TestEnhancedMCPTools:
    """Test suite for enhanced MCP tools with validation"""

    def test_get_template_validation(self):
        """Test get_template input validation"""
        # Test missing template_name
        result = test_mcp_tool("get_template", {})
        assert "error" in result
        assert "template_name" in result["error"]

        # Test empty template_name
        result = test_mcp_tool("get_template", {"template_name": ""})
        assert "error" in result
        assert "required" in result["error"]

        # Test invalid characters (path traversal attempt)
        result = test_mcp_tool("get_template", {"template_name": "../../../etc/passwd"})
        assert "error" in result or result.get("found") == False

    def test_get_template_success(self):
        """Test successful template retrieval"""
        result = test_mcp_tool("get_template", {"template_name": "README"})

        if result.get("found"):
            assert "content" in result
            assert "file_path" in result
            assert "search_method" in result
            assert result["template_name"] == "README"
        else:
            # Template not found is acceptable
            assert "error" in result
            assert "searched_names" in result or "not found" in result["error"]

    def test_get_language_rules_validation(self):
        """Test get_language_rules input validation"""
        # Test missing language
        result = test_mcp_tool("get_language_rules", {})
        assert "error" in result
        assert "language" in result["error"]

        # Test empty language
        result = test_mcp_tool("get_language_rules", {"language": ""})
        assert "error" in result
        assert "required" in result["error"]

        # Test invalid characters
        result = test_mcp_tool("get_language_rules", {"language": "../../../etc/passwd"})
        assert "error" in result or result.get("found") == False

    def test_get_language_rules_success(self):
        """Test successful language rules retrieval"""
        result = test_mcp_tool("get_language_rules", {"language": "python"})

        if result.get("found"):
            assert "content" in result
            assert "file_path" in result
            assert "search_method" in result
            assert result["language"] == "python"
        else:
            # Rules not found is acceptable
            assert "error" in result
            assert "not found" in result["error"]

    def test_get_project_config_with_temp_project(self):
        """Test get_project_config with a temporary project"""
        # Create temporary project
        temp_dir = tempfile.mkdtemp(prefix="agent3d_test_")
        project_dir = Path(temp_dir)

        try:
            # Create basic .agent3d-config.yml
            config_content = """
project:
  name: "test-project"
  type: "library"
  language: "python"

enabled_passes:
  - "requirements"
  - "documentation"
"""
            config_path = project_dir / ".agent3d-config.yml"
            config_path.write_text(config_content.strip())

            # Test with valid project
            result = test_mcp_tool("get_project_config", {"ddd_root": str(project_dir)})

            assert result.get("found") == True
            assert "config_data" in result
            assert result["config_data"]["project"]["name"] == "test-project"

        finally:
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir)

    def test_next_action_with_temp_project(self):
        """Test next_action with a temporary project"""
        # Create temporary project
        temp_dir = tempfile.mkdtemp(prefix="agent3d_test_")
        project_dir = Path(temp_dir)

        try:
            # Create basic project structure
            (project_dir / "docs").mkdir(exist_ok=True)

            # Create basic .agent3d-config.yml
            config_content = """
project:
  name: "test-project"
  type: "library"
  language: "python"

enabled_passes:
  - "requirements"
  - "documentation"
"""
            config_path = project_dir / ".agent3d-config.yml"
            config_path.write_text(config_content.strip())

            # Test next_action
            result = test_mcp_tool("next_action", {"ddd_root": str(project_dir)})

            assert "action" in result
            assert "priority" in result
            assert "description" in result
            assert "next_steps" in result
            assert "suggested_tools" in result
            assert "reasoning" in result

        finally:
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir)

    def test_save_and_update_exec_plan(self):
        """Test execution plan save and update functionality"""
        # Create temporary project
        temp_dir = tempfile.mkdtemp(prefix="agent3d_test_")
        project_dir = Path(temp_dir)

        try:
            # Create basic project structure
            (project_dir / "docs").mkdir(exist_ok=True)
            (project_dir / "docs" / "runs").mkdir(exist_ok=True)

            # Create basic .agent3d-config.yml
            config_content = """
project:
  name: "test-project"
"""
            config_path = project_dir / ".agent3d-config.yml"
            config_path.write_text(config_content.strip())

            # Test save_exec_plan
            plan_data = {
                "task": "Test execution plan",
                "status": "started",
                "execution_steps": ["Step 1", "Step 2"]
            }

            save_result = test_mcp_tool("save_exec_plan", {
                "ddd_root": str(project_dir),
                "plan_name": "test-plan",
                "plan_data": plan_data
            })

            assert save_result.get("saved") == True
            assert "plan_path" in save_result
            assert "filename" in save_result

            # Verify file was created
            plan_file = project_dir / "docs" / "runs" / "EXEC-PLAN-test-plan.yml"
            assert plan_file.exists()

            # Test update_exec_plan
            update_result = test_mcp_tool("update_exec_plan", {
                "ddd_root": str(project_dir),
                "plan_name": "test-plan",
                "update_status": "completed",
                "append_steps": ["Step 3"]
            })

            assert update_result.get("updated") == True
            assert "changes_applied" in update_result

        finally:
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir)

    def test_error_handling_robustness(self):
        """Test error handling for various edge cases"""
        # Test with non-existent project root
        result = test_mcp_tool("get_project_config", {"ddd_root": "/non/existent/path"})
        assert "error" in result or result.get("found") == False

        # Test save_exec_plan without required parameters
        result = test_mcp_tool("save_exec_plan", {})
        assert "error" in result
        assert "plan_name" in result["error"]

        # Test update_exec_plan with non-existent plan
        result = test_mcp_tool("update_exec_plan", {
            "plan_name": "non-existent-plan"
        })
        assert "error" in result or result.get("found") == False

def main():
    """Run the test suite"""
    print("🧪 Testing Enhanced MCP Tools")
    print("=" * 40)

    test_suite = TestEnhancedMCPTools()

    tests = [
        ("Template Validation", test_suite.test_get_template_validation),
        ("Template Success", test_suite.test_get_template_success),
        ("Language Rules Validation", test_suite.test_get_language_rules_validation),
        ("Language Rules Success", test_suite.test_get_language_rules_success),
        ("Project Config", test_suite.test_get_project_config_with_temp_project),
        ("Next Action", test_suite.test_next_action_with_temp_project),
        ("Exec Plan Management", test_suite.test_save_and_update_exec_plan),
        ("Error Handling", test_suite.test_error_handling_robustness),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\n🔍 Running: {test_name}")
            test_func()
            print(f"✅ {test_name} passed")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            failed += 1

    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")

    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
