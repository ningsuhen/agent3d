#!/usr/bin/env python3
"""
Check Vector Database Dependencies

Quick diagnostic script to check if all dependencies are properly installed.
"""

import sys
from pathlib import Path

def check_dependency(name, import_name, test_func=None):
    """Check if a dependency is available and working."""
    try:
        module = __import__(import_name)
        print(f"✅ {name}: Available")
        
        if test_func:
            try:
                test_func(module)
                print(f"   ✅ {name}: Functional test passed")
            except Exception as e:
                print(f"   ⚠️ {name}: Import OK but test failed: {e}")
        
        return True
    except ImportError as e:
        print(f"❌ {name}: Not available - {e}")
        return False
    except Exception as e:
        print(f"⚠️ {name}: Import error - {e}")
        return False

def test_numpy(numpy_module):
    """Test numpy functionality."""
    arr = numpy_module.array([1, 2, 3])
    assert len(arr) == 3

def test_faiss(faiss_module):
    """Test FAISS functionality."""
    import numpy as np
    # Create a simple index
    d = 64  # dimension
    index = faiss_module.IndexFlatL2(d)
    
    # Add some vectors
    vectors = np.random.random((10, d)).astype('float32')
    index.add(vectors)
    
    # Search
    query = np.random.random((1, d)).astype('float32')
    distances, indices = index.search(query, 3)
    
    assert len(distances[0]) == 3

def test_sentence_transformers(st_module):
    """Test sentence transformers functionality."""
    # Just check if we can create a model (don't actually load it)
    model_name = "all-MiniLM-L6-v2"
    # We won't actually load it to save time, just check the class exists
    assert hasattr(st_module, 'SentenceTransformer')

def main():
    print("🔧 Vector Database Dependencies Check")
    print("=" * 50)
    
    # Core dependencies
    print("\n📦 Core Dependencies:")
    numpy_ok = check_dependency("NumPy", "numpy", test_numpy)
    
    # Vector search dependencies
    print("\n🔍 Vector Search Dependencies:")
    faiss_ok = check_dependency("FAISS", "faiss", test_faiss)
    st_ok = check_dependency("Sentence Transformers", "sentence_transformers", test_sentence_transformers)
    
    # Optional dependencies
    print("\n⚡ Optional Dependencies:")
    torch_ok = check_dependency("PyTorch", "torch")
    transformers_ok = check_dependency("Transformers", "transformers")
    
    # Summary
    print("\n📊 Summary:")
    print(f"   NumPy: {'✅' if numpy_ok else '❌'}")
    print(f"   FAISS: {'✅' if faiss_ok else '❌'}")
    print(f"   Sentence Transformers: {'✅' if st_ok else '❌'}")
    print(f"   PyTorch: {'✅' if torch_ok else '❌'}")
    print(f"   Transformers: {'✅' if transformers_ok else '❌'}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if numpy_ok and faiss_ok and st_ok:
        print("🎉 All core dependencies are working! Vector database with semantic search is ready.")
    elif numpy_ok and faiss_ok:
        print("⚡ Fast vector search available with FAISS, but no semantic embeddings.")
        print("   Install: pip install sentence-transformers")
    elif numpy_ok:
        print("📊 Basic vector operations available, but no fast search or embeddings.")
        print("   Install: pip install faiss-cpu sentence-transformers")
    else:
        print("❌ Core dependencies missing.")
        print("   Install: pip install numpy faiss-cpu sentence-transformers")
    
    # Test our vector database
    print("\n🧪 Testing Our Vector Database:")
    try:
        # Add agents to path
        agents_path = Path(__file__).parent / "agents"
        sys.path.insert(0, str(agents_path))
        
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Test initialization
        vector_db = RepositoryVectorDB()
        print(f"✅ Vector database initialized")
        print(f"   Model available: {vector_db.model is not None}")
        print(f"   FAISS index available: {vector_db.index is not None}")
        
        # Test basic indexing (without embeddings)
        print(f"\n📊 Testing basic indexing...")
        stats = vector_db.index_repository(str(Path.cwd()))
        print(f"✅ Repository indexed:")
        print(f"   Files: {stats['files_processed']}")
        print(f"   Chunks: {stats['chunks_created']}")
        print(f"   Size: {stats['total_size']:,} bytes")
        
        if 'performance' in stats:
            perf = stats['performance']
            print(f"   Time: {perf.get('total_time', 0):.2f}s")
        
    except Exception as e:
        print(f"❌ Vector database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
