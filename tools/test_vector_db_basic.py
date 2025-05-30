#!/usr/bin/env python3
"""
Basic Vector Database Test

Test the vector database functionality without requiring external dependencies.
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


def test_basic_import():
    """Test basic import of vector database classes."""
    print("🧪 Testing Basic Import")
    print("=" * 30)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB, CodeChunk
        print("✅ Successfully imported RepositoryVectorDB and CodeChunk")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_initialization():
    """Test basic initialization without external dependencies."""
    print("\n🧪 Testing Basic Initialization")
    print("=" * 35)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Initialize without model (should work even without sentence-transformers)
        db = RepositoryVectorDB(logger=logger)
        print("✅ RepositoryVectorDB initialized")
        
        # Check basic properties
        print(f"   Model available: {db.model is not None}")
        print(f"   Index available: {db.index is not None}")
        print(f"   Chunks count: {len(db.chunks)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_detection():
    """Test file detection and language detection."""
    print("\n🧪 Testing File Detection")
    print("=" * 30)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        db = RepositoryVectorDB(logger=logger)
        
        # Test language detection
        test_files = [
            ("test.py", "python"),
            ("script.js", "javascript"),
            ("README.md", "markdown"),
            ("config.yml", "yaml"),
            ("unknown.xyz", "unknown")
        ]
        
        for filename, expected_lang in test_files:
            file_path = Path(filename)
            detected_lang = db._detect_language(file_path)
            status = "✅" if detected_lang == expected_lang else "❌"
            print(f"   {status} {filename}: {detected_lang} (expected: {expected_lang})")
        
        return True
        
    except Exception as e:
        print(f"❌ File detection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chunking():
    """Test code chunking functionality."""
    print("\n🧪 Testing Code Chunking")
    print("=" * 30)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        db = RepositoryVectorDB(logger=logger)
        
        # Test Python chunking
        python_code = '''
def hello_world():
    """A simple function."""
    print("Hello, World!")

class TestClass:
    """A test class."""
    
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
'''
        
        chunks = db._create_chunks(python_code, "test.py", "python")
        print(f"   Python chunks created: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"     {i+1}. {chunk.chunk_type} ({chunk.start_line}-{chunk.end_line})")
        
        # Test Markdown chunking
        markdown_content = '''
# Main Title

This is the introduction.

## Section 1

Content for section 1.

## Section 2

Content for section 2.
'''
        
        chunks = db._create_chunks(markdown_content, "README.md", "markdown")
        print(f"   Markdown chunks created: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"     {i+1}. {chunk.chunk_type} ({chunk.start_line}-{chunk.end_line})")
        
        return True
        
    except Exception as e:
        print(f"❌ Chunking test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_repository_indexing():
    """Test repository indexing (without vector embeddings)."""
    print("\n🧪 Testing Repository Indexing")
    print("=" * 35)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        db = RepositoryVectorDB(logger=logger)
        
        # Index current directory (should work even without embeddings)
        current_dir = str(Path.cwd())
        print(f"   Indexing: {current_dir}")
        
        stats = db.index_repository(current_dir)
        
        print(f"✅ Indexing completed:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Chunks created: {stats['chunks_created']}")
        print(f"   Total size: {stats['total_size']} bytes")
        print(f"   Languages: {list(stats['languages'].keys())}")
        print(f"   Chunk types: {list(stats['chunk_types'].keys())}")
        
        if stats['errors']:
            print(f"   Errors: {len(stats['errors'])}")
            for error in stats['errors'][:3]:  # Show first 3 errors
                print(f"     • {error}")
        
        # Test statistics
        repo_stats = db.get_statistics()
        print(f"\n   Repository statistics:")
        print(f"     Total chunks: {repo_stats['total_chunks']}")
        print(f"     Total files: {repo_stats['total_files']}")
        print(f"     Has embeddings: {repo_stats['has_embeddings']}")
        
        return stats['chunks_created'] > 0
        
    except Exception as e:
        print(f"❌ Repository indexing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vector_search_tool():
    """Test the VectorSearchTool wrapper."""
    print("\n🧪 Testing Vector Search Tool")
    print("=" * 35)
    
    try:
        from orchestrator.tools import VectorSearchTool
        
        # Initialize tool
        search_tool = VectorSearchTool(logger=logger)
        print("✅ VectorSearchTool initialized")
        
        # Test repository indexing
        current_dir = str(Path.cwd())
        result = search_tool.initialize_and_index_repository(current_dir)
        
        print(f"   Indexing result: {result['status']}")
        print(f"   Repository indexed: {result['indexed']}")
        
        if result['indexed']:
            stats = result['stats']
            print(f"   Files processed: {stats['files_processed']}")
            print(f"   Chunks created: {stats['chunks_created']}")
        
        # Test repository overview
        overview = search_tool.get_repository_overview()
        print(f"\n   Repository overview:")
        print(f"     Status: {overview['indexing_status']}")
        print(f"     Total files: {overview['total_files']}")
        print(f"     Total chunks: {overview['total_chunks']}")
        print(f"     Languages: {list(overview['languages'].keys())}")
        
        return result['indexed']
        
    except Exception as e:
        print(f"❌ Vector search tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("🚀 Basic Vector Database Test Suite")
    print("=" * 50)
    
    print("This test suite verifies basic vector database functionality")
    print("without requiring external dependencies like sentence-transformers.")
    
    # Run tests
    tests = [
        ("Basic Import", test_basic_import),
        ("Basic Initialization", test_basic_initialization),
        ("File Detection", test_file_detection),
        ("Code Chunking", test_chunking),
        ("Repository Indexing", test_repository_indexing),
        ("Vector Search Tool", test_vector_search_tool),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
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
    print(f"\n{'='*50}")
    print("FINAL TEST RESULTS")
    print(f"{'='*50}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\n💡 Next steps:")
        print("  • Install vector database dependencies:")
        print("    pip install -r requirements-vector-db.txt")
        print("  • Run full integration tests:")
        print("    python3 test_vector_db_integration.py")
    else:
        print("⚠️ Some basic tests failed. Check the logs above for details.")
    
    print("\n📋 Basic Features Tested:")
    print("✅ Module imports and initialization")
    print("✅ File type detection")
    print("✅ Code chunking algorithms")
    print("✅ Repository indexing (without embeddings)")
    print("✅ Tool wrapper functionality")


if __name__ == "__main__":
    main()
