#!/usr/bin/env python3
"""
Common utilities for Agent3D tools.
Extracted from drift_scanner.py to eliminate code duplication.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class FileInfo:
    """Information about a file."""
    path: Path
    language: Optional[str]
    content: Optional[str] = None


class FileSystemUtils:
    """Common file system operations."""
    
    @staticmethod
    def safe_read_file(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
        """Safely read a file and return its content."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None
    
    @staticmethod
    def safe_write_file(file_path: Path, content: str, encoding: str = 'utf-8') -> bool:
        """Safely write content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    
    @staticmethod
    def find_files_by_patterns(root_dir: Path, patterns: List[str]) -> List[Path]:
        """Find files matching any of the given patterns."""
        files = []
        for pattern in patterns:
            files.extend(root_dir.glob(pattern))
        return [f for f in files if f.is_file()]


class YamlUtils:
    """Common YAML operations."""
    
    @staticmethod
    def safe_load_yaml(file_path: Path) -> Optional[Dict]:
        """Safely load YAML file and return parsed content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading YAML from {file_path}: {e}")
            return None
    
    @staticmethod
    def safe_dump_yaml(data: Any, file_path: Path) -> bool:
        """Safely dump data to YAML file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"❌ Error writing YAML to {file_path}: {e}")
            return False
    
    @staticmethod
    def validate_yaml_syntax(file_path: Path) -> bool:
        """Validate YAML syntax without loading content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            return True
        except Exception:
            return False


