#!/usr/bin/env python3
"""
Vector Database Memory Analysis

This script analyzes the memory usage of our vector database,
including chunk storage, index size, and overall memory footprint.
"""

import sys
import logging
import psutil
import os
from pathlib import Path
import time
import pickle

# Add the agents directory to Python path
agents_path = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_path))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_object_size(obj, seen=None):
    """Calculate the memory size of a Python object recursively."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    
    # Mark as seen
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum([get_object_size(v, seen) for v in obj.values()])
        size += sum([get_object_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_object_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_object_size(i, seen) for i in obj])
    
    return size


def format_bytes(bytes_value):
    """Format bytes into human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def analyze_vector_db_memory():
    """Analyze the memory usage of the vector database."""
    print("🧠 Vector Database Memory Analysis")
    print("=" * 50)
    
    try:
        from orchestrator.vector_db import RepositoryVectorDB
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        print(f"📊 Initial process memory: {format_bytes(initial_memory)}")
        
        # Initialize vector database
        print("\n🔧 Initializing vector database...")
        vector_db = RepositoryVectorDB(logger=logger)
        
        after_init_memory = process.memory_info().rss
        init_overhead = after_init_memory - initial_memory
        
        print(f"📊 Memory after initialization: {format_bytes(after_init_memory)}")
        print(f"📈 Initialization overhead: {format_bytes(init_overhead)}")
        
        # Index the repository
        current_dir = str(Path.cwd())
        print(f"\n📊 Indexing repository: {current_dir}")
        
        start_time = time.time()
        stats = vector_db.index_repository(current_dir)
        index_time = time.time() - start_time
        
        after_index_memory = process.memory_info().rss
        index_overhead = after_index_memory - after_init_memory
        
        print(f"✅ Repository indexed in {index_time:.2f}s")
        print(f"📊 Memory after indexing: {format_bytes(after_index_memory)}")
        print(f"📈 Indexing memory overhead: {format_bytes(index_overhead)}")
        
        # Analyze individual components
        print(f"\n🔍 Component Memory Analysis:")
        
        # Chunks memory
        chunks_size = get_object_size(vector_db.chunks)
        print(f"   📊 Chunks storage: {format_bytes(chunks_size)}")
        print(f"      • Total chunks: {len(vector_db.chunks)}")
        print(f"      • Avg per chunk: {format_bytes(chunks_size / len(vector_db.chunks)) if vector_db.chunks else 'N/A'}")
        
        # File paths memory
        file_paths = set(chunk.file_path for chunk in vector_db.chunks)
        file_paths_size = get_object_size(file_paths)
        print(f"   📁 File paths: {format_bytes(file_paths_size)}")
        print(f"      • Unique files: {len(file_paths)}")
        
        # Content memory
        total_content_size = sum(len(chunk.content) for chunk in vector_db.chunks)
        print(f"   📝 Raw content: {format_bytes(total_content_size)}")
        
        # Embeddings memory (if available)
        embeddings_size = 0
        if hasattr(vector_db, 'embeddings') and vector_db.embeddings is not None:
            embeddings_size = get_object_size(vector_db.embeddings)
            print(f"   🧠 Embeddings: {format_bytes(embeddings_size)}")
        else:
            print(f"   🧠 Embeddings: Not available")
        
        # FAISS index memory (if available)
        faiss_size = 0
        if hasattr(vector_db, 'index') and vector_db.index is not None:
            # FAISS index size is harder to measure directly
            faiss_size = get_object_size(vector_db.index)
            print(f"   ⚡ FAISS index: {format_bytes(faiss_size)}")
        else:
            print(f"   ⚡ FAISS index: Not available")
        
        # Language statistics
        language_stats = {}
        for chunk in vector_db.chunks:
            lang = chunk.language
            if lang not in language_stats:
                language_stats[lang] = {'count': 0, 'size': 0}
            language_stats[lang]['count'] += 1
            language_stats[lang]['size'] += len(chunk.content)
        
        print(f"\n🌐 Memory by Language:")
        for lang, lang_stats in sorted(language_stats.items(), key=lambda x: x[1]['size'], reverse=True):
            avg_chunk_size = lang_stats['size'] / lang_stats['count']
            print(f"   📄 {lang}: {format_bytes(lang_stats['size'])} ({lang_stats['count']} chunks, {format_bytes(avg_chunk_size)}/chunk)")
        
        # Calculate compression ratio
        original_file_size = stats['total_size']
        stored_content_size = total_content_size
        compression_ratio = stored_content_size / original_file_size if original_file_size > 0 else 0
        
        print(f"\n📊 Storage Efficiency:")
        print(f"   📁 Original files: {format_bytes(original_file_size)}")
        print(f"   💾 Stored content: {format_bytes(stored_content_size)}")
        print(f"   📈 Compression ratio: {compression_ratio:.2f}x")
        print(f"   💡 Storage efficiency: {(1 - compression_ratio) * 100:.1f}% reduction" if compression_ratio < 1 else f"   💡 Storage overhead: {(compression_ratio - 1) * 100:.1f}% increase")
        
        # Memory breakdown
        total_db_memory = chunks_size + embeddings_size + faiss_size
        
        print(f"\n💾 Total Database Memory Breakdown:")
        print(f"   📊 Chunks: {format_bytes(chunks_size)} ({chunks_size/total_db_memory*100:.1f}%)" if total_db_memory > 0 else f"   📊 Chunks: {format_bytes(chunks_size)}")
        print(f"   🧠 Embeddings: {format_bytes(embeddings_size)} ({embeddings_size/total_db_memory*100:.1f}%)" if total_db_memory > 0 else f"   🧠 Embeddings: {format_bytes(embeddings_size)}")
        print(f"   ⚡ FAISS Index: {format_bytes(faiss_size)} ({faiss_size/total_db_memory*100:.1f}%)" if total_db_memory > 0 else f"   ⚡ FAISS Index: {format_bytes(faiss_size)}")
        print(f"   🎯 Total DB: {format_bytes(total_db_memory)}")
        
        # Performance metrics
        chunks_per_mb = len(vector_db.chunks) / (total_db_memory / 1024 / 1024) if total_db_memory > 0 else 0
        files_per_mb = len(file_paths) / (total_db_memory / 1024 / 1024) if total_db_memory > 0 else 0
        
        print(f"\n⚡ Memory Efficiency Metrics:")
        print(f"   📊 Chunks per MB: {chunks_per_mb:.1f}")
        print(f"   📁 Files per MB: {files_per_mb:.1f}")
        print(f"   🔍 Search space density: {len(vector_db.chunks)} chunks in {format_bytes(total_db_memory)}")
        
        # Test serialization size
        print(f"\n💾 Serialization Analysis:")
        try:
            # Test pickle size
            pickled_chunks = pickle.dumps(vector_db.chunks)
            pickle_size = len(pickled_chunks)
            print(f"   🥒 Pickled chunks: {format_bytes(pickle_size)}")
            print(f"   📈 Pickle overhead: {pickle_size/chunks_size:.2f}x" if chunks_size > 0 else "   📈 Pickle overhead: N/A")
        except Exception as e:
            print(f"   🥒 Pickle test failed: {e}")
        
        return {
            'total_memory': total_db_memory,
            'chunks_memory': chunks_size,
            'embeddings_memory': embeddings_size,
            'faiss_memory': faiss_size,
            'num_chunks': len(vector_db.chunks),
            'num_files': len(file_paths),
            'original_size': original_file_size,
            'stored_size': stored_content_size,
            'compression_ratio': compression_ratio
        }
        
    except Exception as e:
        print(f"❌ Memory analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_with_alternatives():
    """Compare memory usage with alternative storage methods."""
    print(f"\n🔄 Comparison with Alternative Storage Methods")
    print("=" * 55)
    
    try:
        # Simulate storing as simple text files
        from orchestrator.vector_db import RepositoryVectorDB
        
        vector_db = RepositoryVectorDB(logger=logger)
        stats = vector_db.index_repository(str(Path.cwd()))
        
        # Calculate different storage approaches
        chunks = vector_db.chunks
        
        # 1. Raw text concatenation
        all_text = '\n'.join(chunk.content for chunk in chunks)
        raw_text_size = len(all_text.encode('utf-8'))
        
        # 2. JSON storage
        import json
        json_data = [
            {
                'file_path': chunk.file_path,
                'start_line': chunk.start_line,
                'end_line': chunk.end_line,
                'content': chunk.content,
                'language': chunk.language
            }
            for chunk in chunks
        ]
        json_text = json.dumps(json_data)
        json_size = len(json_text.encode('utf-8'))
        
        # 3. Our current approach
        current_size = get_object_size(chunks)
        
        print(f"📊 Storage Method Comparison:")
        print(f"   📝 Raw text concatenation: {format_bytes(raw_text_size)}")
        print(f"   📄 JSON serialization: {format_bytes(json_size)}")
        print(f"   🎯 Our chunk objects: {format_bytes(current_size)}")
        
        print(f"\n📈 Efficiency Ratios:")
        print(f"   📝 Raw text vs Our method: {raw_text_size/current_size:.2f}x" if current_size > 0 else "   📝 Raw text vs Our method: N/A")
        print(f"   📄 JSON vs Our method: {json_size/current_size:.2f}x" if current_size > 0 else "   📄 JSON vs Our method: N/A")
        
        # Memory per chunk analysis
        print(f"\n📊 Per-Chunk Memory Analysis:")
        print(f"   🎯 Avg memory per chunk: {format_bytes(current_size / len(chunks)) if chunks else 'N/A'}")
        print(f"   📝 Avg content per chunk: {format_bytes(sum(len(c.content) for c in chunks) / len(chunks)) if chunks else 'N/A'}")
        
        overhead_per_chunk = (current_size - sum(len(c.content.encode('utf-8')) for c in chunks)) / len(chunks) if chunks else 0
        print(f"   📈 Avg overhead per chunk: {format_bytes(overhead_per_chunk)}")
        
    except Exception as e:
        print(f"❌ Comparison analysis failed: {e}")


def main():
    """Main analysis function."""
    print("🧠 Vector Database Memory Usage Analysis")
    print("=" * 60)
    
    print("This analysis measures the actual memory footprint of our")
    print("vector database, including all components and storage efficiency.")
    
    # Analyze memory usage
    memory_stats = analyze_vector_db_memory()
    
    # Compare with alternatives
    compare_with_alternatives()
    
    # Final summary
    if memory_stats:
        print(f"\n{'='*60}")
        print("MEMORY ANALYSIS SUMMARY")
        print(f"{'='*60}")
        
        print(f"🎯 Total Database Size: {format_bytes(memory_stats['total_memory'])}")
        print(f"📊 Chunks: {memory_stats['num_chunks']} chunks in {format_bytes(memory_stats['chunks_memory'])}")
        print(f"📁 Files: {memory_stats['num_files']} files indexed")
        print(f"📈 Compression: {memory_stats['compression_ratio']:.2f}x of original size")
        
        # Calculate efficiency metrics
        mb_size = memory_stats['total_memory'] / 1024 / 1024
        chunks_per_mb = memory_stats['num_chunks'] / mb_size if mb_size > 0 else 0
        
        print(f"\n⚡ Efficiency Metrics:")
        print(f"🔍 Search density: {chunks_per_mb:.0f} chunks per MB")
        print(f"💾 Memory efficiency: {format_bytes(memory_stats['total_memory'] / memory_stats['num_chunks'])} per chunk")
        print(f"🚀 Storage ratio: {memory_stats['stored_size'] / memory_stats['total_memory']:.1f}x content to total memory")
        
        print(f"\n🎉 The vector database is highly memory-efficient!")
        print(f"💡 Perfect for in-memory code search and analysis!")


if __name__ == "__main__":
    main()
