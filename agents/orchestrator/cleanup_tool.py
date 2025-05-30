"""
Test File Cleanup Tool

This module provides functionality to clean up test files and temporary
artifacts created during orchestrator execution.
"""

import os
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Set
import re


class TestFileCleanupTool:
    """Tool for cleaning up test files and temporary artifacts."""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        
        # Patterns for test files and temporary artifacts
        self.test_patterns = [
            # Test files
            r"test_.*\.py$",
            r".*_test\.py$",
            r".*\.test\.py$",
            
            # Example files
            r"example_.*\.py$",
            r".*_example\.py$",
            r"demo_.*\.py$",
            r".*_demo\.py$",
            
            # Temporary files
            r"temp_.*\.py$",
            r".*_temp\.py$",
            r"tmp_.*\.py$",
            r".*_tmp\.py$",
            
            # Generated files
            r"generated_.*\.py$",
            r".*_generated\.py$",
            r"output_.*\.py$",
            r".*_output\.py$",
            
            # Sample files
            r"sample_.*\.py$",
            r".*_sample\.py$",
            
            # Backup files
            r".*\.bak$",
            r".*\.backup$",
            r".*~$",
            
            # Other temporary extensions
            r".*\.tmp$",
            r".*\.temp$"
        ]
        
        # Directories to clean
        self.temp_directories = [
            ".agent3d-tmp",
            "__pycache__",
            ".pytest_cache",
            "temp",
            "tmp",
            "examples/temp",
            "test_output"
        ]
        
        # Files to preserve (even if they match patterns)
        self.preserve_files = {
            "test_vector_db_basic.py",
            "test_vector_db_integration.py", 
            "test_ddd_execution_plan_integration.py",
            "demo_vector_orchestrator.py"
        }
    
    def scan_for_cleanup_candidates(self, root_path: str = None) -> Dict[str, Any]:
        """Scan for files and directories that can be cleaned up.
        
        Args:
            root_path: Root directory to scan (defaults to current directory)
            
        Returns:
            Dictionary with cleanup candidates
        """
        if root_path is None:
            root_path = str(Path.cwd())
        
        root_path = Path(root_path)
        
        self.logger.info(f"🔍 Scanning for cleanup candidates in: {root_path}")
        
        candidates = {
            "test_files": [],
            "temp_directories": [],
            "backup_files": [],
            "generated_files": [],
            "total_size": 0,
            "scan_time": time.time()
        }
        
        # Compile regex patterns
        compiled_patterns = [re.compile(pattern) for pattern in self.test_patterns]
        
        # Scan files
        for file_path in root_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(root_path)
                file_name = file_path.name
                
                # Skip preserved files
                if file_name in self.preserve_files:
                    continue
                
                # Check if file matches any pattern
                for pattern in compiled_patterns:
                    if pattern.match(file_name):
                        try:
                            file_size = file_path.stat().st_size
                            file_info = {
                                "path": str(relative_path),
                                "full_path": str(file_path),
                                "size": file_size,
                                "modified": file_path.stat().st_mtime,
                                "pattern_matched": pattern.pattern
                            }
                            
                            # Categorize the file
                            if "test" in pattern.pattern:
                                candidates["test_files"].append(file_info)
                            elif any(x in pattern.pattern for x in ["bak", "backup", "~"]):
                                candidates["backup_files"].append(file_info)
                            elif any(x in pattern.pattern for x in ["generated", "output", "temp", "tmp"]):
                                candidates["generated_files"].append(file_info)
                            else:
                                candidates["test_files"].append(file_info)
                            
                            candidates["total_size"] += file_size
                            
                        except (OSError, PermissionError) as e:
                            self.logger.warning(f"Could not access {file_path}: {e}")
                        break
        
        # Scan directories
        for dir_name in self.temp_directories:
            for dir_path in root_path.rglob(dir_name):
                if dir_path.is_dir():
                    try:
                        # Calculate directory size
                        dir_size = sum(
                            f.stat().st_size 
                            for f in dir_path.rglob("*") 
                            if f.is_file()
                        )
                        
                        dir_info = {
                            "path": str(dir_path.relative_to(root_path)),
                            "full_path": str(dir_path),
                            "size": dir_size,
                            "file_count": len(list(dir_path.rglob("*")))
                        }
                        
                        candidates["temp_directories"].append(dir_info)
                        candidates["total_size"] += dir_size
                        
                    except (OSError, PermissionError) as e:
                        self.logger.warning(f"Could not access directory {dir_path}: {e}")
        
        # Sort by size (largest first)
        for category in ["test_files", "backup_files", "generated_files"]:
            candidates[category].sort(key=lambda x: x["size"], reverse=True)
        
        candidates["temp_directories"].sort(key=lambda x: x["size"], reverse=True)
        
        total_files = (len(candidates["test_files"]) + 
                      len(candidates["backup_files"]) + 
                      len(candidates["generated_files"]))
        
        self.logger.info(f"📊 Scan completed: {total_files} files, "
                        f"{len(candidates['temp_directories'])} directories, "
                        f"{candidates['total_size']} bytes total")
        
        return candidates
    
    def cleanup_files(self, candidates: Dict[str, Any], 
                     categories: List[str] = None,
                     dry_run: bool = True) -> Dict[str, Any]:
        """Clean up the specified files and directories.
        
        Args:
            candidates: Cleanup candidates from scan_for_cleanup_candidates
            categories: Categories to clean (default: all)
            dry_run: If True, only simulate cleanup without deleting
            
        Returns:
            Cleanup results
        """
        if categories is None:
            categories = ["test_files", "backup_files", "generated_files", "temp_directories"]
        
        results = {
            "deleted_files": [],
            "deleted_directories": [],
            "errors": [],
            "total_freed": 0,
            "dry_run": dry_run
        }
        
        action_verb = "Would delete" if dry_run else "Deleting"
        self.logger.info(f"🧹 {'Simulating' if dry_run else 'Starting'} cleanup...")
        
        # Clean up files
        for category in ["test_files", "backup_files", "generated_files"]:
            if category in categories and category in candidates:
                for file_info in candidates[category]:
                    try:
                        file_path = Path(file_info["full_path"])
                        
                        if file_path.exists():
                            self.logger.info(f"   {action_verb}: {file_info['path']} ({file_info['size']} bytes)")
                            
                            if not dry_run:
                                file_path.unlink()
                            
                            results["deleted_files"].append(file_info)
                            results["total_freed"] += file_info["size"]
                        
                    except Exception as e:
                        error_msg = f"Failed to delete {file_info['path']}: {e}"
                        self.logger.error(error_msg)
                        results["errors"].append(error_msg)
        
        # Clean up directories
        if "temp_directories" in categories and "temp_directories" in candidates:
            for dir_info in candidates["temp_directories"]:
                try:
                    dir_path = Path(dir_info["full_path"])
                    
                    if dir_path.exists():
                        self.logger.info(f"   {action_verb}: {dir_info['path']}/ ({dir_info['size']} bytes)")
                        
                        if not dry_run:
                            # Remove directory and all contents
                            import shutil
                            shutil.rmtree(dir_path)
                        
                        results["deleted_directories"].append(dir_info)
                        results["total_freed"] += dir_info["size"]
                    
                except Exception as e:
                    error_msg = f"Failed to delete directory {dir_info['path']}: {e}"
                    self.logger.error(error_msg)
                    results["errors"].append(error_msg)
        
        # Log summary
        if dry_run:
            self.logger.info(f"🔍 Dry run completed: Would free {results['total_freed']} bytes")
        else:
            self.logger.info(f"✅ Cleanup completed: Freed {results['total_freed']} bytes")
        
        return results
    
    def auto_cleanup(self, root_path: str = None, 
                    max_age_days: int = 7,
                    dry_run: bool = True) -> Dict[str, Any]:
        """Automatically clean up old test files and temporary artifacts.
        
        Args:
            root_path: Root directory to clean
            max_age_days: Only clean files older than this many days
            dry_run: If True, only simulate cleanup
            
        Returns:
            Cleanup results
        """
        self.logger.info(f"🤖 Starting auto-cleanup (max age: {max_age_days} days)")
        
        # Scan for candidates
        candidates = self.scan_for_cleanup_candidates(root_path)
        
        # Filter by age
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        filtered_candidates = {
            "test_files": [],
            "backup_files": [],
            "generated_files": [],
            "temp_directories": candidates["temp_directories"],  # Always clean temp dirs
            "total_size": 0
        }
        
        for category in ["test_files", "backup_files", "generated_files"]:
            for file_info in candidates.get(category, []):
                file_age = current_time - file_info["modified"]
                if file_age > max_age_seconds:
                    filtered_candidates[category].append(file_info)
                    filtered_candidates["total_size"] += file_info["size"]
        
        # Perform cleanup
        return self.cleanup_files(filtered_candidates, dry_run=dry_run)
    
    def print_cleanup_summary(self, candidates: Dict[str, Any]):
        """Print a formatted summary of cleanup candidates."""
        print("\n" + "="*60)
        print("🧹 CLEANUP CANDIDATES SUMMARY")
        print("="*60)
        
        total_files = (len(candidates.get("test_files", [])) + 
                      len(candidates.get("backup_files", [])) + 
                      len(candidates.get("generated_files", [])))
        
        print(f"📁 Files to clean: {total_files}")
        print(f"📂 Directories to clean: {len(candidates.get('temp_directories', []))}")
        print(f"💾 Total size: {candidates.get('total_size', 0):,} bytes")
        
        # Show breakdown by category
        categories = [
            ("test_files", "🧪 Test Files"),
            ("backup_files", "💾 Backup Files"),
            ("generated_files", "⚙️  Generated Files"),
            ("temp_directories", "📂 Temp Directories")
        ]
        
        for key, label in categories:
            items = candidates.get(key, [])
            if items:
                print(f"\n{label}: {len(items)} items")
                for item in items[:5]:  # Show first 5
                    size_mb = item["size"] / (1024 * 1024)
                    print(f"   • {item['path']} ({size_mb:.2f} MB)")
                
                if len(items) > 5:
                    print(f"   ... and {len(items) - 5} more")
        
        print("="*60)