class LanguageDetector:
    """Language detection utilities."""
    
    LANGUAGE_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'javascript',
        '.jsx': 'javascript',
        '.tsx': 'javascript',
        '.java': 'java',
        '.rs': 'rust',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.md': 'markdown',
        '.json': 'json'
    }
    
    @classmethod
    def detect_language(cls, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        suffix = file_path.suffix.lower()
        return cls.LANGUAGE_EXTENSIONS.get(suffix)
    
    @classmethod
    def is_test_file(cls, file_path: Path) -> bool:
        """Check if a file is likely a test file."""
        name = file_path.name.lower()
        return (
            name.startswith('test_') or
            name.endswith('_test.py') or
            'test' in file_path.parts or
            name.endswith('Test.java') or
            name.endswith('Tests.java')
        )
    
    @classmethod
    def is_source_file(cls, file_path: Path) -> bool:
        """Check if a file is a source code file."""
        language = cls.detect_language(file_path)
        return language in ['python', 'javascript', 'java', 'rust']


class PatternMatcher:
    """Common pattern matching utilities."""
    
    @staticmethod
    def find_patterns_in_text(text: str, pattern: str, flags: int = 0) -> List[str]:
        """Find all matches of a pattern in text."""
        try:
            return re.findall(pattern, text, flags)
        except re.error as e:
            print(f"❌ Invalid regex pattern '{pattern}': {e}")
            return []
    
    @staticmethod
    def find_pattern_positions(text: str, pattern: str) -> List[Tuple[int, str]]:
        """Find all pattern matches with their positions."""
        try:
            matches = []
            for match in re.finditer(pattern, text):
                matches.append((match.start(), match.group()))
            return matches
        except re.error as e:
            print(f"❌ Invalid regex pattern '{pattern}': {e}")
            return []
    
    @staticmethod
    def get_line_number(text: str, position: int) -> int:
        """Get line number for a position in text."""
        return text[:position].count('\n') + 1
    
    @staticmethod
    def extract_text_around_position(text: str, position: int, range_size: int = 1000) -> str:
        """Extract text around a specific position."""
        start = max(0, position - range_size // 2)
        end = min(len(text), position + range_size)
        return text[start:end]


class ConfigurationLoader:
    """Common configuration loading utilities."""
    
    @staticmethod
    def load_agent3d_config(root_dir: Path) -> Dict:
        """Load Agent3D configuration with fallback to defaults."""
        config_file = root_dir / '.agent3d-config.yml'
        
        if config_file.exists():
            config = YamlUtils.safe_load_yaml(config_file)
            if config:
                print(f"✅ Loaded configuration from {config_file}")
                return config
        
        print(f"⚠️  Configuration file not found at {config_file}")
        print("   Using default configuration")
        return ConfigurationLoader.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict:
        """Get default Agent3D configuration."""
        return {
            'identifier_patterns': {
                'TC-': {
                    'name': 'Test Case',
                    'pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
                    'flexible_pattern': r'TC-[A-Za-z0-9-]+',
                    'primary_files': ['docs/TEST-CASES.md', 'TEST-CASES.md'],
                    'relationship_targets': ['FT-*', 'REQ-*']
                },
                'FT-': {
                    'name': 'Feature',
                    'pattern': r'FT-[A-Z]+-\d+[a-z]?',
                    'flexible_pattern': r'FT-[A-Za-z0-9-]+',
                    'primary_files': ['docs/FEATURES.md', 'FEATURES.md'],
                    'relationship_targets': ['TC-*', 'REQ-*']
                },
                'REQ-': {
                    'name': 'Requirement',
                    'pattern': r'REQ-[A-Z0-9]+-\d+[a-z]?',
                    'flexible_pattern': r'REQ-[A-Za-z0-9-]+',
                    'primary_files': ['docs/REQUIREMENTS.md', 'REQUIREMENTS.md'],
                    'relationship_targets': ['TC-*', 'FT-*']
                }
            },
            'drift_detection': {
                'enabled_patterns': ['TC-', 'FT-', 'REQ-'],
                'primary_patterns': ['TC-', 'FT-', 'REQ-'],
                'relationship_validation': True
            }
        }


class LoggingUtils:
    """Common logging utilities."""
    
    @staticmethod
    def log_analysis_start(mode: str, root_dir: str, log_file: str) -> None:
        """Log the start of an analysis session."""
        try:
            with open(log_file, 'w') as f:
                f.write(f"=== Agent3D Analysis Session ===\n")
                f.write(f"Timestamp: {os.popen('date').read().strip()}\n")
                f.write(f"Mode: {mode}\n")
                f.write(f"Root Directory: {root_dir}\n")
                f.write(f"Log File: {log_file}\n")
                f.write(f"{'='*50}\n\n")
        except Exception as e:
            print(f"❌ Error writing to log file {log_file}: {e}")
    
    @staticmethod
    def create_log_directory(root_dir: Path) -> Path:
        """Create and return the log directory path."""
        log_dir = root_dir / '.agent3d-tmp' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir


class ValidationUtils:
    """Common validation utilities."""
    
    @staticmethod
    def validate_file_exists(file_path: Path) -> bool:
        """Validate that a file exists."""
        return file_path.exists() and file_path.is_file()
    
    @staticmethod
    def validate_directory_exists(dir_path: Path) -> bool:
        """Validate that a directory exists."""
        return dir_path.exists() and dir_path.is_dir()
    
    @staticmethod
    def validate_yaml_file(file_path: Path) -> bool:
        """Validate that a file exists and has valid YAML syntax."""
        if not ValidationUtils.validate_file_exists(file_path):
            return False
        return YamlUtils.validate_yaml_syntax(file_path)
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
        """Validate that all required fields are present in data."""
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        return missing_fields


class StringUtils:
    """Common string manipulation utilities."""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text."""
        return ' '.join(text.split())
    
    @staticmethod
    def extract_identifier_from_text(text: str, prefix: str) -> List[str]:
        """Extract identifiers with a specific prefix from text."""
        pattern = f'{prefix}[A-Za-z0-9-]+'
        return PatternMatcher.find_patterns_in_text(text, pattern)
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """Clean a filename for safe file system usage."""
        # Remove or replace invalid characters
        cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove multiple underscores
        cleaned = re.sub(r'_+', '_', cleaned)
        # Remove leading/trailing underscores
        return cleaned.strip('_')


# Export commonly used utilities
__all__ = [
    'FileInfo',
    'FileSystemUtils',
    'YamlUtils', 
    'LanguageDetector',
    'PatternMatcher',
    'ConfigurationLoader',
    'LoggingUtils',
    'ValidationUtils',
    'StringUtils'
]
