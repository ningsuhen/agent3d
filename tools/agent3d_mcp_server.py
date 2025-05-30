#!/usr/bin/env python3
"""
Agent3D MCP Server

A comprehensive Model Context Protocol (MCP) server that provides intelligent search,
analysis, and drift detection capabilities for Agent3D Documentation-Driven Development projects.

This server leverages vector database technology for semantic search and provides
a rich set of tools for DDD workflow automation.

Features:
- Intelligent file search with semantic understanding
- Feature and test case discovery and mapping
- Vector-enhanced drift analysis
- Code location validation and suggestions
- Test quality assessment
- Live reloading and file watching
- Multi-root project support

Installation:
    pip install -r tools/requirements.txt

Dependencies:
- Required: pyyaml, sentence-transformers, faiss-cpu, numpy
- Optional: watchdog (for file watching and live reloading)

Author: Agent3D Framework
"""

import json
import sys
import os
import subprocess
import logging
import time
import threading
import re
import importlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union

# File watching for live reloading (optional dependency)
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None

# Vector database manager for enhanced file discovery
try:
    from vector_db_manager import MultiRootVectorDBManager
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    MultiRootVectorDBManager = None

# Drift scanner for analysis
try:
    from drift_scanner import MultiModeDriftAnalyzer
    DRIFT_SCANNER_AVAILABLE = True
except ImportError:
    DRIFT_SCANNER_AVAILABLE = False
    MultiModeDriftAnalyzer = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


if WATCHDOG_AVAILABLE:
    class Agent3DFileWatcher(FileSystemEventHandler):
        """File system event handler for live reloading"""

        def __init__(self, server):
            self.server = server
            super().__init__()

        def on_modified(self, event):
            """Handle file modification events"""
            if not WATCHDOG_AVAILABLE or event.is_directory:
                return

            # Check if it's a relevant file
            relevant_extensions = {'.md', '.py', '.yaml', '.yml', '.json', '.txt', '.js', '.ts', '.jsx', '.tsx'}
            file_path = Path(event.src_path)

            if file_path.suffix.lower() in relevant_extensions:
                logger.info(f"📝 File change detected: {file_path.name}")
                # Trigger incremental reindexing for the specific file
                self.server.trigger_incremental_reindex(str(file_path))
else:
    class Agent3DFileWatcher:
        """Dummy file watcher when watchdog is not available"""
        def __init__(self, server):
            self.server = server

        def on_modified(self, event):
            pass


