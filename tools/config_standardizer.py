#!/usr/bin/env python3
"""
Configuration Standardizer for Agent3D Framework
Standardizes YAML configuration files for consistency and maintainability.
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import common utilities
try:
    from tools.common_utilities import YamlUtils, FileSystemUtils, LoggingUtils
except ImportError:
    # Fallback to direct imports
    import logging

    class YamlUtils:
        @staticmethod
        def load_yaml(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        @staticmethod
        def save_yaml(data, file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2, allow_unicode=True, sort_keys=False)

    class FileSystemUtils:
        @staticmethod
        def find_files_by_pattern(directory, pattern):
            return list(Path(directory).glob(pattern))

    class LoggingUtils:
        @staticmethod
        def setup_logger(name):
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            return logger

class ConfigurationStandardizer:
    """Standardizes YAML configuration files across the Agent3D framework."""
    
    def __init__(self, root_directory: str = "."):
        """Initialize the configuration standardizer."""
        self.root_directory = Path(root_directory)
        self.logger = LoggingUtils.setup_logger("config_standardizer")
        self.yaml_utils = YamlUtils()
        self.fs_utils = FileSystemUtils()
        
        # Standard metadata format
        self.standard_metadata_fields = [
            "name", "type", "version", "purpose", "created", 
            "last_updated", "refactoring_version", "configuration_version", "features"
        ]
        
        # Common configuration blocks
        self.common_blocks = self._load_common_patterns()
    
    def _load_common_patterns(self) -> Dict[str, Any]:
        """Load common patterns from common-patterns.yml."""
        try:
            patterns_file = self.root_directory / "procedures.yml" / "common-patterns.yml"
            if patterns_file.exists():
                return self.yaml_utils.load_yaml(patterns_file)
            return {}
        except Exception as e:
            self.logger.warning(f"Could not load common patterns: {e}")
            return {}
    
    def standardize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize metadata format according to common patterns."""
        standardized = {}
        
        # Process fields in standard order
        for field in self.standard_metadata_fields:
            if field in metadata:
                standardized[field] = metadata[field]
        
        # Add any additional fields not in standard list
        for key, value in metadata.items():
            if key not in standardized:
                standardized[key] = value
        
        # Ensure required fields have appropriate defaults
        if "type" not in standardized:
            standardized["type"] = "configuration"
        
        if "last_updated" not in standardized:
            standardized["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        if "configuration_version" not in standardized:
            standardized["configuration_version"] = "1.0.0"
        
        return standardized
    
    def standardize_indentation(self, file_path: Path) -> bool:
        """Standardize YAML indentation to 2 spaces."""
        try:
            # Read the file
            content = file_path.read_text(encoding='utf-8')
            
            # Load and dump with standard formatting
            data = yaml.safe_load(content)
            
            # Write back with standard 2-space indentation
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2, 
                         allow_unicode=True, sort_keys=False)
            
            self.logger.info(f"Standardized indentation for {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to standardize indentation for {file_path}: {e}")
            return False
    
    def consolidate_common_blocks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate common configuration blocks."""
        # Add references to common patterns where applicable
        if "validation" in data and isinstance(data["validation"], dict):
            # Check if validation follows common patterns
            common_validation = self.common_blocks.get("validation_rules", {}).get("universal_requirements", {})
            if common_validation:
                data["validation"]["inherits_from"] = "common-patterns.yml#validation_rules.universal_requirements"
        
        if "quality_gates" in data and isinstance(data["quality_gates"], list):
            # Add reference to common quality gates
            data["quality_gates_reference"] = "common-patterns.yml#quality_gates.universal_gates"
        
        return data
    
    def standardize_file(self, file_path: Path) -> bool:
        """Standardize a single YAML file."""
        try:
            self.logger.info(f"Standardizing {file_path}")
            
            # Load the YAML file
            data = self.yaml_utils.load_yaml(file_path)
            
            # Standardize metadata if present
            if "metadata" in data:
                data["metadata"] = self.standardize_metadata(data["metadata"])
            
            # Consolidate common blocks
            data = self.consolidate_common_blocks(data)
            
            # Save the standardized file
            self.yaml_utils.save_yaml(data, file_path)
            
            # Standardize indentation
            self.standardize_indentation(file_path)
            
            self.logger.info(f"Successfully standardized {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to standardize {file_path}: {e}")
            return False
    
    def find_yaml_files(self, directories: List[str] = None) -> List[Path]:
        """Find all YAML files in specified directories."""
        if directories is None:
            directories = ["passes.yml", "procedures.yml", "templates", "rules.yml"]
        
        yaml_files = []
        for directory in directories:
            dir_path = self.root_directory / directory
            if dir_path.exists():
                yaml_files.extend(self.fs_utils.find_files_by_pattern(dir_path, "*.yml"))
                yaml_files.extend(self.fs_utils.find_files_by_pattern(dir_path, "*.yaml"))
        
        return yaml_files
    
    def standardize_all(self, directories: List[str] = None) -> Dict[str, Any]:
        """Standardize all YAML files in specified directories."""
        yaml_files = self.find_yaml_files(directories)
        
        results = {
            "total_files": len(yaml_files),
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for file_path in yaml_files:
            if self.standardize_file(file_path):
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(str(file_path))
        
        return results
    
    def validate_standardization(self, file_path: Path) -> Dict[str, Any]:
        """Validate that a file follows standardization rules."""
        validation_results = {
            "file": str(file_path),
            "valid": True,
            "issues": []
        }
        
        try:
            data = self.yaml_utils.load_yaml(file_path)
            
            # Check metadata format
            if "metadata" in data:
                metadata = data["metadata"]
                
                # Check required fields
                required_fields = ["name", "type", "version", "purpose"]
                for field in required_fields:
                    if field not in metadata:
                        validation_results["issues"].append(f"Missing required metadata field: {field}")
                        validation_results["valid"] = False
                
                # Check field ordering
                actual_order = list(metadata.keys())
                expected_order = [f for f in self.standard_metadata_fields if f in actual_order]
                if actual_order[:len(expected_order)] != expected_order:
                    validation_results["issues"].append("Metadata fields not in standard order")
                    validation_results["valid"] = False
            
            # Check indentation (basic check)
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip() and line.startswith(' '):
                    # Check if indentation is multiple of 2
                    leading_spaces = len(line) - len(line.lstrip(' '))
                    if leading_spaces % 2 != 0:
                        validation_results["issues"].append(f"Line {i}: Non-standard indentation (not multiple of 2)")
                        validation_results["valid"] = False
                        break
        
        except Exception as e:
            validation_results["valid"] = False
            validation_results["issues"].append(f"Failed to validate: {e}")
        
        return validation_results

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Standardize YAML configuration files")
    parser.add_argument("--directory", "-d", default=".", help="Root directory to process")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate standardization only")
    parser.add_argument("--file", "-f", help="Process single file")
    parser.add_argument("--directories", nargs="+", help="Specific directories to process")
    
    args = parser.parse_args()
    
    standardizer = ConfigurationStandardizer(args.directory)
    
    if args.file:
        # Process single file
        file_path = Path(args.file)
        if args.validate:
            result = standardizer.validate_standardization(file_path)
            print(f"Validation result for {file_path}:")
            print(f"Valid: {result['valid']}")
            if result['issues']:
                print("Issues:")
                for issue in result['issues']:
                    print(f"  - {issue}")
        else:
            success = standardizer.standardize_file(file_path)
            print(f"Standardization {'successful' if success else 'failed'} for {file_path}")
    
    else:
        # Process all files
        if args.validate:
            yaml_files = standardizer.find_yaml_files(args.directories)
            for file_path in yaml_files:
                result = standardizer.validate_standardization(file_path)
                if not result['valid']:
                    print(f"❌ {file_path}: {', '.join(result['issues'])}")
                else:
                    print(f"✅ {file_path}: Valid")
        else:
            results = standardizer.standardize_all(args.directories)
            print(f"Standardization complete:")
            print(f"  Total files: {results['total_files']}")
            print(f"  Successful: {results['successful']}")
            print(f"  Failed: {results['failed']}")
            if results['errors']:
                print("  Errors:")
                for error in results['errors']:
                    print(f"    - {error}")

if __name__ == "__main__":
    main()
