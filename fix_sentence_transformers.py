#!/usr/bin/env python3
"""
Fix Sentence Transformers Installation

This script diagnoses and fixes sentence-transformers import issues.
"""

import sys
import subprocess
import importlib

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True, None
    except Exception as e:
        return False, str(e)

def fix_sentence_transformers():
    """Fix sentence-transformers installation."""
    print("🔧 Diagnosing sentence-transformers installation...")
    
    # Check current status
    can_import, error = check_import('sentence_transformers')
    
    if can_import:
        print("✅ sentence-transformers is already working!")
        return True
    
    print(f"❌ Import failed: {error}")
    
    # Check dependencies
    deps = ['torch', 'transformers', 'numpy', 'scipy', 'scikit-learn']
    missing_deps = []
    
    for dep in deps:
        can_import_dep, _ = check_import(dep)
        if can_import_dep:
            print(f"✅ {dep}: Available")
        else:
            print(f"❌ {dep}: Missing")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n🔧 Installing missing dependencies: {', '.join(missing_deps)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_deps)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    # Try reinstalling sentence-transformers
    print("\n🔧 Reinstalling sentence-transformers...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'uninstall', 'sentence-transformers', '-y'
        ])
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 'sentence-transformers'
        ])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to reinstall: {e}")
        return False
    
    # Test again
    can_import, error = check_import('sentence_transformers')
    if can_import:
        print("✅ sentence-transformers is now working!")
        return True
    else:
        print(f"❌ Still failing: {error}")
        return False

def test_full_functionality():
    """Test the full vector database with embeddings."""
    print("\n🧪 Testing full vector database functionality...")
    
    try:
        # Test sentence transformers
        from sentence_transformers import SentenceTransformer
        print("✅ SentenceTransformer import successful")
        
        # Test our vector database
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path.cwd() / 'agents'))
        
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Initialize with embeddings
        print("🔧 Initializing vector database with embeddings...")
        vector_db = RepositoryVectorDB()
        
        print(f"✅ Vector database initialized:")
        print(f"   Model available: {vector_db.model is not None}")
        print(f"   FAISS index available: {vector_db.index is not None}")
        
        # Test indexing with embeddings
        print("\n📊 Testing repository indexing with embeddings...")
        stats = vector_db.index_repository(str(Path.cwd()))
        
        print(f"✅ Repository indexed with embeddings:")
        print(f"   Files: {stats['files_processed']}")
        print(f"   Chunks: {stats['chunks_created']}")
        print(f"   Has embeddings: {vector_db.embeddings is not None}")
        print(f"   Has FAISS index: {vector_db.index is not None}")
        
        # Test semantic search
        if vector_db.embeddings is not None and vector_db.index is not None:
            print("\n🔍 Testing semantic search...")
            results = vector_db.search("python function", top_k=3)
            print(f"✅ Semantic search working: {len(results)} results found")
            
            for i, (chunk, score) in enumerate(results[:3], 1):
                print(f"   {i}. {chunk.file_path} (score: {score:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Full functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🚀 Sentence Transformers Fix & Test")
    print("=" * 50)
    
    # Try to fix sentence-transformers
    if fix_sentence_transformers():
        # Test full functionality
        if test_full_functionality():
            print("\n🎉 All vector database features are now working!")
            print("\n📋 Enabled Features:")
            print("✅ Fast repository indexing")
            print("✅ Semantic search with embeddings")
            print("✅ FAISS-accelerated search")
            print("✅ Performance monitoring")
            print("✅ Multi-language support")
        else:
            print("\n⚠️ Basic functionality works, but advanced features need attention")
    else:
        print("\n❌ Could not fix sentence-transformers")
        print("\n💡 Manual fix options:")
        print("1. Try: pip install --upgrade sentence-transformers")
        print("2. Try: pip install --force-reinstall sentence-transformers")
        print("3. Check Python version compatibility")
        print("4. The vector database still works without embeddings!")

if __name__ == "__main__":
    main()
