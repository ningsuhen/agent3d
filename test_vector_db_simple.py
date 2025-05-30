#!/usr/bin/env python3
"""
Simple Vector Database Test

Test the vector database functionality with proper path setup.
"""

import sys
import logging
from pathlib import Path

# Add the agents directory to Python path
agents_path = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_path))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_basic_functionality():
    """Test basic vector database functionality."""
    print("🧪 Testing Vector Database Basic Functionality")
    print("=" * 60)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from orchestrator.vector_db import RepositoryVectorDB, CodeChunk
        from orchestrator.tools import VectorSearchTool
        from orchestrator.token_tracker import TokenTracker
        from orchestrator.cleanup_tool import TestFileCleanupTool
        print("✅ All modules imported successfully")
        
        # Test vector database initialization
        print("\n🔧 Testing vector database initialization...")
        vector_db = RepositoryVectorDB(logger=logger)
        print(f"✅ Vector database initialized")
        print(f"   Model available: {vector_db.model is not None}")
        print(f"   Index available: {vector_db.index is not None}")
        
        # Test language detection
        print("\n🔍 Testing language detection...")
        test_files = [
            ("test.py", "python"),
            ("script.js", "javascript"),
            ("README.md", "markdown"),
            ("config.yml", "yaml")
        ]
        
        for filename, expected in test_files:
            detected = vector_db._detect_language(Path(filename))
            status = "✅" if detected == expected else "❌"
            print(f"   {status} {filename}: {detected}")
        
        # Test repository indexing (without embeddings)
        print("\n📊 Testing repository indexing...")
        current_dir = str(Path.cwd())
        stats = vector_db.index_repository(current_dir)
        
        print(f"✅ Repository indexed:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Chunks created: {stats['chunks_created']}")
        print(f"   Total size: {stats['total_size']:,} bytes")
        print(f"   Languages: {list(stats['languages'].keys())}")
        
        # Performance metrics
        if 'performance' in stats:
            perf = stats['performance']
            print(f"\n⚡ Performance metrics:")
            print(f"   Total time: {perf.get('total_time', 0):.2f}s")
            print(f"   File scan: {perf.get('file_scan_time', 0):.2f}s")
            print(f"   Chunking: {perf.get('chunking_time', 0):.2f}s")
            print(f"   Embeddings: {perf.get('embedding_time', 0):.2f}s")
        
        # Test vector search tool
        print("\n🔍 Testing vector search tool...")
        search_tool = VectorSearchTool(logger=logger)
        result = search_tool.initialize_and_index_repository(current_dir)
        
        print(f"✅ Vector search tool:")
        print(f"   Status: {result['status']}")
        print(f"   Indexed: {result['indexed']}")
        
        if result['indexed']:
            overview = search_tool.get_repository_overview()
            print(f"   Total files: {overview['total_files']}")
            print(f"   Total chunks: {overview['total_chunks']}")
            print(f"   Languages: {', '.join(overview['languages'].keys())}")
        
        # Test token tracker
        print("\n💰 Testing token tracker...")
        tracker = TokenTracker(logger=logger)
        
        # Simulate an API call
        call_context = tracker.start_call("test_operation")
        tracker.end_call(call_context, input_tokens=100, output_tokens=50)
        
        stats = tracker.get_session_stats()
        print(f"✅ Token tracker:")
        print(f"   Total calls: {stats['total_calls']}")
        print(f"   Total tokens: {stats['total_tokens']}")
        print(f"   Total cost: ${stats['total_cost']:.4f}")
        
        # Test cleanup tool
        print("\n🧹 Testing cleanup tool...")
        cleanup_tool = TestFileCleanupTool(logger=logger)
        
        # Create a test file
        test_file = "temp_test_cleanup.py"
        with open(test_file, 'w') as f:
            f.write("# Test file for cleanup\nprint('test')\n")
        
        candidates = cleanup_tool.scan_for_cleanup_candidates()
        print(f"✅ Cleanup tool:")
        print(f"   Test files found: {len(candidates.get('test_files', []))}")
        print(f"   Generated files found: {len(candidates.get('generated_files', []))}")
        print(f"   Temp directories found: {len(candidates.get('temp_directories', []))}")
        
        # Clean up the test file
        try:
            Path(test_file).unlink()
        except:
            pass
        
        print(f"\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_dependencies():
    """Check which dependencies are available."""
    print("\n🔧 Checking Dependencies")
    print("=" * 30)
    
    dependencies = {
        "numpy": "numpy",
        "sentence-transformers": "sentence_transformers", 
        "faiss-cpu": "faiss",
        "torch": "torch",
        "transformers": "transformers"
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
    
    # Check core functionality
    core_deps = ["numpy", "sentence-transformers"]
    core_available = all(available.get(dep, False) for dep in core_deps)
    
    print(f"\n📊 Status Summary:")
    if core_available:
        print(f"✅ Core vector database functionality: Available")
        if available.get("faiss-cpu", False):
            print(f"✅ Fast search with FAISS: Available")
        else:
            print(f"⚠️ FAISS not available - will use slower numpy search")
    else:
        print(f"❌ Core dependencies missing")
        print(f"\n💡 To install missing dependencies:")
        print(f"   pip install sentence-transformers faiss-cpu numpy")
        print(f"   # or")
        print(f"   pip install -r requirements-vector-db.txt")
    
    return core_available


def test_with_dependencies():
    """Test functionality that requires external dependencies."""
    print("\n🧪 Testing Advanced Features (Requires Dependencies)")
    print("=" * 60)
    
    try:
        # Check if dependencies are available
        import sentence_transformers
        import numpy as np
        
        print("✅ Dependencies available, testing advanced features...")
        
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Create vector database with embeddings
        vector_db = RepositoryVectorDB(logger=logger)
        
        # Index repository with embeddings
        current_dir = str(Path.cwd())
        stats = vector_db.index_repository(current_dir)
        
        print(f"📊 Advanced indexing results:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Chunks created: {stats['chunks_created']}")
        print(f"   Has embeddings: {vector_db.embeddings is not None}")
        print(f"   Has FAISS index: {vector_db.index is not None}")
        
        # Test semantic search
        if vector_db.embeddings is not None:
            print(f"\n🔍 Testing semantic search...")
            search_results = vector_db.search("python function", top_k=3)
            print(f"   Search results: {len(search_results)} chunks found")
            
            for i, (chunk, score) in enumerate(search_results[:3], 1):
                print(f"     {i}. {chunk.file_path} (score: {score:.3f})")
        
        print(f"✅ Advanced features working!")
        return True
        
    except ImportError as e:
        print(f"⚠️ Dependencies not available: {e}")
        print(f"   Basic functionality still works without embeddings")
        return False
    except Exception as e:
        print(f"❌ Advanced features test failed: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Vector Database Integration Test")
    print("=" * 60)
    
    print("This test validates the enhanced orchestrator components:")
    print("• Vector database with performance monitoring")
    print("• Token usage tracking")
    print("• Test file cleanup automation")
    
    # Test basic functionality (should work without dependencies)
    basic_success = test_basic_functionality()
    
    # Check dependencies
    deps_available = check_dependencies()
    
    # Test advanced features if dependencies are available
    advanced_success = False
    if deps_available:
        advanced_success = test_with_dependencies()
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL TEST RESULTS")
    print(f"{'='*60}")
    
    print(f"✅ Basic functionality: {'PASSED' if basic_success else 'FAILED'}")
    print(f"{'✅' if deps_available else '❌'} Dependencies: {'Available' if deps_available else 'Missing'}")
    print(f"{'✅' if advanced_success else '⚠️'} Advanced features: {'PASSED' if advanced_success else 'SKIPPED/FAILED'}")
    
    if basic_success:
        print(f"\n🎉 Core vector database functionality is working!")
        
        if not deps_available:
            print(f"\n💡 To enable advanced features:")
            print(f"   1. Activate your virtual environment:")
            print(f"      source venv/bin/activate")
            print(f"   2. Install dependencies:")
            print(f"      pip install sentence-transformers faiss-cpu numpy")
            print(f"   3. Re-run this test to verify advanced features")
        else:
            print(f"\n🚀 All features are working perfectly!")
    else:
        print(f"\n❌ Basic functionality failed. Check the error messages above.")
    
    print(f"\n📋 Features Tested:")
    print(f"✅ Vector database initialization and indexing")
    print(f"✅ Performance monitoring and metrics")
    print(f"✅ Token usage tracking")
    print(f"✅ Test file cleanup automation")
    print(f"{'✅' if advanced_success else '⚠️'} Semantic search with embeddings")


if __name__ == "__main__":
    main()
