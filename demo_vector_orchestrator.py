#!/usr/bin/env python3
"""
Demo: Vector Database Enhanced Orchestrator

This script demonstrates the enhanced orchestrator with vector database
capabilities for intelligent code search and context-aware planning.
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


def demo_vector_search():
    """Demonstrate vector search capabilities."""
    print("🔍 Vector Search Demo")
    print("=" * 40)
    
    try:
        from orchestrator.tools import VectorSearchTool
        
        # Initialize vector search
        search_tool = VectorSearchTool(logger=logger)
        result = search_tool.initialize_and_index_repository(str(Path.cwd()))
        
        if not result["indexed"]:
            print("❌ Failed to index repository")
            return
        
        print(f"✅ Repository indexed: {result['stats']['chunks_created']} chunks")
        
        # Demo queries
        queries = [
            "Python class definition",
            "test function",
            "orchestrator workflow",
            "vector database search",
            "file processing logic"
        ]
        
        for query in queries:
            print(f"\n🔍 Query: '{query}'")
            files = search_tool.find_relevant_files(query, max_files=3)
            
            for i, file_info in enumerate(files, 1):
                score = file_info["relevance_score"]
                path = file_info["file_path"]
                print(f"  {i}. {path} (score: {score:.3f})")
        
        # Repository overview
        overview = search_tool.get_repository_overview()
        print(f"\n📊 Repository Overview:")
        print(f"  Files: {overview['total_files']}")
        print(f"  Chunks: {overview['total_chunks']}")
        print(f"  Languages: {', '.join(overview['languages'].keys())}")
        
    except Exception as e:
        print(f"❌ Vector search demo failed: {e}")


def demo_intelligent_orchestrator():
    """Demonstrate the intelligent orchestrator."""
    print("\n🤖 Intelligent Orchestrator Demo")
    print("=" * 40)
    
    try:
        from orchestrator.langgraph_orchestrator import Agent3DOrchestratorGraph
        
        # Create orchestrator
        orchestrator = Agent3DOrchestratorGraph(
            logger=logger,
            max_iterations=1,
            enable_swebench=False  # Disable for demo
        )
        
        # Check vector database status
        if orchestrator.vector_search_tool.is_indexed:
            print("✅ Vector database integrated and ready")
        else:
            print("⚠️ Vector database not available")
            return
        
        # Demo tasks
        demo_tasks = [
            "Create a new utility function for data processing",
            "Add unit tests for the vector database functionality", 
            "Update the README with vector search documentation",
            "Refactor the orchestrator to improve performance"
        ]
        
        for task in demo_tasks:
            print(f"\n🎯 Task: {task}")
            print("-" * 50)
            
            # Analyze task
            ddd_analysis = orchestrator.ddd_tool.analyze_task(task)
            print(f"  Task type: {ddd_analysis['primary_type']}")
            print(f"  Complexity: {ddd_analysis['complexity']}")
            
            # Run intelligent file discovery
            scan_results = orchestrator._run_drift_scanner(task, ddd_analysis)
            
            discovery_method = scan_results.get("discovery_method", "unknown")
            files = scan_results.get("files_to_modify", [])
            
            print(f"  Discovery: {discovery_method}")
            print(f"  Files found: {len(files)}")
            
            # Show top files with relevance scores
            if "relevance_scores" in scan_results:
                scores = scan_results["relevance_scores"]
                print("  Top relevant files:")
                for file_path in files[:3]:
                    score = scores.get(file_path, 0)
                    print(f"    • {file_path} (relevance: {score:.3f})")
            else:
                print("  Files to modify:")
                for file_path in files[:3]:
                    print(f"    • {file_path}")
        
    except Exception as e:
        print(f"❌ Orchestrator demo failed: {e}")


def demo_file_context_analysis():
    """Demonstrate file context analysis."""
    print("\n📁 File Context Analysis Demo")
    print("=" * 40)
    
    try:
        from orchestrator.tools import VectorSearchTool
        
        search_tool = VectorSearchTool(logger=logger)
        search_tool.initialize_and_index_repository(str(Path.cwd()))
        
        if not search_tool.is_indexed:
            print("❌ Repository not indexed")
            return
        
        # Find some Python files to analyze
        python_files = []
        for file_path in Path.cwd().rglob("*.py"):
            if "test_" not in file_path.name and "__pycache__" not in str(file_path):
                python_files.append(str(file_path.relative_to(Path.cwd())))
                if len(python_files) >= 3:
                    break
        
        for file_path in python_files:
            print(f"\n📄 Analyzing: {file_path}")
            context = search_tool.get_file_context(file_path)
            
            if "error" in context:
                print(f"  ❌ {context['error']}")
                continue
            
            print(f"  Language: {context['language']}")
            print(f"  Chunks: {context['total_chunks']}")
            print(f"  Lines: {context['total_lines']}")
            print(f"  Complexity: {context['complexity_score']}")
            
            structure = context['structure']
            print(f"  Structure: {structure['functions']} functions, {structure['classes']} classes")
            
            features = context['features']
            feature_list = []
            if features['has_imports']:
                feature_list.append("imports")
            if features['has_tests']:
                feature_list.append("tests")
            if features['has_classes']:
                feature_list.append("classes")
            if features['has_functions']:
                feature_list.append("functions")
            
            print(f"  Features: {', '.join(feature_list)}")
        
    except Exception as e:
        print(f"❌ File context demo failed: {e}")


def demo_similar_code_search():
    """Demonstrate similar code search."""
    print("\n🔎 Similar Code Search Demo")
    print("=" * 40)
    
    try:
        from orchestrator.tools import VectorSearchTool
        
        search_tool = VectorSearchTool(logger=logger)
        search_tool.initialize_and_index_repository(str(Path.cwd()))
        
        if not search_tool.is_indexed:
            print("❌ Repository not indexed")
            return
        
        # Search for similar implementations
        search_queries = [
            "function that processes files",
            "class initialization method",
            "error handling with try-except",
            "logging and debug output",
            "configuration and setup"
        ]
        
        for query in search_queries:
            print(f"\n🔍 Finding: {query}")
            similar = search_tool.find_similar_implementations(query, top_k=2)
            
            for impl in similar:
                score = impl["similarity_score"]
                path = impl["file_path"]
                lines = impl["lines"]
                print(f"  • {path}:{lines} (similarity: {score:.3f})")
                
                # Show a preview of the code
                preview = impl["content_preview"]
                if preview:
                    # Show first line of preview
                    first_line = preview.split('\n')[0]
                    print(f"    Preview: {first_line[:60]}...")
        
    except Exception as e:
        print(f"❌ Similar code search demo failed: {e}")


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔧 Checking Dependencies")
    print("=" * 30)
    
    required = ["sentence_transformers", "numpy"]
    optional = ["faiss"]
    
    all_good = True
    
    for dep in required:
        try:
            __import__(dep)
            print(f"✅ {dep}: Available")
        except ImportError:
            print(f"❌ {dep}: Missing (required)")
            all_good = False
    
    for dep in optional:
        try:
            __import__(dep)
            print(f"✅ {dep}: Available (fast search enabled)")
        except ImportError:
            print(f"⚠️ {dep}: Missing (will use slower search)")
    
    if not all_good:
        print(f"\n❌ Missing required dependencies. Install with:")
        print(f"   pip install -r requirements-vector-db.txt")
        return False
    
    return True


def main():
    """Main demo function."""
    print("🚀 Vector Database Enhanced Orchestrator Demo")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print(f"\n🎯 This demo showcases:")
    print(f"  • Intelligent repository indexing")
    print(f"  • Semantic code search")
    print(f"  • Context-aware file discovery")
    print(f"  • Enhanced orchestrator planning")
    
    # Run demos
    demos = [
        demo_vector_search,
        demo_file_context_analysis,
        demo_similar_code_search,
        demo_intelligent_orchestrator
    ]
    
    for demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            print(f"\n⏹️ Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            logger.exception("Demo failed")
    
    print(f"\n🎉 Demo completed!")
    print(f"\n💡 Key Benefits:")
    print(f"  • Finds relevant files automatically")
    print(f"  • Understands code context and structure")
    print(f"  • Provides intelligent task planning")
    print(f"  • Reduces manual file selection")
    print(f"  • Improves orchestrator accuracy")


if __name__ == "__main__":
    main()
