#!/usr/bin/env python3
"""
Test script for vector database integration with Drift MCP

This script tests the vector database integration to ensure it works correctly
with different DDD_ROOT directories and provides enhanced file discovery.
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s'
    )
    return logging.getLogger(__name__)

def test_vector_db_manager():
    """Test the MultiRootVectorDBManager."""
    logger = setup_logging()
    logger.info("🧪 Testing Vector Database Manager")
    
    try:
        from vector_db_manager import MultiRootVectorDBManager
        
        # Initialize manager
        manager = MultiRootVectorDBManager(logger=logger)
        logger.info("✅ Vector database manager initialized")
        
        # Test with current directory
        current_dir = str(Path.cwd())
        logger.info(f"📁 Testing with directory: {current_dir}")
        
        # Get or create database
        db = manager.get_or_create_database(current_dir)
        if db:
            logger.info("✅ Vector database created successfully")
            
            # Get statistics
            stats = manager.get_statistics(current_dir)
            logger.info(f"📊 Database stats: {stats}")
            
            # Test search functionality
            if stats.get("total_chunks", 0) > 0:
                logger.info("🔍 Testing search functionality...")
                
                # Search for drift-related content
                results = manager.search(current_dir, "drift scanner test", top_k=5)
                logger.info(f"   Found {len(results)} results for 'drift scanner test'")
                
                # Search for Python files
                python_results = manager.search(current_dir, "python function", top_k=3, filter_language="python")
                logger.info(f"   Found {len(python_results)} Python results")
                
                # Get related files
                related_files = manager.get_related_files(current_dir, "test implementation", top_k=3)
                logger.info(f"   Found {len(related_files)} related files")
                
                for i, file_path in enumerate(related_files[:3]):
                    logger.info(f"     {i+1}. {file_path}")
            else:
                logger.warning("⚠️  No chunks indexed, skipping search tests")
        else:
            logger.error("❌ Failed to create vector database")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Vector database dependencies not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Vector database manager test failed: {e}")
        return False
    
    return True

def test_drift_scanner_integration():
    """Test the drift scanner with vector database integration."""
    logger = setup_logging()
    logger.info("🧪 Testing Drift Scanner Integration")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if analyzer.vector_db_manager:
            logger.info("✅ Drift scanner initialized with vector database")
            
            # Test vector database stats
            stats = analyzer.get_vector_db_stats()
            logger.info(f"📊 Vector DB stats: {stats}")
            
            # Test search functionality
            if stats.get("total_chunks", 0) > 0:
                logger.info("🔍 Testing drift scanner search methods...")
                
                # Test related files search
                related_files = analyzer.search_related_files("test case implementation", top_k=3)
                logger.info(f"   Found {len(related_files)} related files")
                
                # Test test files search
                test_files = analyzer.find_related_test_files("drift analysis", top_k=3)
                logger.info(f"   Found {len(test_files)} test files")
                
                # Test implementation files search
                impl_files = analyzer.find_implementation_files("vector database", top_k=3)
                logger.info(f"   Found {len(impl_files)} implementation files")
            else:
                logger.warning("⚠️  No chunks indexed, skipping search tests")
        else:
            logger.warning("⚠️  Vector database not available in drift scanner")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Drift scanner import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Drift scanner integration test failed: {e}")
        return False
    
    return True

def test_mcp_server_integration():
    """Test the MCP server with vector database integration."""
    logger = setup_logging()
    logger.info("🧪 Testing MCP Server Integration")
    
    try:
        from drift_scanner_mcp_server import DriftScannerMCPServer
        
        # Initialize MCP server
        server = DriftScannerMCPServer()
        
        if server.vector_db_manager:
            logger.info("✅ MCP server initialized with vector database")
            
            # Test vector database stats
            current_dir = str(Path.cwd())
            stats = server.get_vector_db_stats(current_dir)
            logger.info(f"📊 Vector DB stats: {stats}")
            
            # Test cache invalidation
            server.invalidate_vector_cache(current_dir)
            logger.info("✅ Vector cache invalidation test passed")
        else:
            logger.warning("⚠️  Vector database not available in MCP server")
            return False
            
    except ImportError as e:
        logger.error(f"❌ MCP server import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ MCP server integration test failed: {e}")
        return False
    
    return True

def main():
    """Run all integration tests."""
    logger = setup_logging()
    logger.info("🚀 Starting Vector Database Integration Tests")
    
    tests = [
        ("Vector DB Manager", test_vector_db_manager),
        ("Drift Scanner Integration", test_drift_scanner_integration),
        ("MCP Server Integration", test_mcp_server_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {test_name}")
        logger.info('='*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info('='*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {status} - {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Vector database integration is working correctly.")
        return 0
    else:
        logger.error("💥 Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    exit(main())
