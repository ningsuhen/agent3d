"""
In-Memory Vector Database for Repository Indexing

This module provides vector database functionality to index and search
the entire repository for better context-aware orchestration.
"""

import os
import logging
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


@dataclass
class CodeChunk:
    """Represents a chunk of code with metadata."""
    file_path: str
    content: str
    start_line: int
    end_line: int
    chunk_type: str  # 'function', 'class', 'module', 'documentation', 'test'
    language: str
    size: int
    hash: str
    metadata: Dict[str, Any]


class RepositoryVectorDB:
    """In-memory vector database for repository code indexing."""

    def __init__(self, logger: logging.Logger = None, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the vector database.

        Args:
            logger: Logger instance
            model_name: Sentence transformer model name
        """
        self.logger = logger or logging.getLogger(__name__)
        self.model_name = model_name
        self.model = None
        self.index = None
        self.chunks: List[CodeChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        self.dimension = 384  # Default for all-MiniLM-L6-v2

        self._initialize_model()
        self._initialize_index()

    def _initialize_model(self):
        """Initialize the sentence transformer model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.logger.warning("sentence-transformers not available. Vector search disabled.")
            return

        try:
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            self.logger.info(f"✅ Initialized sentence transformer: {self.model_name} (dim: {self.dimension})")
        except Exception as e:
            self.logger.error(f"Failed to initialize sentence transformer: {e}")
            self.model = None

    def _initialize_index(self):
        """Initialize the FAISS index."""
        if not FAISS_AVAILABLE or not self.model:
            self.logger.warning("FAISS not available or model not initialized. Using fallback search.")
            return

        try:
            # Use IndexFlatIP for cosine similarity
            self.index = faiss.IndexFlatIP(self.dimension)
            self.logger.info(f"✅ Initialized FAISS index (dimension: {self.dimension})")
        except Exception as e:
            self.logger.error(f"Failed to initialize FAISS index: {e}")
            self.index = None

    def index_repository(self, repo_path: str, exclude_patterns: List[str] = None) -> Dict[str, Any]:
        """Index the entire repository.

        Args:
            repo_path: Path to the repository root
            exclude_patterns: Patterns to exclude from indexing

        Returns:
            Indexing statistics with performance metrics
        """
        start_time = time.time()

        if exclude_patterns is None:
            exclude_patterns = [
                '.git', '__pycache__', '.pytest_cache', 'node_modules',
                '.venv', 'venv', '.env', '.agent3d-tmp', '.DS_Store',
                '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib'
            ]

        self.logger.info(f"🔍 Starting repository indexing: {repo_path}")

        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        stats = {
            "files_processed": 0,
            "chunks_created": 0,
            "total_size": 0,
            "languages": {},
            "chunk_types": {},
            "errors": [],
            "performance": {
                "start_time": start_time,
                "file_scan_time": 0,
                "chunking_time": 0,
                "embedding_time": 0,
                "total_time": 0
            }
        }

        # Clear existing data
        self.chunks.clear()

        # Phase 1: File scanning and discovery
        scan_start = time.time()
        files_to_index = self._get_files_to_index(repo_path, exclude_patterns)
        stats["performance"]["file_scan_time"] = time.time() - scan_start

        self.logger.info(f"📁 Found {len(files_to_index)} files to index")

        # Phase 2: File processing and chunking
        chunking_start = time.time()
        for i, file_path in enumerate(files_to_index):
            try:
                file_stats = self._index_file(file_path, repo_path)
                stats["files_processed"] += 1
                stats["chunks_created"] += file_stats["chunks"]
                stats["total_size"] += file_stats["size"]

                # Update language stats
                lang = file_stats["language"]
                stats["languages"][lang] = stats["languages"].get(lang, 0) + 1

                # Update chunk type stats
                for chunk_type, count in file_stats["chunk_types"].items():
                    stats["chunk_types"][chunk_type] = stats["chunk_types"].get(chunk_type, 0) + count

                # Progress logging for large repositories
                if (i + 1) % 50 == 0:
                    self.logger.info(f"📊 Processed {i + 1}/{len(files_to_index)} files...")

            except Exception as e:
                error_msg = f"Failed to index {file_path}: {e}"
                self.logger.warning(error_msg)
                stats["errors"].append(error_msg)

        stats["performance"]["chunking_time"] = time.time() - chunking_start

        # Phase 3: Vector embedding and indexing
        embedding_start = time.time()
        if self.chunks and self.model:
            self.logger.info(f"🔧 Building vector embeddings for {len(self.chunks)} chunks...")
            self._build_vector_index()
        stats["performance"]["embedding_time"] = time.time() - embedding_start

        # Calculate total time
        total_time = time.time() - start_time
        stats["performance"]["total_time"] = total_time

        # Log performance summary
        perf = stats["performance"]
        self.logger.info(f"✅ Repository indexing completed in {total_time:.2f}s:")
        self.logger.info(f"   📁 File scan: {perf['file_scan_time']:.2f}s")
        self.logger.info(f"   ✂️  Chunking: {perf['chunking_time']:.2f}s")
        self.logger.info(f"   🔧 Embeddings: {perf['embedding_time']:.2f}s")
        self.logger.info(f"   📊 Result: {stats['chunks_created']} chunks from {stats['files_processed']} files")

        return stats

    def _get_files_to_index(self, repo_path: Path, exclude_patterns: List[str]) -> List[Path]:
        """Get list of files to index."""
        files_to_index = []

        # Supported file extensions
        supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
            '.md', '.rst', '.txt', '.yml', '.yaml', '.json', '.xml', '.html',
            '.css', '.scss', '.less', '.sql', '.sh', '.bash', '.zsh'
        }

        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                # Check if file should be excluded
                if self._should_exclude_file(file_path, repo_path, exclude_patterns):
                    continue

                # Check if file extension is supported
                if file_path.suffix.lower() in supported_extensions:
                    files_to_index.append(file_path)

        return files_to_index

    def _should_exclude_file(self, file_path: Path, repo_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded from indexing."""
        relative_path = file_path.relative_to(repo_path)
        path_str = str(relative_path)

        for pattern in exclude_patterns:
            if pattern in path_str or file_path.name.startswith('.'):
                return True

        # Skip very large files (>1MB)
        try:
            if file_path.stat().st_size > 1024 * 1024:
                return True
        except:
            return True

        return False

    def _index_file(self, file_path: Path, repo_path: Path) -> Dict[str, Any]:
        """Index a single file."""
        relative_path = str(file_path.relative_to(repo_path))
        language = self._detect_language(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Could not read file: {e}")

        file_stats = {
            "chunks": 0,
            "size": len(content),
            "language": language,
            "chunk_types": {}
        }

        # Create chunks based on file type
        chunks = self._create_chunks(content, relative_path, language)

        for chunk in chunks:
            self.chunks.append(chunk)
            file_stats["chunks"] += 1
            chunk_type = chunk.chunk_type
            file_stats["chunk_types"][chunk_type] = file_stats["chunk_types"].get(chunk_type, 0) + 1

        return file_stats

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()

        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.md': 'markdown',
            '.rst': 'restructuredtext',
            '.txt': 'text',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh'
        }

        return language_map.get(ext, 'unknown')

    def _create_chunks(self, content: str, file_path: str, language: str) -> List[CodeChunk]:
        """Create chunks from file content."""
        chunks = []
        lines = content.split('\n')

        if language == 'python':
            chunks.extend(self._create_python_chunks(content, file_path, lines))
        elif language in ['javascript', 'typescript']:
            chunks.extend(self._create_js_chunks(content, file_path, lines))
        elif language == 'markdown':
            chunks.extend(self._create_markdown_chunks(content, file_path, lines))
        else:
            # Generic chunking for other languages
            chunks.extend(self._create_generic_chunks(content, file_path, language, lines))

        return chunks

    def _create_python_chunks(self, content: str, file_path: str, lines: List[str]) -> List[CodeChunk]:
        """Create chunks for Python files."""
        chunks = []

        # Simple function/class detection
        current_chunk = []
        current_start = 1
        chunk_type = "module"

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Detect function or class definitions
            if stripped.startswith('def ') or stripped.startswith('class '):
                # Save previous chunk if it exists
                if current_chunk:
                    chunk_content = '\n'.join(current_chunk)
                    if chunk_content.strip():
                        chunks.append(self._create_chunk(
                            chunk_content, file_path, current_start, i-1,
                            chunk_type, "python"
                        ))

                # Start new chunk
                current_chunk = [line]
                current_start = i
                chunk_type = "function" if stripped.startswith('def ') else "class"
            else:
                current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            if chunk_content.strip():
                chunks.append(self._create_chunk(
                    chunk_content, file_path, current_start, len(lines),
                    chunk_type, "python"
                ))

        return chunks

    def _create_js_chunks(self, content: str, file_path: str, lines: List[str]) -> List[CodeChunk]:
        """Create chunks for JavaScript/TypeScript files."""
        chunks = []

        # Simple function detection for JS/TS
        current_chunk = []
        current_start = 1
        chunk_type = "module"

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Detect function definitions
            if ('function ' in stripped or
                stripped.startswith('const ') and '=>' in stripped or
                stripped.startswith('export function')):

                # Save previous chunk
                if current_chunk:
                    chunk_content = '\n'.join(current_chunk)
                    if chunk_content.strip():
                        chunks.append(self._create_chunk(
                            chunk_content, file_path, current_start, i-1,
                            chunk_type, "javascript"
                        ))

                # Start new chunk
                current_chunk = [line]
                current_start = i
                chunk_type = "function"
            else:
                current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            if chunk_content.strip():
                chunks.append(self._create_chunk(
                    chunk_content, file_path, current_start, len(lines),
                    chunk_type, "javascript"
                ))

        return chunks

    def _create_markdown_chunks(self, content: str, file_path: str, lines: List[str]) -> List[CodeChunk]:
        """Create chunks for Markdown files."""
        chunks = []

        current_chunk = []
        current_start = 1
        chunk_type = "documentation"

        for i, line in enumerate(lines, 1):
            # Detect headers
            if line.startswith('#'):
                # Save previous chunk
                if current_chunk:
                    chunk_content = '\n'.join(current_chunk)
                    if chunk_content.strip():
                        chunks.append(self._create_chunk(
                            chunk_content, file_path, current_start, i-1,
                            chunk_type, "markdown"
                        ))

                # Start new chunk
                current_chunk = [line]
                current_start = i
                chunk_type = "documentation"
            else:
                current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            if chunk_content.strip():
                chunks.append(self._create_chunk(
                    chunk_content, file_path, current_start, len(lines),
                    chunk_type, "markdown"
                ))

        return chunks

    def _create_generic_chunks(self, content: str, file_path: str, language: str, lines: List[str]) -> List[CodeChunk]:
        """Create generic chunks for other file types."""
        chunks = []

        # Split into chunks of ~50 lines
        chunk_size = 50
        for i in range(0, len(lines), chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunk_content = '\n'.join(chunk_lines)

            if chunk_content.strip():
                chunks.append(self._create_chunk(
                    chunk_content, file_path, i + 1, i + len(chunk_lines),
                    "module", language
                ))

        return chunks

    def _create_chunk(self, content: str, file_path: str, start_line: int,
                     end_line: int, chunk_type: str, language: str) -> CodeChunk:
        """Create a CodeChunk object."""
        content_hash = hashlib.md5(content.encode()).hexdigest()

        # Extract metadata
        metadata = {
            "lines_count": end_line - start_line + 1,
            "has_imports": "import " in content or "from " in content,
            "has_tests": "test" in file_path.lower() or "def test_" in content,
            "has_classes": "class " in content,
            "has_functions": "def " in content or "function " in content,
            "complexity_score": self._estimate_complexity(content)
        }

        return CodeChunk(
            file_path=file_path,
            content=content,
            start_line=start_line,
            end_line=end_line,
            chunk_type=chunk_type,
            language=language,
            size=len(content),
            hash=content_hash,
            metadata=metadata
        )

    def _estimate_complexity(self, content: str) -> int:
        """Estimate code complexity based on simple heuristics."""
        complexity = 0

        # Count control structures
        complexity += content.count('if ')
        complexity += content.count('for ')
        complexity += content.count('while ')
        complexity += content.count('try:')
        complexity += content.count('except')
        complexity += content.count('def ')
        complexity += content.count('class ')

        return complexity

    def _build_vector_index(self):
        """Build the vector index from chunks."""
        if not self.model or not self.chunks:
            self.logger.warning("Cannot build vector index: model or chunks not available")
            return

        self.logger.info(f"🔧 Building vector index for {len(self.chunks)} chunks...")

        try:
            # Create embeddings for all chunks
            texts = [self._prepare_text_for_embedding(chunk) for chunk in self.chunks]
            embeddings = self.model.encode(texts, show_progress_bar=True)

            # Normalize embeddings for cosine similarity
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

            self.embeddings = embeddings

            # Add to FAISS index if available
            if self.index is not None:
                self.index.add(embeddings.astype(np.float32))
                self.logger.info(f"✅ Vector index built: {len(self.chunks)} chunks indexed")
            else:
                self.logger.info(f"✅ Embeddings created: {len(self.chunks)} chunks (no FAISS index)")

        except Exception as e:
            self.logger.error(f"Failed to build vector index: {e}")

    def _prepare_text_for_embedding(self, chunk: CodeChunk) -> str:
        """Prepare chunk text for embedding."""
        # Combine file path, chunk type, and content for better context
        text_parts = [
            f"File: {chunk.file_path}",
            f"Type: {chunk.chunk_type}",
            f"Language: {chunk.language}",
            chunk.content[:1000]  # Limit content length
        ]

        return " | ".join(text_parts)

    def search(self, query: str, top_k: int = 10, filter_language: str = None,
              filter_chunk_type: str = None) -> List[Tuple[CodeChunk, float]]:
        """Search for relevant code chunks.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_language: Filter by programming language
            filter_chunk_type: Filter by chunk type

        Returns:
            List of (chunk, similarity_score) tuples
        """
        if not self.model or not self.chunks:
            self.logger.warning("Search not available: model or chunks not initialized")
            return []

        try:
            # Create query embedding
            query_embedding = self.model.encode([query])
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

            if self.index is not None and self.embeddings is not None:
                # Use FAISS for fast search
                scores, indices = self.index.search(query_embedding.astype(np.float32), min(top_k * 2, len(self.chunks)))

                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx < len(self.chunks):
                        chunk = self.chunks[idx]

                        # Apply filters
                        if filter_language and chunk.language != filter_language:
                            continue
                        if filter_chunk_type and chunk.chunk_type != filter_chunk_type:
                            continue

                        results.append((chunk, float(score)))

                        if len(results) >= top_k:
                            break

                return results

            else:
                # Fallback to numpy similarity search
                if self.embeddings is None:
                    return []

                similarities = np.dot(self.embeddings, query_embedding.T).flatten()
                top_indices = np.argsort(similarities)[::-1]

                results = []
                for idx in top_indices:
                    chunk = self.chunks[idx]

                    # Apply filters
                    if filter_language and chunk.language != filter_language:
                        continue
                    if filter_chunk_type and chunk.chunk_type != filter_chunk_type:
                        continue

                    results.append((chunk, float(similarities[idx])))

                    if len(results) >= top_k:
                        break

                return results

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    def get_file_context(self, file_path: str) -> List[CodeChunk]:
        """Get all chunks for a specific file."""
        return [chunk for chunk in self.chunks if chunk.file_path == file_path]

    def get_related_files(self, query: str, top_k: int = 5) -> List[str]:
        """Get files most related to the query."""
        search_results = self.search(query, top_k=top_k * 2)

        # Group by file and get unique files
        files_seen = set()
        related_files = []

        for chunk, score in search_results:
            if chunk.file_path not in files_seen:
                files_seen.add(chunk.file_path)
                related_files.append(chunk.file_path)

                if len(related_files) >= top_k:
                    break

        return related_files

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        if not self.chunks:
            return {"status": "empty"}

        stats = {
            "total_chunks": len(self.chunks),
            "total_files": len(set(chunk.file_path for chunk in self.chunks)),
            "languages": {},
            "chunk_types": {},
            "total_size": sum(chunk.size for chunk in self.chunks),
            "has_embeddings": self.embeddings is not None,
            "has_index": self.index is not None,
            "model_available": self.model is not None
        }

        for chunk in self.chunks:
            # Language stats
            lang = chunk.language
            stats["languages"][lang] = stats["languages"].get(lang, 0) + 1

            # Chunk type stats
            chunk_type = chunk.chunk_type
            stats["chunk_types"][chunk_type] = stats["chunk_types"].get(chunk_type, 0) + 1

        return stats