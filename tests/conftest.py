#!/usr/bin/env python3
"""
Pytest configuration and fixtures for Agent3D test suite.
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile
import yaml
from unittest.mock import Mock, patch

# Add tools directory to Python path
tools_dir = Path(__file__).parent.parent / 'tools'
sys.path.insert(0, str(tools_dir))

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with basic Agent3D structure."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create basic directory structure
        (temp_path / 'docs').mkdir()
        (temp_path / 'docs' / 'features').mkdir()
        (temp_path / 'tests').mkdir()
        (temp_path / '.agent3d-tmp').mkdir()
        
        # Create minimal config
        config = {
            'project': {
                'name': 'test_project',
                'type': 'test',
                'language': 'python'
            },
            'identifier_patterns': {
                'TC-': {
                    'pattern': 'TC-.*',
                    'primary_files': ['docs/features/*.md'],
                    'reference_files': ['**/*.py']
                },
                'FT-': {
                    'pattern': 'FT-.*',
                    'primary_files': ['docs/features/*.md'],
                    'reference_files': ['**/*.md']
                }
            },
            'project_settings': {
                'python_paths': {
                    'source_directories': ['tools', '.'],
                    'package_structure': {
                        'flat_modules': ['tools'],
                        'nested_modules': []
                    }
                }
            }
        }
        
        with open(temp_path / '.agent3d-config.yml', 'w') as f:
            yaml.dump(config, f)
        
        yield temp_path

@pytest.fixture
def sample_test_cases():
    """Sample test cases for testing."""
    return [
        {
            'tc_id': 'TC-001',
            'title': 'Core Functionality',
            'status': 'complete',
            'execution_type': 'Automated',
            'priority': 'High'
        },
        {
            'tc_id': 'TC-002',
            'title': 'Edge Cases',
            'status': 'pending',
            'execution_type': 'Manual',
            'priority': 'Medium'
        }
    ]

@pytest.fixture
def sample_features():
    """Sample features for testing."""
    return [
        {
            'ft_id': 'FT-001',
            'title': 'Core Feature',
            'description': 'Main functionality',
            'code_location': 'tools/main.py'
        },
        {
            'ft_id': 'FT-002',
            'title': 'Helper Feature',
            'description': 'Supporting functionality',
            'code_location': 'tools/helper.py'
        }
    ]

@pytest.fixture
def mock_drift_analyzer():
    """Mock drift analyzer for testing."""
    with patch('drift_scanner.MultiModeDriftAnalyzer') as mock_class:
        mock_instance = Mock()
        mock_instance.config = {
            'identifier_patterns': {
                'TC-': {'pattern': 'TC-.*'},
                'FT-': {'pattern': 'FT-.*'}
            }
        }
        mock_instance.ddd_root = Path('.')
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test."""
    # Ensure we're in the right directory context
    original_cwd = os.getcwd()
    
    # Change to project root if we're not there
    project_root = Path(__file__).parent.parent
    if project_root.exists():
        os.chdir(project_root)
    
    yield
    
    # Restore original directory
    os.chdir(original_cwd)

# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