class Agent3DMCPServer:
    """Comprehensive MCP Server for Agent3D DDD Framework"""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.agent3d_dir = self.script_dir.parent

        # Check if MCP server is disabled in configuration
        self._check_mcp_configuration()

        # Initialize components
        self.vector_db_manager = None
        self.drift_analyzer = None
        self._initialize_vector_db()
        self._initialize_drift_analyzer()

        # File watching setup
        if WATCHDOG_AVAILABLE:
            self.file_watcher = Agent3DFileWatcher(self)
            self.observer = None
            self.watched_directories = set()
        else:
            self.file_watcher = None
            self.observer = None
            self.watched_directories = set()

        logger.info("🚀 Agent3D MCP Server initialized")
        logger.info("🔍 Intelligent search and analysis capabilities enabled")
        if VECTOR_DB_AVAILABLE:
            logger.info("🧠 Vector database support: ENABLED")
        else:
            logger.warning("⚠️  Vector database support: DISABLED (install dependencies)")

    def _check_mcp_configuration(self):
        """Check if MCP server is disabled in configuration"""
        try:
            config_file = self.agent3d_dir / ".agent3d-config.yml"
            if config_file.exists():
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f) or {}

                if config.get('mcp', {}).get('disabled', False):
                    logger.info("MCP server is disabled in configuration")
                    sys.exit(0)
        except Exception as e:
            logger.debug(f"Could not check MCP configuration: {e}")

    def _initialize_vector_db(self):
        """Initialize vector database manager if available."""
        if not VECTOR_DB_AVAILABLE:
            logger.info("⚠️  Vector database dependencies not available")
            return

        try:
            self.vector_db_manager = MultiRootVectorDBManager(logger=logger)
            logger.info("✅ Vector database manager initialized")
        except Exception as e:
            logger.warning(f"⚠️  Failed to initialize vector database manager: {e}")
            self.vector_db_manager = None

    def _initialize_drift_analyzer(self):
        """Initialize drift analyzer if available."""
        if not DRIFT_SCANNER_AVAILABLE:
            logger.info("⚠️  Drift scanner not available")
            return

        try:
            # Will be initialized per DDD root as needed
            logger.info("✅ Drift analyzer support enabled")
        except Exception as e:
            logger.warning(f"⚠️  Failed to initialize drift analyzer: {e}")

    def find_ddd_root(self, explicit_root: Optional[str] = None) -> Optional[str]:
        """Find the DDD project root directory"""
        # Priority: explicit parameter > DDD_ROOT env var > auto-detection
        if explicit_root:
            root_path = Path(explicit_root).resolve()
            if (root_path / ".agent3d-config.yml").exists():
                return str(root_path)
            else:
                logger.warning(f"Explicit DDD root {explicit_root} does not contain .agent3d-config.yml")
                return None

        # Check DDD_ROOT environment variable
        env_root = os.environ.get('DDD_ROOT')
        if env_root:
            root_path = Path(env_root).resolve()
            if (root_path / ".agent3d-config.yml").exists():
                return str(root_path)
            else:
                logger.warning(f"DDD_ROOT environment variable {env_root} does not contain .agent3d-config.yml")

        # Auto-detection: look for .agent3d-config.yml in current directory and parents
        current_path = Path.cwd()
        for path in [current_path] + list(current_path.parents):
            if (path / ".agent3d-config.yml").exists():
                return str(path)

        return None

    def invalidate_cache(self):
        """Invalidate all caches"""
        if self.vector_db_manager:
            self.vector_db_manager.invalidate_cache()
            logger.info("🗑️  Invalidated all vector database caches")

    def trigger_incremental_reindex(self, file_path: str):
        """Trigger incremental reindexing for a specific changed file"""
        if not self.vector_db_manager:
            return

        file_path = Path(file_path)

        # Find the DDD root for this file path
        for watched_dir in self.watched_directories:
            watched_path = Path(watched_dir)
            try:
                # Check if the file is within this watched directory
                file_path.relative_to(watched_path)

                # Attempt incremental reindexing
                success = self.vector_db_manager.incremental_reindex(watched_dir, str(file_path))

                if success:
                    logger.info(f"✅ Incremental reindex completed for: {file_path.name}")
                else:
                    # Fall back to full cache invalidation if incremental fails
                    logger.info(f"⚠️  Incremental reindex failed, invalidating cache for: {watched_dir}")
                    self.vector_db_manager.invalidate_cache(watched_dir)

                break
            except ValueError:
                # File is not within this watched directory
                continue

    def force_full_reindex_on_startup(self, ddd_root: str):
        """Force a full reindex on server startup to ensure sync"""
        if not self.vector_db_manager:
            return

        try:
            logger.info(f"🔄 Performing startup full reindex for: {ddd_root}")

            # Force invalidate cache to ensure fresh start
            self.vector_db_manager.invalidate_cache(ddd_root)

            # Create database with force_reindex=True
            db = self.vector_db_manager.get_or_create_database(ddd_root, force_reindex=True)

            if db:
                logger.info(f"✅ Startup full reindex completed for: {ddd_root}")
            else:
                logger.warning(f"⚠️  Startup full reindex failed for: {ddd_root}")

        except Exception as e:
            logger.error(f"❌ Startup full reindex error for {ddd_root}: {e}")

    def get_drift_analyzer(self, ddd_root: str) -> Optional[Any]:
        """Get or create drift analyzer for the specified DDD root"""
        if not DRIFT_SCANNER_AVAILABLE:
            return None

        try:
            # Force reload the drift_scanner module to pick up any changes
            try:
                import drift_scanner
                importlib.reload(drift_scanner)
                # Re-import the class after reload
                from drift_scanner import MultiModeDriftAnalyzer
            except Exception as reload_error:
                logger.warning(f"Failed to reload drift_scanner module: {reload_error}")
                # Fall back to cached version
                pass

            analyzer = MultiModeDriftAnalyzer(
                root_dir=ddd_root,
                enable_vector_db=bool(self.vector_db_manager)
            )
            return analyzer
        except Exception as e:
            logger.error(f"Failed to create drift analyzer for {ddd_root}: {e}")
            return None

    def start_file_watching(self, ddd_root: str):
        """Start file watching for the specified directory"""
        if not WATCHDOG_AVAILABLE or not ddd_root:
            return

        if ddd_root in self.watched_directories:
            return  # Already watching

        try:
            if not self.observer:
                self.observer = Observer()
                self.observer.start()

            self.observer.schedule(self.file_watcher, ddd_root, recursive=True)
            self.watched_directories.add(ddd_root)
            logger.info(f"👁️  Started file watching for: {ddd_root}")
        except Exception as e:
            logger.warning(f"Failed to start file watching for {ddd_root}: {e}")

    def stop_file_watching(self):
        """Stop file watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watched_directories.clear()
            logger.info("👁️  File watching stopped")

    # ==================== SEARCH FUNCTIONS ====================

    def search_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for files using semantic search with various filters"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            query = args.get('query', '')
            if not query:
                raise Exception("Query parameter is required")

            file_type = args.get('file_type', 'any')  # any, python, test, doc, config
            top_k = args.get('top_k', 10)
            min_similarity = args.get('min_similarity', 0.3)

            if not self.vector_db_manager:
                return {"error": "Vector database not available"}

            # Start file watching for this root
            self.start_file_watching(ddd_root)

            # Check if this is the first access to this DDD root (startup reindex)
            is_first_access = ddd_root not in getattr(self.vector_db_manager, 'databases', {})

            # Get or create vector database
            db = self.vector_db_manager.get_or_create_database(ddd_root)
            if not db:
                return {"error": "Failed to create vector database"}

            # Perform startup verification reindex if this is the first access
            if is_first_access:
                logger.info(f"🔄 First access detected, performing startup verification for: {ddd_root}")
                # This ensures we have the most up-to-date content on startup
                self.force_full_reindex_on_startup(ddd_root)
                # Reload the database after startup reindex
                db = self.vector_db_manager.get_or_create_database(ddd_root)
                if not db:
                    return {"error": "Failed to create vector database after startup reindex"}

            # Apply filters based on file type
            filter_language = None
            filter_chunk_type = None

            if file_type == 'python':
                filter_language = 'python'
            elif file_type == 'test':
                filter_chunk_type = 'test'
            elif file_type == 'doc':
                filter_language = 'markdown'

            # Perform search
            results = self.vector_db_manager.search(
                ddd_root, query, top_k, filter_language, filter_chunk_type
            )

            # Filter by minimum similarity and format results
            filtered_results = []
            seen_files = set()

            for chunk, score in results:
                if score >= min_similarity and hasattr(chunk, 'file_path'):
                    if chunk.file_path not in seen_files:
                        seen_files.add(chunk.file_path)

                        # Additional filtering based on file type
                        file_path_lower = chunk.file_path.lower()
                        if file_type == 'test' and 'test' not in file_path_lower:
                            continue
                        elif file_type == 'doc' and not any(ext in file_path_lower for ext in ['.md', '.rst', '.txt']):
                            continue
                        elif file_type == 'config' and not any(ext in file_path_lower for ext in ['.yml', '.yaml', '.json', '.toml', '.ini']):
                            continue

                        filtered_results.append({
                            'file_path': chunk.file_path,
                            'similarity_score': round(score, 3),
                            'chunk_type': getattr(chunk, 'chunk_type', 'unknown'),
                            'language': getattr(chunk, 'language', 'unknown'),
                            'content_preview': getattr(chunk, 'content', '')[:200] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 200 else getattr(chunk, 'content', '')
                        })

            return {
                "query": query,
                "file_type": file_type,
                "ddd_root": ddd_root,
                "total_results": len(filtered_results),
                "min_similarity": min_similarity,
                "results": filtered_results[:top_k]
            }

        except Exception as e:
            logger.error(f"Error in search_files: {e}")
            return {"error": str(e)}

    def search_test_cases(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for test cases with TC-* identifiers"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            query = args.get('query', '')
            tc_id = args.get('tc_id', '')  # Specific TC-* identifier
            top_k = args.get('top_k', 10)

            if not query and not tc_id:
                raise Exception("Either query or tc_id parameter is required")

            if not self.vector_db_manager:
                return {"error": "Vector database not available"}

            # Start file watching
            self.start_file_watching(ddd_root)

            # Search for test cases using multiple strategies
            search_results = []

            if tc_id:
                # Search for specific TC-* identifier
                tc_query = f"TC-{tc_id}"
                # Search in documentation first (where test cases are defined)
                doc_results = self.vector_db_manager.search(
                    ddd_root, tc_query, top_k * 2,
                    filter_language="markdown"
                )
                search_results.extend(doc_results)

                # Also search for test implementations that reference this TC-*
                impl_results = self.vector_db_manager.search(
                    ddd_root, tc_query, top_k,
                    filter_chunk_type="test"
                )
                search_results.extend(impl_results)
            else:
                # Search for test case descriptions
                # First search in feature documentation
                doc_query = f"test case {query}"
                doc_results = self.vector_db_manager.search(
                    ddd_root, doc_query, top_k,
                    filter_language="markdown"
                )
                search_results.extend(doc_results)

                # Then search for related test implementations
                test_query = f"test {query}"
                test_results = self.vector_db_manager.search(
                    ddd_root, test_query, top_k,
                    filter_chunk_type="test"
                )
                search_results.extend(test_results)

            # Combine and process results
            all_results = []
            seen_items = set()

            # Process all search results
            for chunk, score in search_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    key = f"impl_{chunk.file_path}"
                    if key not in seen_items:
                        seen_items.add(key)

                        # Extract TC IDs from content
                        tc_ids = []
                        if hasattr(chunk, 'content'):
                            tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                            tc_ids = list(set(tc_matches))

                        all_results.append({
                            'type': 'test_implementation',
                            'file_path': chunk.file_path,
                            'similarity_score': round(score, 3),
                            'tc_ids_found': tc_ids,
                            'content_preview': getattr(chunk, 'content', '')[:300] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 300 else getattr(chunk, 'content', '')
                        })

            # Process documentation results
            for chunk, score in doc_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    key = f"doc_{chunk.file_path}"
                    if key not in seen_items:
                        seen_items.add(key)

                        # Extract TC IDs from content
                        tc_ids = []
                        if hasattr(chunk, 'content'):
                            tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                            tc_ids = list(set(tc_matches))

                        all_results.append({
                            'type': 'test_documentation',
                            'file_path': chunk.file_path,
                            'similarity_score': round(score, 3),
                            'tc_ids_found': tc_ids,
                            'content_preview': getattr(chunk, 'content', '')[:300] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 300 else getattr(chunk, 'content', '')
                        })

            # Sort by similarity score
            all_results.sort(key=lambda x: x['similarity_score'], reverse=True)

            # Determine the primary search query used
            primary_query = f"TC-{tc_id}" if tc_id else f"test case {query}"

            return {
                "search_query": primary_query,
                "tc_id": tc_id,
                "query": query,
                "ddd_root": ddd_root,
                "total_results": len(all_results),
                "results": all_results[:top_k]
            }

        except Exception as e:
            logger.error(f"Error in search_test_cases: {e}")
            return {"error": str(e)}

    def search_features(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for features with FT-* identifiers"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            query = args.get('query', '')
            ft_id = args.get('ft_id', '')  # Specific FT-* identifier
            top_k = args.get('top_k', 10)

            if not query and not ft_id:
                raise Exception("Either query or ft_id parameter is required")

            if not self.vector_db_manager:
                return {"error": "Vector database not available"}

            # Start file watching
            self.start_file_watching(ddd_root)

            # Search for features
            search_query = f"FT-{ft_id}" if ft_id else f"feature {query}"

            # Search in documentation (features are primarily documented)
            doc_results = self.vector_db_manager.search(
                ddd_root, search_query, top_k * 2,
                filter_language="markdown"
            )

            # Also search for related implementations
            impl_results = self.vector_db_manager.search(
                ddd_root, search_query, top_k,
                filter_language="python"
            )

            # Combine and process results
            all_results = []
            seen_items = set()

            # Process documentation results
            for chunk, score in doc_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    key = f"doc_{chunk.file_path}"
                    if key not in seen_items:
                        seen_items.add(key)

                        # Extract FT IDs from content
                        ft_ids = []
                        tc_ids = []
                        if hasattr(chunk, 'content'):
                            ft_matches = re.findall(r'FT-[A-Z]+-\d+', chunk.content)
                            tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                            ft_ids = list(set(ft_matches))
                            tc_ids = list(set(tc_matches))

                        all_results.append({
                            'type': 'feature_documentation',
                            'file_path': chunk.file_path,
                            'similarity_score': round(score, 3),
                            'ft_ids_found': ft_ids,
                            'tc_ids_found': tc_ids,
                            'content_preview': getattr(chunk, 'content', '')[:300] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 300 else getattr(chunk, 'content', '')
                        })

            # Process implementation results
            for chunk, score in impl_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    key = f"impl_{chunk.file_path}"
                    if key not in seen_items and 'test' not in chunk.file_path.lower():
                        seen_items.add(key)

                        # Extract FT IDs from content (comments, docstrings)
                        ft_ids = []
                        if hasattr(chunk, 'content'):
                            ft_matches = re.findall(r'FT-[A-Z]+-\d+', chunk.content)
                            ft_ids = list(set(ft_matches))

                        all_results.append({
                            'type': 'feature_implementation',
                            'file_path': chunk.file_path,
                            'similarity_score': round(score, 3),
                            'ft_ids_found': ft_ids,
                            'chunk_type': getattr(chunk, 'chunk_type', 'unknown'),
                            'content_preview': getattr(chunk, 'content', '')[:300] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 300 else getattr(chunk, 'content', '')
                        })

            # Sort by similarity score
            all_results.sort(key=lambda x: x['similarity_score'], reverse=True)

            return {
                "search_query": search_query,
                "ft_id": ft_id,
                "query": query,
                "ddd_root": ddd_root,
                "total_results": len(all_results),
                "results": all_results[:top_k]
            }

        except Exception as e:
            logger.error(f"Error in search_features: {e}")
            return {"error": str(e)}

    def find_feature_test_mapping(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Find mapping between features (FT-*) and test cases (TC-*)"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            feature_query = args.get('feature_query', '')
            ft_id = args.get('ft_id', '')
            top_k = args.get('top_k', 10)

            if not feature_query and not ft_id:
                raise Exception("Either feature_query or ft_id parameter is required")

            if not self.vector_db_manager:
                return {"error": "Vector database not available"}

            # Start file watching
            self.start_file_watching(ddd_root)

            # Search for the feature first
            search_query = f"FT-{ft_id}" if ft_id else feature_query

            # Find feature documentation
            feature_results = self.vector_db_manager.search(
                ddd_root, search_query, 5,
                filter_language="markdown"
            )

            # Find related test cases
            test_query = f"test {search_query}"
            test_results = self.vector_db_manager.search(
                ddd_root, test_query, top_k,
                filter_chunk_type="test"
            )

            # Find test documentation
            test_doc_results = self.vector_db_manager.search(
                ddd_root, f"TC test case {search_query}", top_k,
                filter_language="markdown"
            )

            # Process results
            mapping_results = {
                "feature_query": search_query,
                "ft_id": ft_id,
                "ddd_root": ddd_root,
                "features_found": [],
                "related_tests": [],
                "test_documentation": []
            }

            # Process feature results
            for chunk, score in feature_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    ft_ids = []
                    tc_ids = []
                    if hasattr(chunk, 'content'):
                        ft_matches = re.findall(r'FT-[A-Z]+-\d+', chunk.content)
                        tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                        ft_ids = list(set(ft_matches))
                        tc_ids = list(set(tc_matches))

                    mapping_results["features_found"].append({
                        'file_path': chunk.file_path,
                        'similarity_score': round(score, 3),
                        'ft_ids': ft_ids,
                        'related_tc_ids': tc_ids,
                        'content_preview': getattr(chunk, 'content', '')[:200] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 200 else getattr(chunk, 'content', '')
                    })

            # Process test implementation results
            seen_test_files = set()
            for chunk, score in test_results:
                if hasattr(chunk, 'file_path') and score > 0.3 and chunk.file_path not in seen_test_files:
                    seen_test_files.add(chunk.file_path)

                    tc_ids = []
                    ft_ids = []
                    if hasattr(chunk, 'content'):
                        tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                        ft_matches = re.findall(r'FT-[A-Z]+-\d+', chunk.content)
                        tc_ids = list(set(tc_matches))
                        ft_ids = list(set(ft_matches))

                    mapping_results["related_tests"].append({
                        'file_path': chunk.file_path,
                        'similarity_score': round(score, 3),
                        'tc_ids': tc_ids,
                        'ft_ids': ft_ids,
                        'content_preview': getattr(chunk, 'content', '')[:200] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 200 else getattr(chunk, 'content', '')
                    })

            # Process test documentation results
            for chunk, score in test_doc_results:
                if hasattr(chunk, 'file_path') and score > 0.3:
                    tc_ids = []
                    ft_ids = []
                    if hasattr(chunk, 'content'):
                        tc_matches = re.findall(r'TC-[A-Z]+-\d+(?:-[a-z])?', chunk.content)
                        ft_matches = re.findall(r'FT-[A-Z]+-\d+', chunk.content)
                        tc_ids = list(set(tc_matches))
                        ft_ids = list(set(ft_matches))

                    mapping_results["test_documentation"].append({
                        'file_path': chunk.file_path,
                        'similarity_score': round(score, 3),
                        'tc_ids': tc_ids,
                        'ft_ids': ft_ids,
                        'content_preview': getattr(chunk, 'content', '')[:200] + '...' if hasattr(chunk, 'content') and len(getattr(chunk, 'content', '')) > 200 else getattr(chunk, 'content', '')
                    })

            return mapping_results

        except Exception as e:
            logger.error(f"Error in find_feature_test_mapping: {e}")
            return {"error": str(e)}

    # ==================== ANALYSIS FUNCTIONS ====================

    def analyze_drift(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive drift analysis with vector enhancement"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            mode = args.get('mode', 'all')
            quiet = args.get('quiet', False)

            # Start file watching
            self.start_file_watching(ddd_root)

            # Get drift analyzer
            analyzer = self.get_drift_analyzer(ddd_root)
            if not analyzer:
                return {"error": "Drift analyzer not available"}

            # Perform analysis
            if not quiet:
                logger.info(f"🔍 Starting drift analysis in mode: {mode}")

            report = analyzer.analyze_drift(mode)

            # Convert report to dictionary format
            result = {
                "mode": mode,
                "ddd_root": ddd_root,
                "vector_enhanced": bool(analyzer.vector_db_manager),
                "metadata": getattr(report, 'metadata', {}),
                "summary": {
                    "total_test_cases": getattr(report, 'total_test_cases', 0),
                    "total_test_functions": getattr(report, 'total_test_functions', 0),
                    "drift_level": "high" if getattr(report, 'total_test_cases', 0) > getattr(report, 'total_test_functions', 0) else "low"
                }
            }

            # Add mode-specific results
            if hasattr(report, 'test_cases_without_implementation'):
                result["test_cases_without_implementation"] = [
                    {
                        "tc_id": tc.tc_id,
                        "title": tc.title,
                        "file": tc.file
                    } for tc in report.test_cases_without_implementation[:10]  # Limit for MCP
                ]

            if hasattr(report, 'features_without_tests'):
                result["features_without_tests"] = [
                    {
                        "ft_id": ft.ft_id,
                        "title": ft.title,
                        "file": getattr(ft, 'file', 'unknown')
                    } for ft in report.features_without_tests[:10]  # Limit for MCP
                ]

            if hasattr(report, 'coverage_issues'):
                result["coverage_issues"] = [
                    {
                        "file": issue.file,
                        "function": issue.function,
                        "issue_type": issue.issue_type,
                        "severity": issue.severity
                    } for issue in report.coverage_issues[:10]  # Limit for MCP
                ]

            if hasattr(report, 'test_quality_score') and report.test_quality_score is not None:
                result["test_quality_score"] = round(report.test_quality_score, 3)

            return result

        except Exception as e:
            logger.error(f"Error in analyze_drift: {e}")
            return {"error": str(e)}

    def validate_code_locations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and suggest code locations for features"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            # Start file watching
            self.start_file_watching(ddd_root)

            # Get drift analyzer
            analyzer = self.get_drift_analyzer(ddd_root)
            if not analyzer:
                return {"error": "Drift analyzer not available"}

            # Perform code location analysis
            logger.info("🔍 Validating code locations...")
            report = analyzer._analyze_code_location()

            # Format results
            result = {
                "ddd_root": ddd_root,
                "vector_enhanced": bool(analyzer.vector_db_manager),
                "total_features": report.metadata.get('total_features', 0),
                "features_with_code_location": report.metadata.get('features_with_code_location', 0),
                "coverage_percentage": report.metadata.get('coverage_percentage', 0),
                "issues": []
            }

            # Add code location issues
            if hasattr(report, 'code_location_issues'):
                for issue in report.code_location_issues[:20]:  # Limit for MCP
                    result["issues"].append({
                        "feature_id": issue.feature_id,
                        "feature_name": issue.feature_name,
                        "current_location": issue.code_location,
                        "issue_type": issue.issue_type,
                        "severity": issue.severity,
                        "description": issue.description,
                        "suggestion": issue.suggestion,
                        "expected_path": getattr(issue, 'expected_path', None)
                    })

            return result

        except Exception as e:
            logger.error(f"Error in validate_code_locations: {e}")
            return {"error": str(e)}

    def get_vector_stats(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get vector database statistics"""
        try:
            ddd_root = self.find_ddd_root(args.get('ddd_root'))
            if not ddd_root:
                raise Exception("No DDD root found")

            if not self.vector_db_manager:
                return {"error": "Vector database not available"}

            # Start file watching
            self.start_file_watching(ddd_root)

            # Get statistics
            stats = self.vector_db_manager.get_statistics(ddd_root)

            return {
                "ddd_root": ddd_root,
                "vector_database_stats": stats
            }

        except Exception as e:
            logger.error(f"Error in get_vector_stats: {e}")
            return {"error": str(e)}

    # ==================== MCP PROTOCOL HANDLERS ====================

    def handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = [
            {
                "name": "search_files",
                "description": "Semantic file search across repository using vector embeddings. Searches file content, not just names. Supports: Python (.py), JavaScript/TypeScript (.js/.ts), Markdown (.md), YAML (.yml/.yaml), JSON, and other text files. Filters: 'python' (Python files only), 'test' (test files), 'doc' (documentation), 'config' (configuration files), 'any' (all supported types). Returns similarity scores (0.0-1.0) with file paths and content previews. Requires vector database to be indexed for the target repository.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Natural language search query (e.g., 'HTTP client implementation', 'error handling functions')"},
                        "file_type": {"type": "string", "enum": ["any", "python", "test", "doc", "config"], "default": "any", "description": "File type filter: 'python' (.py files), 'test' (test files), 'doc' (documentation), 'config' (config files), 'any' (all types)"},
                        "top_k": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50, "description": "Maximum number of results to return"},
                        "min_similarity": {"type": "number", "default": 0.3, "minimum": 0.0, "maximum": 1.0, "description": "Minimum similarity score threshold (0.3 = 30% similarity)"},
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_test_cases",
                "description": "Search for test cases (TC-*) in feature documentation files, NOT test implementations. Test cases are specifications defined in feature files (docs/features/*.md) with TC-* identifiers like TC-HTTP-001. This tool searches both test case documentation and finds related test implementations that reference these TC-* IDs. Supports semantic search by description or exact TC-* ID lookup. Returns test case specifications from documentation and any Python test functions that implement them (with @pytest.mark or TC-* comments).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for test case descriptions (e.g., 'HTTP error handling', 'authentication tests') or leave empty when using tc_id"},
                        "tc_id": {"type": "string", "description": "Specific TC-* identifier without 'TC-' prefix (e.g., 'HTTP-001' for TC-HTTP-001)"},
                        "top_k": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50, "description": "Maximum number of results to return"},
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            },
            {
                "name": "search_features",
                "description": "Search for feature specifications (FT-*) in documentation files and their implementations. Features are defined in docs/features/*.md files with FT-* identifiers like FT-CORE-001. Each feature includes description, test cases (TC-*), code locations, and implementation status. This tool searches feature documentation semantically and can locate corresponding source code implementations. Returns feature specifications, associated test cases, code locations, and implementation status. Does NOT search arbitrary code - only documented features with FT-* identifiers.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for feature descriptions (e.g., 'user authentication', 'HTTP client', 'data validation') or leave empty when using ft_id"},
                        "ft_id": {"type": "string", "description": "Specific FT-* identifier without 'FT-' prefix (e.g., 'CORE-001' for FT-CORE-001)"},
                        "top_k": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50, "description": "Maximum number of results to return"},
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            },
            {
                "name": "find_feature_test_mapping",
                "description": "Find relationships between feature specifications (FT-*) and their test cases (TC-*) using semantic analysis. This tool analyzes feature documentation to identify which test cases validate each feature, and finds test implementations that cover those test cases. Returns comprehensive mapping showing: feature specifications, associated test cases from documentation, test implementations in code, coverage gaps, and traceability matrix. Useful for understanding test coverage and ensuring features are properly validated.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "feature_query": {"type": "string", "description": "Natural language query for features to analyze (e.g., 'authentication features', 'HTTP client functionality')"},
                        "ft_id": {"type": "string", "description": "Specific FT-* identifier without 'FT-' prefix (e.g., 'CORE-001' for FT-CORE-001) to analyze specific feature"},
                        "top_k": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50, "description": "Maximum number of feature-test mappings to return"},
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            },
            {
                "name": "analyze_drift",
                "description": "Comprehensive drift analysis to detect inconsistencies between documentation and implementation in DDD projects. Analyzes: test case mapping (TC-* in docs vs implementations), feature mapping (FT-* documentation vs code), feature-test relationships, code coverage gaps, test quality metrics, and code location accuracy. Uses vector search for enhanced semantic analysis. Modes: 'tc-mapping' (test case drift), 'ft-mapping' (feature drift), 'ft-tc-mapping' (feature-test relationships), 'code-coverage' (implementation gaps), 'test-quality' (test completeness), 'code-location' (location accuracy), 'all' (comprehensive analysis). Returns detailed drift report with recommendations.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "string", "enum": ["tc-mapping", "ft-mapping", "ft-tc-mapping", "code-coverage", "test-quality", "code-location", "all"], "default": "all", "description": "Analysis mode: 'tc-mapping' (test case drift), 'ft-mapping' (feature drift), 'ft-tc-mapping' (feature-test relationships), 'code-coverage' (implementation gaps), 'test-quality' (test completeness), 'code-location' (location accuracy), 'all' (comprehensive)"},
                        "quiet": {"type": "boolean", "default": False, "description": "Suppress verbose output, return summary only"},
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            },
            {
                "name": "validate_code_locations",
                "description": "Validate and suggest accurate code locations for features using vector search and semantic analysis. Analyzes feature documentation (FT-*) to verify that specified code locations (file paths, classes, methods) actually exist and contain relevant implementations. Uses vector search to find better code locations when current ones are invalid or incomplete. Returns validation results showing: valid locations, invalid/missing locations, suggested alternatives with similarity scores, and recommendations for updating feature documentation. Helps maintain accurate traceability between features and their implementations.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            },
            {
                "name": "get_vector_stats",
                "description": "Get comprehensive statistics and health information about the vector database for a project. Returns detailed metrics including: total indexed files and code chunks, supported programming languages, embedding model information, index size and performance, cache status, and database health indicators. Useful for understanding search capabilities, troubleshooting indexing issues, and monitoring vector database performance. Shows whether semantic search is available and functioning properly for the target repository.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ddd_root": {"type": "string", "description": "DDD project root directory path (optional, defaults to current project)"}
                    }
                }
            }
        ]

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }

    def handle_tools_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})

        try:
            # Route to appropriate function
            if tool_name == "search_files":
                result = self.search_files(arguments)
            elif tool_name == "search_test_cases":
                result = self.search_test_cases(arguments)
            elif tool_name == "search_features":
                result = self.search_features(arguments)
            elif tool_name == "find_feature_test_mapping":
                result = self.find_feature_test_mapping(arguments)
            elif tool_name == "analyze_drift":
                result = self.analyze_drift(arguments)
            elif tool_name == "validate_code_locations":
                result = self.validate_code_locations(arguments)
            elif tool_name == "get_vector_stats":
                result = self.get_vector_stats(arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }

            # Check for errors in result
            if isinstance(result, dict) and "error" in result:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Tool execution failed: {result['error']}"
                    }
                }

            # Format successful response
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }

        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Tool execution failed: {str(e)}"
                }
            }

    def handle_initialize(self, request_id: Any) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "agent3d-mcp",
                    "version": "2.0.0"
                }
            }
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        method = request.get('method')
        request_id = request.get('id')
        params = request.get('params', {})

        logger.info(f"Handling request: {method}")

        if method == "initialize":
            return self.handle_initialize(request_id)
        elif method == "tools/list":
            return self.handle_tools_list(request_id)
        elif method == "tools/call":
            return self.handle_tools_call(request_id, params)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def run(self):
        """Run the MCP server"""
        logger.info("🚀 Agent3D MCP Server starting...")
        logger.info("📡 Listening for JSON-RPC requests on stdin...")

        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                try:
                    request = json.loads(line)
                    response = self.handle_request(request)

                    # Send response to stdout (MCP protocol)
                    print(json.dumps(response), flush=True)

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON request: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)

                except Exception as e:
                    logger.error(f"Error handling request: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32603,
                            "message": "Internal error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)

        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)
        finally:
            self.stop_file_watching()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        print("ERROR: Agent3D MCP server should not be called with command-line arguments", file=sys.stderr)
        print("Usage: echo '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\"}' | python3 agent3d_mcp_server.py", file=sys.stderr)
        print("This is an MCP server that communicates via JSON-RPC over stdin/stdout", file=sys.stderr)
        sys.exit(1)

    server = Agent3DMCPServer()
    server.run()


if __name__ == "__main__":
    main()
