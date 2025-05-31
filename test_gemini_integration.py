#!/usr/bin/env python3
"""
Test script for Google Gemini integration with Agent3D DDD Framework

This script tests the Gemini client integration without running a full DDD pass.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_gemini_import():
    """Test if Google AI package can be imported."""
    print("🔍 Testing Google AI package import...")
    try:
        import google.generativeai as genai
        print("✅ Google AI package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Google AI package: {e}")
        return False

def test_gemini_client():
    """Test if Gemini client can be created."""
    print("\n🔍 Testing Gemini client creation...")
    try:
        from agents.swebench.utils.llm_client import GeminiDirectClient, GOOGLE_AI_AVAILABLE
        
        if not GOOGLE_AI_AVAILABLE:
            print("❌ Google AI package not available")
            return False
        
        # Check for API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not set - client creation will fail")
            print("   To get an API key: https://aistudio.google.com/app/apikey")
            print("   Then run: export GOOGLE_API_KEY=your_api_key")
            return False
        
        # Try to create client
        client = GeminiDirectClient(model_name="gemini-1.5-pro")
        print("✅ Gemini client created successfully")
        print(f"   Model: {client.model_name}")
        print(f"   Max retries: {client.max_retries}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Gemini client: {e}")
        return False

def test_swebench_integration():
    """Test if SWE-bench tool can use Gemini."""
    print("\n🔍 Testing SWE-bench tool integration...")
    try:
        from agents.orchestrator.tools import SWEBenchTool
        import logging
        
        # Create a logger
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        
        # Try to create SWE-bench tool
        tool = SWEBenchTool(logger=logger)
        
        if tool.agent is None:
            print("⚠️  SWE-bench agent not initialized (likely due to missing API key)")
            return False
        
        print("✅ SWE-bench tool created successfully with LLM client")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create SWE-bench tool: {e}")
        return False

def test_orchestrator_integration():
    """Test if orchestrator can be created with Gemini support."""
    print("\n🔍 Testing orchestrator integration...")
    try:
        from agents.orchestrator import create_orchestrator_graph
        import logging
        
        # Create a logger
        logger = logging.getLogger("test_orchestrator")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        
        # Try to create orchestrator
        orchestrator = create_orchestrator_graph(
            logger=logger,
            max_iterations=1,
            enable_swebench=True
        )
        
        print("✅ Orchestrator created successfully")
        print(f"   SWE-bench enabled: {orchestrator.enable_swebench}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create orchestrator: {e}")
        return False

def main():
    """Run all tests."""
    print("🎯 Agent3D Gemini Integration Test")
    print("=" * 50)
    
    tests = [
        ("Google AI Package Import", test_gemini_import),
        ("Gemini Client Creation", test_gemini_client),
        ("SWE-bench Integration", test_swebench_integration),
        ("Orchestrator Integration", test_orchestrator_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini integration is ready.")
        print("\nNext steps:")
        print("1. Set GOOGLE_API_KEY if not already set")
        print("2. Run: ./ddd-pass.sh --task 'Test task' --verbose")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("\n💡 Quick fix: Set your Google API key")
            print("   1. Get key from: https://aistudio.google.com/app/apikey")
            print("   2. Run: export GOOGLE_API_KEY=your_api_key")
            print("   3. Re-run this test")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
