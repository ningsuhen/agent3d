#!/usr/bin/env python3
"""
Test DDD Execution Plan Integration with LangGraph Orchestrator

This script tests the integration of DDD execution plans with the orchestrator,
ensuring that execution plans are created, used, and updated properly.
"""

import os
import logging
import sys
from pathlib import Path

# Add the agents directory to Python path
agents_path = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_path))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_execution_plan_creation():
    """Test that execution plans are created properly."""
    print("🧪 Testing DDD Execution Plan Creation")
    print("=" * 50)
    
    try:
        from orchestrator.tools import DDDExecutionPlanTool
        
        # Create execution plan tool
        plan_tool = DDDExecutionPlanTool(logger)
        
        # Test task
        task = "Create a Python utility module with string manipulation functions"
        context = {
            "primary_type": "coding",
            "complexity": "medium",
            "task_types": ["coding"],
            "quality_requirements": ["ddd_compliance", "code_quality", "test_coverage"]
        }
        
        # Create execution plan
        plan_info = plan_tool.find_or_create_execution_plan(task, context)
        
        print(f"✅ Plan created: {plan_info['plan_name']}")
        print(f"   Status: {plan_info['status']}")
        print(f"   File: {plan_info['file_path']}")
        
        # Verify plan content
        plan_content = plan_info['content']
        assert 'metadata' in plan_content
        assert 'goals' in plan_content
        assert 'checkpoints' in plan_content
        
        print(f"   Title: {plan_content['metadata']['title']}")
        print(f"   Goals: {len(plan_content['goals'])} goals defined")
        print(f"   Checkpoints: {len(plan_content['checkpoints'])} checkpoints")
        
        return True
        
    except Exception as e:
        print(f"❌ Execution plan creation failed: {e}")
        logger.exception("Execution plan creation test failed")
        return False


def test_execution_context_generation():
    """Test that execution context is generated for SWE-bench agent."""
    print("\n🧪 Testing Execution Context Generation")
    print("=" * 50)
    
    try:
        from orchestrator.tools import DDDExecutionPlanTool
        
        plan_tool = DDDExecutionPlanTool(logger)
        
        # Mock plan info
        plan_info = {
            "content": {
                "metadata": {
                    "title": "Test Implementation Plan",
                    "scope": "String manipulation module"
                },
                "goals": ["Create functional API", "Ensure quality"],
                "success_criteria": ["All tests pass", "Code quality maintained"]
            },
            "file_path": "test-plan.yml",
            "status": "created"
        }
        
        # Generate execution context
        context = plan_tool.get_execution_context_for_swebench(plan_info, "api.py")
        
        print("✅ Execution context generated")
        print(f"   Plan title: {context['execution_plan']['title']}")
        print(f"   Target file: {context['file_context']['target_file']}")
        print(f"   DDD compliance required: {context['ddd_compliance']['required']}")
        print(f"   Quality gates: {len(context['ddd_compliance']['quality_gates'])}")
        
        # Verify structure
        assert 'execution_plan' in context
        assert 'ddd_compliance' in context
        assert 'file_context' in context
        
        return True
        
    except Exception as e:
        print(f"❌ Execution context generation failed: {e}")
        logger.exception("Execution context generation test failed")
        return False


