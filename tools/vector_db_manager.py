#!/usr/bin/env python3
"""
Multi-Root Vector Database Manager for Agent3D Drift Scanner

This module manages multiple vector databases for different DDD_ROOT directories,
providing efficient indexing and search capabilities for drift analysis.

Features:
- Multiple vector databases for different DDD_ROOT directories
- Automatic indexing and cache management
- File change detection and incremental updates
- Graceful fallback when vector dependencies are unavailable
"""

import os
import sys
import logging
import hashlib
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict

# Add the parent directory to sys.path to import vector_db
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from agents.orchestrator.vector_db import RepositoryVectorDB, CodeChunk
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    RepositoryVectorDB = None
    CodeChunk = None


@dataclass
class VectorDBMetadata:
    """Metadata for a vector database instance."""
    ddd_root: str
    last_indexed: float
    file_count: int
    chunk_count: int
    content_hash: str
    version: str = "1.0"


class MultiRootVectorDBManager:
    """Manager for multiple vector databases across different DDD_ROOT directories."""

    def __init__(self, logger: logging.Logger = None, cache_dir: str = None):
        """Initialize the multi-root vector database manager.

        Args:
            logger: Logger instance
            cache_dir: Directory for storing cache metadata (default: .agent3d-tmp/vector-cache)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.cache_dir = Path(cache_dir) if cache_dir else Path.cwd() / ".agent3d-tmp" / "vector-cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Dictionary to store vector databases by DDD_ROOT path
        self.databases: Dict[str, RepositoryVectorDB] = {}
        self.metadata: Dict[str, VectorDBMetadata] = {}

        # Check if vector database functionality is available
        if not VECTOR_DB_AVAILABLE:
            self.logger.warning("⚠️  Vector database dependencies not available. Falling back to file system scanning.")
        else:
            self.logger.info("✅ Vector database manager initialized")

    def get_or_create_database(self, ddd_root: str, force_reindex: bool = False) -> Optional[RepositoryVectorDB]:
        """Get or create a vector database for the specified DDD_ROOT.

        Args:
            ddd_root: Path to the DDD project root
            force_reindex: Force reindexing even if cache is valid

        Returns:
            RepositoryVectorDB instance or None if not available
        """
        if not VECTOR_DB_AVAILABLE:
            self.logger.warning("Vector database not available")
            return None

        ddd_root = str(Path(ddd_root).resolve())

        # Check if we already have this database loaded
        if ddd_root in self.databases and not force_reindex:
            if self._is_cache_valid(ddd_root):
                self.logger.info(f"📚 Using cached vector database for: {ddd_root}")
                return self.databases[ddd_root]
            else:
                self.logger.info(f"🔄 Cache invalid, reindexing: {ddd_root}")

        # Create or recreate the database
        return self._create_database(ddd_root)

    def _create_database(self, ddd_root: str) -> Optional[RepositoryVectorDB]:
        """Create a new vector database for the DDD_ROOT."""
        try:
            self.logger.info(f"🔧 Creating vector database for: {ddd_root}")

            # Initialize the vector database with cache directory
            db = RepositoryVectorDB(logger=self.logger, cache_dir=str(self.cache_dir))

            # Generate cache key for this DDD_ROOT
            cache_key = hashlib.md5(ddd_root.encode()).hexdigest()

            # Try to load from cache first
            if db.load_from_cache(cache_key):
                self.logger.info(f"📚 Loaded vector database from cache for: {ddd_root}")

                # Store database and load metadata
                self.databases[ddd_root] = db
                if self._load_metadata(ddd_root):
                    return db

            # Cache miss or invalid - create new index
            self.logger.info(f"🔄 Building new vector index for: {ddd_root}")

            # Index the repository
            exclude_patterns = [
                '.git', '__pycache__', '.pytest_cache', 'node_modules',
                '.venv', 'venv', '.env', '.agent3d-tmp', '.DS_Store',
                '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib'
            ]

            start_time = time.time()
            stats = db.index_repository(ddd_root, exclude_patterns)
            index_time = time.time() - start_time

            # Save to cache
            db.save_to_cache(cache_key)

            # Calculate content hash for cache validation
            content_hash = self._calculate_content_hash(ddd_root, exclude_patterns)

            # Store database and metadata
            self.databases[ddd_root] = db
            self.metadata[ddd_root] = VectorDBMetadata(
                ddd_root=ddd_root,
                last_indexed=time.time(),
                file_count=stats.get("files_processed", 0),
                chunk_count=stats.get("chunks_created", 0),
                content_hash=content_hash
            )

            # Save metadata to cache
            self._save_metadata(ddd_root)

            self.logger.info(f"✅ Vector database created in {index_time:.2f}s: "
                           f"{stats.get('chunks_created', 0)} chunks from {stats.get('files_processed', 0)} files")

            return db

        except Exception as e:
            self.logger.error(f"Failed to create vector database for {ddd_root}: {e}")
            return None

    def _is_cache_valid(self, ddd_root: str) -> bool:
        """Check if the cached vector database is still valid."""
        if ddd_root not in self.metadata:
            # Load metadata from cache
            if not self._load_metadata(ddd_root):
                return False

        metadata = self.metadata[ddd_root]

        # Check if actual cache files exist
        cache_key = hashlib.md5(ddd_root.encode()).hexdigest()
        cache_path = self.cache_dir / f"{cache_key}"
        chunks_file = cache_path / "chunks.pkl"
        embeddings_file = cache_path / "embeddings.npy"

        if not cache_path.exists() or not chunks_file.exists() or not embeddings_file.exists():
            self.logger.info(f"📁 Cache files missing for {ddd_root}, cache invalid")
            return False

        # Check if content has changed
        current_hash = self._calculate_content_hash(ddd_root, [
            '.git', '__pycache__', '.pytest_cache', 'node_modules',
            '.venv', 'venv', '.env', '.agent3d-tmp', '.DS_Store',
            '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib'
        ])

        if current_hash != metadata.content_hash:
            self.logger.info(f"📝 Content changed in {ddd_root}, cache invalid")
            return False

        # Check if cache is too old (24 hours)
        cache_age = time.time() - metadata.last_indexed
        if cache_age > 24 * 3600:
            self.logger.info(f"⏰ Cache too old for {ddd_root} ({cache_age/3600:.1f}h), reindexing")
            return False

        return True

    def _calculate_content_hash(self, ddd_root: str, exclude_patterns: List[str]) -> str:
        """Calculate a hash of the repository content for cache validation."""
        hasher = hashlib.md5()

        try:
            repo_path = Path(ddd_root)

            # Get all relevant files and their modification times
            files_info = []
            for file_path in repo_path.rglob('*'):
                if file_path.is_file():
                    # Check if file should be excluded
                    relative_path = file_path.relative_to(repo_path)
                    path_str = str(relative_path)

                    excluded = False
                    for pattern in exclude_patterns:
                        if pattern in path_str or file_path.name.startswith('.'):
                            excluded = True
                            break

                    if not excluded:
                        try:
                            stat = file_path.stat()
                            files_info.append((str(relative_path), stat.st_mtime, stat.st_size))
                        except:
                            continue

            # Sort for consistent hashing
            files_info.sort()

            # Hash the file information
            for file_info in files_info:
                hasher.update(str(file_info).encode())

            return hasher.hexdigest()

        except Exception as e:
            self.logger.warning(f"Failed to calculate content hash for {ddd_root}: {e}")
            return str(time.time())  # Fallback to timestamp

    def _save_metadata(self, ddd_root: str):
        """Save metadata to cache file."""
        if ddd_root not in self.metadata:
            return

        try:
            cache_file = self.cache_dir / f"{hashlib.md5(ddd_root.encode()).hexdigest()}.json"
            with open(cache_file, 'w') as f:
                json.dump(asdict(self.metadata[ddd_root]), f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save metadata for {ddd_root}: {e}")

    def _load_metadata(self, ddd_root: str) -> bool:
        """Load metadata from cache file."""
        try:
            cache_file = self.cache_dir / f"{hashlib.md5(ddd_root.encode()).hexdigest()}.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                self.metadata[ddd_root] = VectorDBMetadata(**data)
                return True
        except Exception as e:
            self.logger.warning(f"Failed to load metadata for {ddd_root}: {e}")

        return False

    def search(self, ddd_root: str, query: str, top_k: int = 10,
               filter_language: str = None, filter_chunk_type: str = None) -> List[Tuple[Any, float]]:
        """Search for relevant code chunks in the specified DDD_ROOT.

        Args:
            ddd_root: Path to the DDD project root
            query: Search query
            top_k: Number of results to return
            filter_language: Filter by programming language
            filter_chunk_type: Filter by chunk type

        Returns:
            List of (chunk, similarity_score) tuples
        """
        db = self.get_or_create_database(ddd_root)
        if not db:
            return []

        return db.search(query, top_k, filter_language, filter_chunk_type)

    def get_related_files(self, ddd_root: str, query: str, top_k: int = 5) -> List[str]:
        """Get files most related to the query in the specified DDD_ROOT."""
        db = self.get_or_create_database(ddd_root)
        if not db:
            return []

        return db.get_related_files(query, top_k)

    def get_statistics(self, ddd_root: str = None) -> Dict[str, Any]:
        """Get statistics for vector databases.

        Args:
            ddd_root: Specific DDD_ROOT to get stats for, or None for all

        Returns:
            Dictionary with statistics
        """
        if ddd_root:
            db = self.get_or_create_database(ddd_root)
            if db:
                return db.get_statistics()
            return {"status": "unavailable"}

        # Return stats for all databases
        stats = {
            "total_databases": len(self.databases),
            "databases": {}
        }

        for root, db in self.databases.items():
            stats["databases"][root] = db.get_statistics()

        return stats

    def invalidate_cache(self, ddd_root: str = None):
        """Invalidate cache for specific or all DDD_ROOT directories.

        Args:
            ddd_root: Specific DDD_ROOT to invalidate, or None for all
        """
        if ddd_root:
            if ddd_root in self.databases:
                del self.databases[ddd_root]
            if ddd_root in self.metadata:
                del self.metadata[ddd_root]
            self.logger.info(f"🗑️  Invalidated cache for: {ddd_root}")
        else:
            self.databases.clear()
            self.metadata.clear()
            self.logger.info("🗑️  Invalidated all vector database caches")

    def cleanup_old_caches(self, max_age_hours: int = 168):  # 1 week default
        """Clean up old cache files.

        Args:
            max_age_hours: Maximum age of cache files in hours
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600

            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    if current_time - cache_file.stat().st_mtime > max_age_seconds:
                        cache_file.unlink()
                        self.logger.info(f"🗑️  Removed old cache file: {cache_file.name}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove cache file {cache_file}: {e}")

        except Exception as e:
            self.logger.warning(f"Failed to cleanup old caches: {e}")
