"""
Integration tests for the drift scanner module.
"""
import pytest
from pathlib import Path
import sys
import os

# Add tools directory to Python path
tools_dir = Path(__file__).parent.parent / 'tools'
sys.path.insert(0, str(tools_dir))

# Import after modifying path
from drift_scanner import MultiModeDriftAnalyzer

class TestDriftScannerIntegration:
    """Integration tests for the drift scanner."""
    
    @pytest.fixture
    def sample_project(self, tmp_path):
        """Create a sample project structure for testing."""
        # Create project structure
        (tmp_path / 'docs' / 'features').mkdir(parents=True)
        (tmp_path / 'src').mkdir()
        (tmp_path / 'tests').mkdir()
        
        # Create sample feature file
        feature_content = """
        # Feature: Test Feature
        
        ## FT-TEST-001 Sample Feature
        
        **Description:** This is a test feature.
        
        **Acceptance Criteria:**
        - [ ] TC-TEST-001: Should work correctly
        - [ ] TC-TEST-002: Should handle errors
        """
        (tmp_path / 'docs' / 'features' / 'test_feature.md').write_text(feature_content)
        
        # Create sample source file
        source_content = """
        def test_function():
            """
            This function is referenced by TC-TEST-001.
            """
            return "test"
            
        # TC-TEST-002: This is a test case reference in code
        def another_function():
            pass
        """
        (tmp_path / 'src' / 'test_module.py').write_text(source_content)
        
        # Create sample test file
        test_content = """
        import pytest
        
        def test_tc_test_001():
            """Test case TC-TEST-001"""
            from src.test_module import test_function
            assert test_function() == "test"
            
        def test_tc_test_002():
            """Test case TC-TEST-002"""
            from src.test_module import another_function
            another_function()
            assert True
        """
        (tmp_path / 'tests' / 'test_module_test.py').write_text(test_content)
        
        return tmp_path
    
    def test_tc_scan_basic_workflow(self, sample_project, tmp_path):
        """TC-IMPL-001: Test basic TC scanning workflow."""
        # Initialize analyzer
        analyzer = MultiModeDriftAnalyzer()
        
        # Run TC scan
        results = analyzer.analyze_drift(
            root_dir=str(sample_project),
            mode='tc-mapping',
            output_dir=str(tmp_path / 'output')
        )
        
        # Verify results
        assert results is not None
        assert 'tc_mapping' in results
        assert 'TC-TEST-001' in results['tc_mapping']
        assert 'TC-TEST-002' in results['tc_mapping']
        
        # Verify test case references
        tc1_refs = results['tc_mapping']['TC-TEST-001']['references']
        tc2_refs = results['tc_mapping']['TC-TEST-002']['references']
        
        assert any('test_module.py' in ref['file'] for ref in tc1_refs)
        assert any('test_module_test.py' in ref['file'] for ref in tc1_refs)
        assert any('test_module.py' in ref['file'] for ref in tc2_refs)
    
    def test_ft_scan_basic_workflow(self, sample_project, tmp_path):
        """TC-IMPL-002: Test basic FT scanning workflow."""
        # Initialize analyzer
        analyzer = MultiModeDriftAnalyzer()
        
        # Run FT scan
        results = analyzer.analyze_drift(
            root_dir=str(sample_project),
            mode='ft-mapping',
            output_dir=str(tmp_path / 'output')
        )
        
        # Verify results
        assert results is not None
        assert 'ft_mapping' in results
        assert 'FT-TEST-001' in results['ft_mapping']
        
        # Verify feature references
        ft_refs = results['ft_mapping']['FT-TEST-001']['references']
        assert any('test_feature.md' in ref['file'] for ref in ft_refs)
    
    def test_reverse_drift_detection(self, sample_project, tmp_path):
        """TC-IMPL-020: Test reverse drift detection."""
        # Initialize analyzer
        analyzer = MultiModeDriftAnalyzer()
        
        # Run reverse drift scan
        results = analyzer.analyze_drift(
            root_dir=str(sample_project),
            mode='reverse',
            output_dir=str(tmp_path / 'output')
        )
        
        # Verify results
        assert results is not None
        assert 'undocumented_implementation' in results
        
        # In our test case, there should be no undocumented implementations
        # since we've documented everything in the test setup
        assert len(results['undocumented_implementation']) == 0