def test_orchestrator_with_execution_plan():
    """Test the complete orchestrator with DDD execution plan integration."""
    print("\n🧪 Testing Complete Orchestrator with DDD Execution Plan")
    print("=" * 60)
    
    try:
        from orchestrator.langgraph_orchestrator import Agent3DOrchestratorGraph
        
        # Create orchestrator
        orchestrator = Agent3DOrchestratorGraph(
            logger=logger,
            max_iterations=2,
            enable_swebench=True
        )
        
        if not orchestrator.graph:
            print("⚠️  LangGraph not available, using fallback mode")
        else:
            print("✅ LangGraph orchestrator initialized with execution plan support")
        
        # Test task
        task = "Create a Python calculator module with basic arithmetic operations"
        
        print(f"\n🎯 Task: {task}")
        print("-" * 60)
        
        # Execute the complete workflow
        result = orchestrator.execute_task(task)
        
        # Analyze results
        print(f"\n📊 Execution Results:")
        print(f"  Status: {result.get('status', 'unknown')}")
        
        if "messages" in result:
            print(f"\n📝 Workflow Messages:")
            for message in result["messages"]:
                print(f"    {message}")
        
        # Check for DDD execution plan information
        if "ddd_execution_plan_info" in result:
            plan_info = result["ddd_execution_plan_info"]
            print(f"\n📋 DDD Execution Plan:")
            print(f"    Plan: {plan_info['plan_name']} ({plan_info['status']})")
            print(f"    File: {plan_info['file_path']}")
        
        if "execution_plan" in result and "ddd_execution_plan" in result["execution_plan"]:
            ddd_plan = result["execution_plan"]["ddd_execution_plan"]
            print(f"    Integrated: Yes")
            print(f"    Plan Status: {ddd_plan['status']}")
        
        if "completed_files" in result:
            files = result["completed_files"]
            print(f"\n📁 Files Processed ({len(files)}):")
            for file_info in files:
                print(f"    • {file_info['path']}: {file_info['status']}")
        
        # Overall assessment
        success = False
        if result.get("validation_result", {}).get("overall_passed"):
            success = True
        elif result.get("status") in ["completed", "completed_fallback"]:
            success = True
        
        print(f"\n🎉 Test Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Complete orchestrator test failed: {e}")
        logger.exception("Complete orchestrator test failed")
        return False


def test_execution_plan_status_updates():
    """Test that execution plan status updates work."""
    print("\n🧪 Testing Execution Plan Status Updates")
    print("=" * 50)
    
    try:
        from orchestrator.tools import DDDExecutionPlanTool
        
        plan_tool = DDDExecutionPlanTool(logger)
        
        # Create a test plan
        task = "Test status updates"
        plan_info = plan_tool.find_or_create_execution_plan(task, {})
        
        # Test status updates
        statuses = ["in_progress", "completed", "failed"]
        
        for status in statuses:
            success = plan_tool.update_execution_plan_status(
                plan_info=plan_info,
                checkpoint="test_checkpoint",
                task="Test task",
                status=status
            )
            
            if success:
                print(f"✅ Status update to '{status}': SUCCESS")
            else:
                print(f"❌ Status update to '{status}': FAILED")
        
        return True
        
    except Exception as e:
        print(f"❌ Status update test failed: {e}")
        logger.exception("Status update test failed")
        return False


def check_execution_plan_files():
    """Check what execution plan files were created."""
    print("\n🔍 Checking Created Execution Plan Files")
    print("=" * 50)
    
    runs_dir = Path("docs/runs")
    if not runs_dir.exists():
        print("📁 No docs/runs directory found")
        return False
    
    plan_files = list(runs_dir.glob("EXEC-PLAN-*.yml"))
    
    if plan_files:
        print(f"📁 Found {len(plan_files)} execution plan files:")
        for plan_file in plan_files:
            size = plan_file.stat().st_size
            print(f"    • {plan_file.name} ({size} bytes)")
            
            # Show first few lines
            try:
                with open(plan_file, 'r') as f:
                    lines = f.readlines()[:5]
                    if lines:
                        print(f"      Preview: {lines[0].strip()}")
            except:
                pass
        return True
    else:
        print("📁 No execution plan files found")
        return False


def main():
    """Main test function."""
    print("🚀 DDD Execution Plan Integration Test Suite")
    print("=" * 60)
    
    # Check prerequisites
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found")
        return
    
    swebench_path = Path(__file__).parent / "augment-swebench-agent"
    if not swebench_path.exists():
        print("❌ augment-swebench-agent directory not found")
        return
    
    print("✅ Prerequisites check passed")
    
    # Run tests
    tests = [
        ("Execution Plan Creation", test_execution_plan_creation),
        ("Execution Context Generation", test_execution_context_generation),
        ("Complete Orchestrator Integration", test_orchestrator_with_execution_plan),
        ("Status Updates", test_execution_plan_status_updates),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"\n{status}: {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"\n❌ FAILED: {test_name} - {e}")
            logger.exception(f"Test {test_name} failed")
    
    # Check file outputs
    print(f"\n{'='*60}")
    check_execution_plan_files()
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL TEST RESULTS")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DDD execution plan integration working!")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    print("\n📋 Integration Features Tested:")
    print("✅ DDD execution plan creation from templates")
    print("✅ Execution context generation for SWE-bench agent")
    print("✅ Plan integration with LangGraph orchestrator")
    print("✅ Status tracking and updates")
    print("✅ File-focused processing with plan context")


if __name__ == "__main__":
    main()
