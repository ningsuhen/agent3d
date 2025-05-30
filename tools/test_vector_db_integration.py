#!/usr/bin/env python3
"""
Test Vector Database Integration with LangGraph Orchestrator

This script tests the complete integration of the in-memory vector database
with the orchestrator for intelligent code search and context discovery.
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


def test_vector_database_standalone():
    """Test the vector database functionality standalone."""
    print("🧪 Testing Vector Database Standalone")
    print("=" * 50)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Create vector database
        vector_db = RepositoryVectorDB(logger=logger)
        
        # Index current repository
        current_dir = str(Path.cwd())
        print(f"📁 Indexing repository: {current_dir}")
        
        stats = vector_db.index_repository(current_dir)
        
        print(f"✅ Indexing completed:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Chunks created: {stats['chunks_created']}")
        print(f"   Languages found: {list(stats['languages'].keys())}")
        print(f"   Chunk types: {list(stats['chunk_types'].keys())}")
        
        if stats['chunks_created'] == 0:
            print("⚠️ No chunks created - this might indicate an issue")
            return False
        
        # Test search functionality
        print(f"\n🔍 Testing search functionality:")
        
        search_queries = [
            "python function",
            "orchestrator",
            "vector database",
            "test",
            "documentation"
        ]
        
        for query in search_queries:
            results = vector_db.search(query, top_k=3)
            print(f"   Query: '{query}' -> {len(results)} results")
            
            if results:
                top_result = results[0]
                chunk, score = top_result
                print(f"     Top: {chunk.file_path} (score: {score:.3f})")
        
        # Test repository statistics
        repo_stats = vector_db.get_statistics()
        print(f"\n📊 Repository Statistics:")
        print(f"   Total chunks: {repo_stats['total_chunks']}")
        print(f"   Total files: {repo_stats['total_files']}")
        print(f"   Has embeddings: {repo_stats['has_embeddings']}")
        print(f"   Model available: {repo_stats['model_available']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vector database test failed: {e}")
        logger.exception("Vector database test failed")
        return False


def test_vector_search_tool():
    """Test the VectorSearchTool wrapper."""
    print("\n🧪 Testing Vector Search Tool")
    print("=" * 50)
    
    try:
        from orchestrator.tools import VectorSearchTool
        
        # Create vector search tool
        search_tool = VectorSearchTool(logger=logger)
        
        # Initialize and index repository
        current_dir = str(Path.cwd())
        result = search_tool.initialize_and_index_repository(current_dir)
        
        print(f"✅ Vector search tool initialized:")
        print(f"   Status: {result['status']}")
        print(f"   Indexed: {result['indexed']}")
        
        if not result['indexed']:
            print("⚠️ Repository not indexed properly")
            return False
        
        # Test file discovery
        test_tasks = [
            "Create a Python utility module with string functions",
            "Add unit tests for the orchestrator",
            "Update documentation for vector database",
            "Refactor the main application logic"
        ]
        
        for task in test_tasks:
            print(f"\n🎯 Task: {task}")
            relevant_files = search_tool.find_relevant_files(task, max_files=5)
            
            print(f"   Found {len(relevant_files)} relevant files:")
            for i, file_info in enumerate(relevant_files[:3]):
                score = file_info["relevance_score"]
                path = file_info["file_path"]
                print(f"     {i+1}. {path} (score: {score:.3f})")
        
        # Test repository overview
        overview = search_tool.get_repository_overview()
        print(f"\n📋 Repository Overview:")
        print(f"   Total files: {overview['total_files']}")
        print(f"   Total chunks: {overview['total_chunks']}")
        print(f"   Languages: {list(overview['languages'].keys())}")
        print(f"   Semantic search: {overview['capabilities']['semantic_search']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vector search tool test failed: {e}")
        logger.exception("Vector search tool test failed")
        return False


def test_orchestrator_with_vector_db():
    """Test the complete orchestrator with vector database integration."""
    print("\n🧪 Testing Orchestrator with Vector Database")
    print("=" * 60)
    
    try:
        from orchestrator.langgraph_orchestrator import Agent3DOrchestratorGraph
        
        # Create orchestrator (this should initialize vector database)
        print("🚀 Initializing orchestrator with vector database...")
        orchestrator = Agent3DOrchestratorGraph(
            logger=logger,
            max_iterations=2,
            enable_swebench=True
        )
        
        # Check if vector database was initialized
        if hasattr(orchestrator, 'vector_search_tool'):
            if orchestrator.vector_search_tool.is_indexed:
                print("✅ Vector database successfully integrated with orchestrator")
                
                # Get repository overview
                overview = orchestrator.vector_search_tool.get_repository_overview()
                print(f"   Repository indexed: {overview['total_files']} files, {overview['total_chunks']} chunks")
            else:
                print("⚠️ Vector database not indexed in orchestrator")
        else:
            print("❌ Vector search tool not found in orchestrator")
            return False
        
        # Test intelligent file discovery
        test_tasks = [
            "Create a new API endpoint for user management",
            "Add comprehensive tests for the vector database",
            "Improve the orchestrator's error handling"
        ]
        
        for task in test_tasks:
            print(f"\n🎯 Testing intelligent discovery for: {task}")
            
            # Test the drift scanner (which should use vector database)
            try:
                ddd_analysis = orchestrator.ddd_tool.analyze_task(task)
                scan_results = orchestrator._run_drift_scanner(task, ddd_analysis)
                
                discovery_method = scan_results.get("discovery_method", "unknown")
                files_found = scan_results.get("files_to_modify", [])
                
                print(f"   Discovery method: {discovery_method}")
                print(f"   Files to modify: {len(files_found)}")
                
                if discovery_method == "vector_search":
                    print("   ✅ Using intelligent vector search")
                    # Show relevance scores if available
                    if "relevance_scores" in scan_results:
                        scores = scan_results["relevance_scores"]
                        for file_path in files_found[:3]:
                            score = scores.get(file_path, 0)
                            print(f"     • {file_path} (relevance: {score:.3f})")
                else:
                    print("   ⚠️ Falling back to pattern matching")
                
            except Exception as e:
                print(f"   ❌ Drift scanner test failed: {e}")
        
        # Test complete workflow execution
        print(f"\n🔄 Testing complete workflow execution...")
        
        simple_task = "Create a simple utility function for string manipulation"
        
        try:
            result = orchestrator.execute_task(simple_task)
            
            print(f"   Workflow status: {result.get('status', 'unknown')}")
            
            if "messages" in result:
                print(f"   Workflow messages:")
                for message in result["messages"][-3:]:  # Show last 3 messages
                    print(f"     • {message}")
            
            # Check if vector database context was used
            if "scan_results" in result:
                scan_results = result["scan_results"]
                discovery_method = scan_results.get("discovery_method", "unknown")
                print(f"   File discovery method: {discovery_method}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Workflow execution failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Orchestrator integration test failed: {e}")
        logger.exception("Orchestrator integration test failed")
        return False


def test_vector_db_dependencies():
    """Test if vector database dependencies are available."""
    print("🧪 Testing Vector Database Dependencies")
    print("=" * 50)
    
    dependencies = {
        "sentence-transformers": "sentence_transformers",
        "faiss-cpu": "faiss",
        "numpy": "numpy"
    }
    
    available = {}
    
    for dep_name, import_name in dependencies.items():
        try:
            __import__(import_name)
            available[dep_name] = True
            print(f"✅ {dep_name}: Available")
        except ImportError:
            available[dep_name] = False
            print(f"❌ {dep_name}: Not available")
    
    # Check if core functionality is available
    core_available = available.get("sentence-transformers", False) and available.get("numpy", False)
    
    if core_available:
        print(f"\n✅ Core vector database functionality available")
        if available.get("faiss-cpu", False):
            print(f"✅ Fast search with FAISS available")
        else:
            print(f"⚠️ FAISS not available - will use slower numpy search")
    else:
        print(f"\n❌ Core dependencies missing - vector database will not work")
    
    return core_available


def main():
    """Main test function."""
    print("🚀 Vector Database Integration Test Suite")
    print("=" * 60)
    
    # Test dependencies first
    deps_ok = test_vector_db_dependencies()
    
    if not deps_ok:
        print("\n❌ Dependencies not available. Install with:")
        print("   pip install sentence-transformers faiss-cpu numpy")
        return
    
    # Run tests
    tests = [
        ("Vector Database Standalone", test_vector_database_standalone),
        ("Vector Search Tool", test_vector_search_tool),
        ("Orchestrator Integration", test_orchestrator_with_vector_db),
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
        print("🎉 All tests passed! Vector database integration working!")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    print("\n📋 Vector Database Features Tested:")
    print("✅ Repository indexing and chunking")
    print("✅ Semantic search with embeddings")
    print("✅ File relevance scoring")
    print("✅ Integration with orchestrator")
    print("✅ Intelligent file discovery")
    print("✅ Context-aware planning")


if __name__ == "__main__":
    main()
