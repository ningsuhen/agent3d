#!/usr/bin/env python3
"""
Test script for vector-enhanced drift analysis

This script demonstrates the enhanced drift analysis capabilities using vector database
for semantic search and intelligent file discovery.
"""

import os
import sys
import logging
import time
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

def test_vector_enhanced_feature_mapping():
    """Test vector-enhanced feature-to-test mapping."""
    logger = setup_logging()
    logger.info("🧪 Testing Vector-Enhanced Feature Mapping")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if not analyzer.vector_db_manager:
            logger.warning("⚠️  Vector database not available, skipping test")
            return False
        
        # Run FT mapping analysis
        logger.info("🔍 Running vector-enhanced FT mapping analysis...")
        start_time = time.time()
        
        ft_report = analyzer._analyze_ft_mapping()
        
        analysis_time = time.time() - start_time
        
        # Display results
        logger.info(f"✅ Analysis completed in {analysis_time:.2f}s")
        logger.info(f"📊 Results:")
        logger.info(f"   - Total features: {ft_report.metadata.get('total_features', 0)}")
        logger.info(f"   - Features with tests: {ft_report.metadata.get('features_with_tests', 0)}")
        logger.info(f"   - Vector enhanced: {ft_report.metadata.get('vector_enhanced', False)}")
        logger.info(f"   - Mapping method: {ft_report.metadata.get('mapping_method', 'unknown')}")
        
        if ft_report.features_without_tests:
            logger.info(f"   - Features without tests: {len(ft_report.features_without_tests)}")
            for feature in ft_report.features_without_tests[:3]:  # Show first 3
                logger.info(f"     • {feature.ft_id}: {feature.title}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector-enhanced feature mapping test failed: {e}")
        return False

def test_vector_enhanced_coverage_analysis():
    """Test vector-enhanced test coverage analysis."""
    logger = setup_logging()
    logger.info("🧪 Testing Vector-Enhanced Coverage Analysis")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if not analyzer.vector_db_manager:
            logger.warning("⚠️  Vector database not available, skipping test")
            return False
        
        # Run coverage analysis
        logger.info("🔍 Running vector-enhanced coverage analysis...")
        start_time = time.time()
        
        coverage_report = analyzer._analyze_code_coverage()
        
        analysis_time = time.time() - start_time
        
        # Display results
        logger.info(f"✅ Analysis completed in {analysis_time:.2f}s")
        logger.info(f"📊 Results:")
        logger.info(f"   - Total source files: {coverage_report.metadata.get('total_source_files', 0)}")
        logger.info(f"   - Total functions: {coverage_report.metadata.get('total_functions', 0)}")
        logger.info(f"   - Coverage percentage: {coverage_report.metadata.get('coverage_percentage', 0):.1f}%")
        logger.info(f"   - Vector enhanced: {coverage_report.metadata.get('vector_enhanced', False)}")
        logger.info(f"   - Analysis method: {coverage_report.metadata.get('analysis_method', 'unknown')}")
        logger.info(f"   - Traditional issues: {coverage_report.metadata.get('traditional_issues', 0)}")
        logger.info(f"   - Vector issues: {coverage_report.metadata.get('vector_issues', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector-enhanced coverage analysis test failed: {e}")
        return False

def test_vector_enhanced_test_quality():
    """Test vector-enhanced test quality analysis."""
    logger = setup_logging()
    logger.info("🧪 Testing Vector-Enhanced Test Quality Analysis")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if not analyzer.vector_db_manager:
            logger.warning("⚠️  Vector database not available, skipping test")
            return False
        
        # Run test quality analysis
        logger.info("🔍 Running vector-enhanced test quality analysis...")
        start_time = time.time()
        
        quality_report = analyzer._analyze_test_quality()
        
        analysis_time = time.time() - start_time
        
        # Display results
        logger.info(f"✅ Analysis completed in {analysis_time:.2f}s")
        logger.info(f"📊 Results:")
        logger.info(f"   - Total test functions: {quality_report.metadata.get('total_test_functions', 0)}")
        logger.info(f"   - Test quality score: {quality_report.metadata.get('test_quality_score', 0):.3f}")
        logger.info(f"   - Traditional score: {quality_report.metadata.get('traditional_score', 0):.3f}")
        logger.info(f"   - Vector score: {quality_report.metadata.get('vector_score', 0):.3f}")
        logger.info(f"   - Vector enhanced: {quality_report.metadata.get('vector_enhanced', False)}")
        logger.info(f"   - Analysis method: {quality_report.metadata.get('analysis_method', 'unknown')}")
        logger.info(f"   - Quality issues: {quality_report.metadata.get('quality_issues_count', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector-enhanced test quality analysis test failed: {e}")
        return False

