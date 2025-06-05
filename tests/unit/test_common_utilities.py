"""
Unit tests for common_utilities.py module.
"""
import pytest
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, mock_open

# Import the module to test
from tools.common_utilities import (
    FileInfo,
    FileSystemUtils,
    YamlUtils,
    LanguageDetector,
    PatternMatcher,
    StringUtils,
    ValidationUtils
)

class TestFileSystemUtils:
    """Tests for FileSystemUtils class."""
    
    def test_safe_read_file_exists(self, tmp_path):
        """Test reading an existing file."""
        test_file = tmp_path / "test.txt"
        test_content = "test content"
        test_file.write_text(test_content)
        
        content = FileSystemUtils.safe_read_file(test_file)
        assert content == test_content
    
    def test_safe_read_file_not_exists(self):
        """Test reading a non-existent file returns None."""
        non_existent = Path("/non/existent/file.txt")
        content = FileSystemUtils.safe_read_file(non_existent)
        assert content is None
    
    def test_safe_write_file(self, tmp_path):
        """Test writing content to a file."""
        test_file = tmp_path / "output.txt"
        test_content = "test output"
        
        result = FileSystemUtils.safe_write_file(test_file, test_content)
        assert result is True
        assert test_file.read_text() == test_content
    
    def test_find_files_by_patterns(self, tmp_path):
        """Test finding files by patterns."""
        # Create test files
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir2").mkdir()
        (tmp_path / "dir1" / "test1.py").touch()
        (tmp_path / "dir2" / "test2.py").touch()
        (tmp_path / "test3.txt").touch()
        
        # Find Python files
        patterns = ["**/*.py"]
        files = FileSystemUtils.find_files_by_patterns(tmp_path, patterns)
        assert len(files) == 2
        assert any("test1.py" in str(f) for f in files)
        assert any("test2.py" in str(f) for f in files)


class TestYamlUtils:
    """Tests for YamlUtils class."""
    
    def test_safe_load_yaml_valid(self, tmp_path):
        """Test loading valid YAML."""
        yaml_content = """
        key1: value1
        key2:
          - item1
          - item2
        """
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)
        
        data = YamlUtils.safe_load_yaml(yaml_file)
        assert data["key1"] == "value1"
        assert data["key2"] == ["item1", "item2"]
    
    def test_safe_load_yaml_invalid(self, tmp_path):
        """Test loading invalid YAML returns None."""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("key: [missing bracket")
        
        data = YamlUtils.safe_load_yaml(yaml_file)
        assert data is None


class TestLanguageDetector:
    """Tests for LanguageDetector class."""
    
    @pytest.mark.parametrize("ext,expected", [
        (".py", "python"),
        (".js", "javascript"),
        (".ts", "javascript"),
        (".yaml", "yaml"),
        (".md", "markdown"),
        (".unknown", None)
    ])
    def test_detect_language(self, ext, expected):
        """Test language detection by file extension."""
        file_path = Path(f"test{ext}")
        assert LanguageDetector.detect_language(file_path) == expected
    
    @pytest.mark.parametrize("path,expected", [
        ("test_test.py", True),
        ("test_spec.py", True),
        ("test.py", False),
        ("test_test.txt", False)
    ])
    def test_is_test_file(self, path, expected):
        """Test test file detection."""
        assert LanguageDetector.is_test_file(Path(path)) == expected


class TestPatternMatcher:
    """Tests for PatternMatcher class."""
    
    def test_find_patterns_in_text(self):
        """Test finding patterns in text."""
        text = "TC-123 and TC-456 are test cases"
        pattern = r"TC-\d+"
        
        matches = PatternMatcher.find_patterns_in_text(text, pattern)
        assert len(matches) == 2
        assert "TC-123" in matches
        assert "TC-456" in matches
    
    def test_find_pattern_positions(self):
        """Test finding pattern positions."""
        text = "TC-123 and TC-456"
        pattern = r"TC-\d+"
        
        matches = PatternMatcher.find_pattern_positions(text, pattern)
        assert len(matches) == 2
        assert matches[0][0] == "TC-123"
        assert matches[0][1] == 0
        assert matches[1][0] == "TC-456"
        assert matches[1][1] == 10


class TestStringUtils:
    """Tests for StringUtils class."""
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "  test   string  with  extra  spaces  "
        expected = "test string with extra spaces"
        assert StringUtils.normalize_whitespace(text) == expected
    
    def test_extract_identifier_from_text(self):
        """Test identifier extraction."""
        text = "This is TC-123 and FT-456"
        assert StringUtils.extract_identifier_from_text(text, "TC-") == ["TC-123"]
        assert StringUtils.extract_identifier_from_text(text, "FT-") == ["FT-456"]
    
    def test_clean_filename(self):
        """Test filename cleaning."""
        assert StringUtils.clean_filename("test:file/name?.txt") == "test_file_name_.txt"


class TestValidationUtils:
    """Tests for ValidationUtils class."""
    
    def test_validate_required_fields(self):
        """Test required field validation."""
        data = {"name": "test", "value": 123}
        assert ValidationUtils.validate_required_fields(data, ["name", "value"]) is True
        
        with pytest.raises(ValueError):
            ValidationUtils.validate_required_fields(data, ["name", "missing"])
    
    def test_validate_yaml_file(self, tmp_path):
        """Test YAML file validation."""
        # Valid YAML
        valid_file = tmp_path / "valid.yaml"
        valid_file.write_text("key: value")
        assert ValidationUtils.validate_yaml_file(valid_file) is True
        
        # Invalid YAML
        invalid_file = tmp_path / "invalid.yaml"
        invalid_file.write_text("key: [missing bracket")
        assert ValidationUtils.validate_yaml_file(invalid_file) is False