def test_vector_enhanced_code_location():
    """Test vector-enhanced code location analysis."""
    logger = setup_logging()
    logger.info("🧪 Testing Vector-Enhanced Code Location Analysis")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if not analyzer.vector_db_manager:
            logger.warning("⚠️  Vector database not available, skipping test")
            return False
        
        # Run code location analysis
        logger.info("🔍 Running vector-enhanced code location analysis...")
        start_time = time.time()
        
        location_report = analyzer._analyze_code_location()
        
        analysis_time = time.time() - start_time
        
        # Display results
        logger.info(f"✅ Analysis completed in {analysis_time:.2f}s")
        logger.info(f"📊 Results:")
        logger.info(f"   - Total features: {location_report.metadata.get('total_features', 0)}")
        logger.info(f"   - Features with code location: {location_report.metadata.get('features_with_code_location', 0)}")
        logger.info(f"   - Coverage percentage: {location_report.metadata.get('coverage_percentage', 0):.1f}%")
        logger.info(f"   - Vector enhanced: {location_report.metadata.get('vector_enhanced', False)}")
        logger.info(f"   - Analysis method: {location_report.metadata.get('analysis_method', 'unknown')}")
        logger.info(f"   - Location issues: {location_report.metadata.get('code_location_issues_count', 0)}")
        logger.info(f"   - Vector issues: {location_report.metadata.get('vector_issues', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector-enhanced code location analysis test failed: {e}")
        return False

def test_comprehensive_vector_analysis():
    """Test comprehensive vector-enhanced drift analysis."""
    logger = setup_logging()
    logger.info("🧪 Testing Comprehensive Vector-Enhanced Analysis")
    
    try:
        from drift_scanner import MultiModeDriftAnalyzer
        
        # Initialize analyzer with vector database enabled
        analyzer = MultiModeDriftAnalyzer(
            root_dir='.',
            enable_vector_db=True
        )
        
        if not analyzer.vector_db_manager:
            logger.warning("⚠️  Vector database not available, skipping test")
            return False
        
        # Run comprehensive analysis
        logger.info("🔍 Running comprehensive vector-enhanced analysis...")
        start_time = time.time()
        
        all_report = analyzer._analyze_all_modes()
        
        analysis_time = time.time() - start_time
        
        # Display results
        logger.info(f"✅ Comprehensive analysis completed in {analysis_time:.2f}s")
        logger.info(f"📊 Summary:")
        
        # Check which analyses were vector-enhanced
        vector_enhanced_analyses = []
        if all_report.metadata.get('vector_enhanced'):
            vector_enhanced_analyses.append("Overall")
        
        logger.info(f"   - Vector-enhanced analyses: {', '.join(vector_enhanced_analyses) if vector_enhanced_analyses else 'None'}")
        logger.info(f"   - Total test cases: {all_report.metadata.get('total_test_cases', 0)}")
        logger.info(f"   - Total test functions: {all_report.metadata.get('total_test_functions', 0)}")
        logger.info(f"   - Coverage percentage: {all_report.metadata.get('coverage_percentage', 0):.1f}%")
        logger.info(f"   - Test quality score: {all_report.metadata.get('test_quality_score', 0):.3f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Comprehensive vector-enhanced analysis test failed: {e}")
        return False

def main():
    """Run all vector-enhanced drift analysis tests."""
    logger = setup_logging()
    logger.info("🚀 Starting Vector-Enhanced Drift Analysis Tests")
    
    tests = [
        ("Vector-Enhanced Feature Mapping", test_vector_enhanced_feature_mapping),
        ("Vector-Enhanced Coverage Analysis", test_vector_enhanced_coverage_analysis),
        ("Vector-Enhanced Test Quality", test_vector_enhanced_test_quality),
        ("Vector-Enhanced Code Location", test_vector_enhanced_code_location),
        ("Comprehensive Vector Analysis", test_comprehensive_vector_analysis),
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
        logger.info("🎉 All vector-enhanced drift analysis tests passed!")
        return 0
    else:
        logger.error("💥 Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    exit(main())
