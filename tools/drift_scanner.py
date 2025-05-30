#!/usr/bin/env python3
"""
Multi-mode drift scanner for Agent3D framework.
Detects various types of drift between documentation and implementation.

Supported drift detection modes:
- tc-mapping: TC ID mapping between TEST-CASES.md and test implementations
- ft-mapping: FT ID mapping between FEATURES.md and test implementations
- ft-tc-mapping: FT-* ↔ TC-* relationship mapping and validation
- code-coverage: Test coverage analysis and missing test detection
- test-quality: Test quality validation to ensure tests actually test project code
- doc-code: Documentation-code signature drift detection
- feature-impl: Feature implementation status drift
- requirements: Requirements traceability drift
- dependencies: Package dependency drift detection
- config: Configuration drift detection
- links: Broken link and reference detection
- all: Run all drift detection modes
"""

import re
import yaml
import os
import subprocess
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field, asdict

# Import vector database manager for enhanced file discovery
try:
    from vector_db_manager import MultiRootVectorDBManager
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    MultiRootVectorDBManager = None

# Agent3D temporary directory for drift scanner operations
AGENT3D_TMP_DIR = Path('.agent3d-tmp')

def ensure_tmp_directory() -> Path:
    """Ensure the Agent3D temporary directory exists and return its path."""
    tmp_dir = AGENT3D_TMP_DIR
    tmp_dir.mkdir(exist_ok=True)

    # Create subdirectories for different types of outputs
    (tmp_dir / 'drift-reports').mkdir(exist_ok=True)
    (tmp_dir / 'analysis-cache').mkdir(exist_ok=True)
    (tmp_dir / 'logs').mkdir(exist_ok=True)

    return tmp_dir

def get_default_output_path(mode: str) -> str:
    """Get the default output path for a given drift analysis mode."""
    tmp_dir = ensure_tmp_directory()
    return str(tmp_dir / 'drift-reports' / f'{mode}-drift-report.yaml')

def get_log_file_path() -> str:
    """Get the log file path for the current analysis session."""
    tmp_dir = ensure_tmp_directory()
    timestamp = os.popen('date +%Y%m%d_%H%M%S').read().strip()
    return str(tmp_dir / 'logs' / f'drift-analysis-{timestamp}.log')

def log_analysis_start(mode: str, root_dir: str, log_file: str) -> None:
    """Log the start of a drift analysis session."""
    with open(log_file, 'w') as f:
        f.write(f"=== Agent3D Drift Analysis Session ===\n")
        f.write(f"Timestamp: {os.popen('date').read().strip()}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Root Directory: {root_dir}\n")
        f.write(f"Log File: {log_file}\n")
        f.write(f"{'='*50}\n\n")

class ConfigurationManager:
    """Manages Agent3D configuration from .agent3d-config.yml"""

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.config_file = self.root_dir / '.agent3d-config.yml'
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from .agent3d-config.yml"""
        if not self.config_file.exists():
            print(f"⚠️  Configuration file not found at {self.config_file}")
            print("   Using default identifier patterns")
            return self._get_default_config()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print(f"✅ Loaded configuration from {self.config_file}")
                return config
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            print("   Using default identifier patterns")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration when .agent3d-config.yml is not available"""
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

    def get_identifier_patterns(self) -> Dict:
        """Get all identifier patterns from configuration"""
        return self.config.get('identifier_patterns', {})

    def get_pattern_config(self, prefix: str) -> Optional[Dict]:
        """Get configuration for a specific identifier pattern"""
        patterns = self.get_identifier_patterns()
        return patterns.get(prefix)

    def get_enabled_patterns(self) -> List[str]:
        """Get list of enabled identifier patterns"""
        drift_config = self.config.get('drift_detection', {})
        return drift_config.get('enabled_patterns', ['TC-', 'FT-', 'REQ-'])

    def get_primary_patterns(self) -> List[str]:
        """Get list of primary (non-deprecated) patterns"""
        drift_config = self.config.get('drift_detection', {})
        return drift_config.get('primary_patterns', ['TC-', 'FT-', 'REQ-'])

    def is_relationship_validation_enabled(self) -> bool:
        """Check if relationship validation is enabled"""
        drift_config = self.config.get('drift_detection', {})
        return drift_config.get('relationship_validation', True)

    def get_pattern_for_prefix(self, prefix: str, flexible: bool = False) -> str:
        """Get regex pattern for a specific prefix"""
        config = self.get_pattern_config(prefix)
        if not config:
            # Fallback pattern
            return f'{prefix}[A-Za-z0-9-]+' if flexible else f'{prefix}[A-Z0-9]+-\\d+[a-z]?'

        pattern_key = 'flexible_pattern' if flexible else 'pattern'
        return config.get(pattern_key, f'{prefix}[A-Za-z0-9-]+')

    def get_primary_files_for_pattern(self, prefix: str) -> List[str]:
        """Get primary files where this pattern is defined"""
        config = self.get_pattern_config(prefix)
        return config.get('primary_files', []) if config else []

    def get_relationship_targets(self, prefix: str) -> List[str]:
        """Get which patterns this prefix can reference"""
        config = self.get_pattern_config(prefix)
        return config.get('relationship_targets', []) if config else []

    def get_python_paths_config(self) -> Dict:
        """Get Python path configuration for Code Location validation"""
        # First check under project_settings (new location)
        project_settings = self.config.get('project_settings', {})
        if 'python_paths' in project_settings:
            return project_settings['python_paths']

        # Fallback to root level (legacy location) for backward compatibility
        return self.config.get('python_paths', {})

    def get_source_directories(self) -> List[str]:
        """Get source directories for Python module resolution"""
        python_config = self.get_python_paths_config()
        return python_config.get('source_directories', ['tools', 'src', 'lib', 'scripts', 'app', '.'])

    def get_framework_modules(self) -> Dict[str, str]:
        """Get framework-specific module mappings"""
        python_config = self.get_python_paths_config()
        return python_config.get('framework_modules', {})

    def get_resolution_strategies(self) -> List[str]:
        """Get module resolution strategies in order of preference"""
        python_config = self.get_python_paths_config()
        return python_config.get('resolution_strategies', ['pyproject_toml', 'direct_path', 'flat_structure', 'nested_structure', 'package_init'])

    def get_flat_module_directories(self) -> List[str]:
        """Get directories with flat module structure"""
        python_config = self.get_python_paths_config()
        package_structure = python_config.get('package_structure', {})
        return package_structure.get('flat_modules', ['tools', 'scripts', 'utils'])

    def get_nested_module_directories(self) -> List[str]:
        """Get directories with nested module structure"""
        python_config = self.get_python_paths_config()
        package_structure = python_config.get('package_structure', {})
        return package_structure.get('nested_modules', ['src', 'lib', 'app'])

class GitChangeDetector:
    """Detects changed files using Git for optimized drift scanning."""

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)

    def is_git_repository(self) -> bool:
        """Check if the current directory is a Git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_changed_files(self, since: str = 'HEAD~1', include_untracked: bool = True) -> Set[Path]:
        """Get list of changed files since a specific commit/branch."""
        if not self.is_git_repository():
            print("⚠️  Not a Git repository - change-based scanning disabled")
            return set()

        changed_files = set()

        try:
            # Get modified and staged files
            result = subprocess.run(
                ['git', 'diff', '--name-only', since],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True
            )

            for file_path in result.stdout.strip().split('\n'):
                if file_path:  # Skip empty lines
                    full_path = self.root_dir / file_path
                    if full_path.exists():
                        changed_files.add(full_path)

            # Get staged files (different from committed)
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True
            )

            for file_path in result.stdout.strip().split('\n'):
                if file_path:  # Skip empty lines
                    full_path = self.root_dir / file_path
                    if full_path.exists():
                        changed_files.add(full_path)

            # Get untracked files if requested
            if include_untracked:
                result = subprocess.run(
                    ['git', 'ls-files', '--others', '--exclude-standard'],
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )

                for file_path in result.stdout.strip().split('\n'):
                    if file_path:  # Skip empty lines
                        full_path = self.root_dir / file_path
                        if full_path.exists():
                            changed_files.add(full_path)

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git command failed: {e}")
            return set()

        return changed_files

    def get_changed_files_in_pr(self, base_branch: str = 'main') -> Set[Path]:
        """Get files changed in current branch compared to base branch."""
        return self.get_changed_files(since=base_branch)

    def get_recently_changed_files(self, days: int = 7) -> Set[Path]:
        """Get files changed in the last N days."""
        since = f'--since="{days} days ago"'

        try:
            result = subprocess.run(
                ['git', 'log', '--name-only', '--pretty=format:', since],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True
            )

            changed_files = set()
            for file_path in result.stdout.strip().split('\n'):
                if file_path:  # Skip empty lines
                    full_path = self.root_dir / file_path
                    if full_path.exists():
                        changed_files.add(full_path)

            return changed_files

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git command failed: {e}")
            return set()

    def filter_files_by_changes(self, all_files: List[Tuple[Path, str]], changed_files: Set[Path]) -> List[Tuple[Path, str]]:
        """Filter a list of files to only include changed files."""
        if not changed_files:
            return all_files  # If no changed files detected, scan all files

        filtered_files = []
        for file_path, language in all_files:
            if file_path in changed_files:
                filtered_files.append((file_path, language))

        return filtered_files

@dataclass
class TestFunction:
    """Represents a test function found in code."""
    file: str
    function: str
    full_name: str
    type: str  # 'class_method', 'standalone', 'describe_block', etc.
    class_name: Optional[str] = None
    tc_ids: List[str] = None
    line_number: Optional[int] = None
    # Test quality validation fields
    imports_project_code: bool = False
    calls_project_functions: bool = False
    uses_only_mocks: bool = False
    test_quality_score: float = 0.0
    quality_issues: List[str] = None

    def __post_init__(self):
        if self.tc_ids is None:
            self.tc_ids = []
        if self.quality_issues is None:
            self.quality_issues = []

@dataclass
class TestCase:
    """Represents a test case from TEST-CASES.md."""
    tc_id: str
    title: str
    status: str  # 'completed', 'pending', 'skipped'
    execution_type: str  # 'Manual', 'Automated', 'Partial'
    priority: str  # 'High', 'Medium', 'Low'
    is_sub_case: bool = False
    parent_tc_id: Optional[str] = None
    ft_id: Optional[str] = None  # Associated FT-* feature ID

@dataclass
class Feature:
    """Represents a feature from FEATURES.md."""
    ft_id: str
    title: str
    description: str
    status: str  # 'completed', 'pending', 'skipped'
    criteria: str  # Acceptance criteria
    is_sub_feature: bool = False
    parent_ft_id: Optional[str] = None
    tc_ids: List[str] = field(default_factory=list)  # Associated TC-* test case IDs
    code_location: Optional[str] = None  # Implementation location for feature-implementation analysis

@dataclass
class FeatureTestMapping:
    """Represents a mapping between FT-* features and TC-* test cases."""
    ft_id: str
    feature_title: str
    tc_ids: List[str]
    missing_tests: List[str]  # Features without test coverage
    orphaned_tests: List[str]  # Tests without feature coverage
    mapping_issues: List[str]  # Specific mapping problems

@dataclass
class CoverageIssue:
    """Represents a code coverage issue."""
    file: str
    function: str
    line_number: Optional[int] = None
    issue_type: str = "missing_test"  # missing_test, untested_function, orphaned_test
    severity: str = "medium"  # low, medium, high

@dataclass
class DocumentationIssue:
    """Represents a documentation-code drift issue."""
    file: str
    function_or_class: str
    issue_type: str  # signature_mismatch, missing_docs, outdated_docs
    expected: str
    actual: str
    line_number: Optional[int] = None

@dataclass
class FeatureIssue:
    """Represents a feature implementation drift issue."""
    feature_id: str
    feature_name: str
    documented_status: str  # completed, pending, skipped
    actual_status: str  # implemented, missing, partial
    issue_type: str  # status_mismatch, missing_implementation, undocumented_feature

@dataclass
class CodeLocationIssue:
    """Represents a Code Location field analysis issue."""
    feature_id: str
    feature_name: str
    code_location: Optional[str]
    issue_type: str  # 'missing_code_location', 'invalid_path', 'file_not_found', 'class_not_found', 'multiple_locations_invalid'
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    suggestion: str
    expected_path: Optional[str] = None
    actual_status: Optional[str] = None

@dataclass
class TestQualityIssue:
    """Represents a test quality issue."""
    test_file: str
    test_function: str
    issue_type: str  # 'no_project_imports', 'only_mock_data', 'no_function_calls', 'poor_coverage'
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    suggestion: str
    line_number: Optional[int] = None



@dataclass
class FeatureTestDriftIssue:
    """Represents a specific feature-test drift issue."""
    feature_name: str
    issue_type: str  # 'feature_without_tests', 'tests_without_feature', 'status_mismatch', 'incomplete_coverage'
    severity: str  # 'critical', 'warning', 'info'
    description: str
    suggested_action: str
    related_test_cases: List[str] = None
    related_test_functions: List[str] = None

    def __post_init__(self):
        if self.related_test_cases is None:
            self.related_test_cases = []
        if self.related_test_functions is None:
            self.related_test_functions = []

@dataclass
class DriftIssue:
    """Represents a specific drift detection issue with severity and suggestions."""
    strategy: str
    drift_type: str
    severity: str  # 'critical', 'warning', 'info'
    description: str
    location: str
    expected: str
    actual: str
    suggestion: str
    file_path: str = None
    line_number: int = None

@dataclass
class DuplicateTCIssue:
    """Represents a TC ID that is used in multiple test functions."""
    tc_id: str
    test_functions: List[TestFunction]
    issue_type: str = 'duplicate_tc_id'
    severity: str = 'warning'
    description: str = ''
    suggestion: str = ''

    def __post_init__(self):
        if not self.description:
            self.description = f"TC ID '{self.tc_id}' is used in {len(self.test_functions)} different test functions"
        if not self.suggestion:
            self.suggestion = f"Each TC ID should be used in only one test function. Consider using sub-test cases with parameters or renaming duplicate TC IDs to unique identifiers."

@dataclass
class DriftReport:
    """Complete multi-mode drift analysis report."""
    mode: str
    # TC Mapping (original)
    test_cases_without_implementations: List[TestCase] = None
    implementations_without_test_cases: List[TestFunction] = None
    tc_mappings: Dict[str, List[TestFunction]] = None
    orphaned_tc_ids: List[str] = None
    # Duplicate TC ID Detection
    duplicate_tc_issues: List[DuplicateTCIssue] = None
    # FT Mapping (new)
    features_without_tests: List[Feature] = None
    tests_without_features: List[TestFunction] = None
    ft_mappings: Dict[str, List[TestFunction]] = None
    ft_tc_mappings: List[FeatureTestMapping] = None
    orphaned_ft_ids: List[str] = None
    # Code Coverage
    coverage_issues: List[CoverageIssue] = None
    coverage_percentage: float = None
    # Documentation-Code Drift
    documentation_issues: List[DocumentationIssue] = None
    # Feature Implementation Drift
    feature_issues: List[FeatureIssue] = None
    # Code Location Analysis
    code_location_issues: List[CodeLocationIssue] = None
    # Test Quality Validation
    test_quality_issues: List[TestQualityIssue] = None
    low_quality_tests: List[TestFunction] = None
    test_quality_score: float = None
    # Enhanced Drift Issues (with severity and suggestions)
    drift_issues: List[DriftIssue] = None
    # General
    metadata: Dict = None

    def __post_init__(self):
        if self.test_cases_without_implementations is None:
            self.test_cases_without_implementations = []
        if self.implementations_without_test_cases is None:
            self.implementations_without_test_cases = []
        if self.tc_mappings is None:
            self.tc_mappings = {}
        if self.orphaned_tc_ids is None:
            self.orphaned_tc_ids = []
        # Duplicate TC ID fields
        if self.duplicate_tc_issues is None:
            self.duplicate_tc_issues = []
        # FT Mapping fields
        if self.features_without_tests is None:
            self.features_without_tests = []
        if self.tests_without_features is None:
            self.tests_without_features = []
        if self.ft_mappings is None:
            self.ft_mappings = {}
        if self.ft_tc_mappings is None:
            self.ft_tc_mappings = []
        if self.orphaned_ft_ids is None:
            self.orphaned_ft_ids = []
        # Other fields
        if self.coverage_issues is None:
            self.coverage_issues = []
        if self.documentation_issues is None:
            self.documentation_issues = []
        if self.feature_issues is None:
            self.feature_issues = []
        # Code Location fields
        if self.code_location_issues is None:
            self.code_location_issues = []
        # Test Quality fields
        if self.test_quality_issues is None:
            self.test_quality_issues = []
        if self.low_quality_tests is None:
            self.low_quality_tests = []
        if self.drift_issues is None:
            self.drift_issues = []
        if self.metadata is None:
            self.metadata = {}

class LanguageDetector:
    """Detects programming language and provides language-specific patterns."""

    LANGUAGE_PATTERNS = {
        'python': {
            'file_patterns': ['test_*.py', '*_test.py', 'tests/*.py', 'test/**/*.py'],
            'test_function_patterns': [
                r'def\s+(test_\w+)',  # def test_something
                r'def\s+(\w*test\w*)',  # def something_test
            ],
            'class_patterns': [
                r'class\s+(\w*Test\w*)\s*\([^)]*\):(.*?)(?=class|\Z)',
            ],
            'tc_id_pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
            'comment_patterns': ['#', '"""', "'''"],
        },
        'javascript': {
            'file_patterns': ['*.test.js', '*.spec.js', 'test/**/*.js', 'tests/**/*.js', '__tests__/**/*.js'],
            'test_function_patterns': [
                r'(?:it|test)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',  # it('test name') or test('test name')
                r'(?:describe)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',  # describe('test suite')
            ],
            'class_patterns': [],
            'tc_id_pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
            'comment_patterns': ['//', '/*', '*/', '/**'],
        },
        'java': {
            'file_patterns': ['*Test.java', '*Tests.java', 'src/test/**/*.java'],
            'test_function_patterns': [
                r'@Test[^}]*?(?:public|private|protected)?\s+\w+\s+(\w+)\s*\(',
                r'(?:public|private|protected)\s+\w+\s+(test\w+)\s*\(',
            ],
            'class_patterns': [
                r'(?:public\s+)?class\s+(\w*Test\w*)\s*(?:extends\s+\w+)?\s*\{(.*?)(?=class|\Z)',
            ],
            'tc_id_pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
            'comment_patterns': ['//', '/*', '*/', '/**', '@DisplayName'],
        },

        'rust': {
            'file_patterns': ['**/tests/*.rs', 'src/**/*test*.rs'],
            'test_function_patterns': [
                r'#\[test\]\s*(?:async\s+)?fn\s+(\w+)',  # #[test] fn test_name
            ],
            'class_patterns': [],
            'tc_id_pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
            'comment_patterns': ['//'],
        }
    }

    @classmethod
    def detect_language(cls, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        suffix = file_path.suffix.lower()
        if suffix == '.py':
            return 'python'
        elif suffix in ['.js', '.ts', '.jsx', '.tsx']:
            return 'javascript'
        elif suffix == '.java':
            return 'java'
        elif suffix == '.rs':
            return 'rust'
        return None

    @classmethod
    def get_patterns(cls, language: str) -> Dict:
        """Get language-specific patterns."""
        return cls.LANGUAGE_PATTERNS.get(language, {})

class TestCaseParser:
    """Parses test cases from merged FT-TC structure in docs/features/ directory."""

    def __init__(self, features_dir: str = 'docs/features',
                 config_manager: Optional[ConfigurationManager] = None):
        self.features_dir = features_dir
        self.config_manager = config_manager or ConfigurationManager('.')

    def parse_test_cases(self, vector_db_manager=None) -> List[TestCase]:
        """Parse test cases from merged FT-TC structure in docs/features/ directory.

        Args:
            vector_db_manager: Optional vector database manager for enhanced parsing
        """
        if not Path(self.features_dir).exists():
            print(f"⚠️  Features directory not found at {self.features_dir}")
            return []

        test_cases = []

        # Try vector-enhanced parsing first
        if vector_db_manager:
            print("🔍 Using vector-enhanced test case discovery...")
            test_cases = self._parse_test_cases_with_vector_db(vector_db_manager)
            if test_cases:
                print(f"✅ Found {len(test_cases)} test cases via vector search")
                return test_cases
            else:
                print("⚠️  Vector search found no test cases, falling back to regex parsing")

        # Fallback to traditional regex parsing
        try:
            # Parse all .md files in the features directory
            for feature_file in Path(self.features_dir).glob('*.md'):
                with open(feature_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_cases.extend(self._parse_merged_test_cases(content, str(feature_file)))
        except Exception as e:
            print(f"❌ Error reading features directory {self.features_dir}: {e}")
            return []

        return test_cases

    def _parse_test_cases_with_vector_db(self, vector_db_manager) -> List[TestCase]:
        """Parse test cases using vector database search for TC-* identifiers."""
        test_cases = []

        try:
            # Search for TC-* patterns in documentation with multiple strategies
            search_queries = [
                "TC- test case",
                "TC-AUTH test authentication",
                "TC-HTTP test HTTP",
                "TC-CORE test core functionality",
                "test case TC-",
                "**TC-"
            ]

            seen_tc_ids = set()

            for query in search_queries:
                # Try both with and without language filter
                for filter_lang in [None, "markdown"]:
                    tc_search_results = vector_db_manager.search(
                        self.config_manager.root_dir,
                        query,
                        top_k=20,
                        filter_language=filter_lang
                    )

                    # Process search results to extract test cases
                    for chunk, score in tc_search_results:
                        if score < 0.2:  # Lower threshold for broader search
                            continue

                        if hasattr(chunk, 'content'):
                            # Extract TC IDs and details from chunk content
                            # Main test case pattern: - [x] **TC-ID** - Description (ExecutionType, Priority) Status
                            main_tc_pattern = r'- \[([x~\s])\] \*\*(TC-[A-Z]+-\d+[a-z]?)\*\* - ([^(]+?)\s*\(([^,]+),\s*([^)]+)\).*'
                            # Sub-test case pattern: - [x] **TC-ID** - Description Status (no execution type/priority)
                            sub_tc_pattern = r'\s+- \[([x~\s])\] \*\*(TC-[A-Z]+-\d+[a-z]?)\*\* - (.+?)(?:\s+[🔶✅].*)?$'

                            current_execution_type = "Unknown"
                            current_priority = "Unknown"

                            # Process main test cases
                            matches = re.finditer(main_tc_pattern, chunk.content)
                            for match in matches:
                                status_char, tc_id, description, execution_type, priority = match.groups()
                                current_execution_type = execution_type.strip()
                                current_priority = priority.strip()

                                if tc_id not in seen_tc_ids:
                                    seen_tc_ids.add(tc_id)

                                    test_case = TestCase(
                                        tc_id=tc_id,
                                        title=description.strip(),
                                        execution_type=current_execution_type,
                                        priority=current_priority,
                                        status='complete' if status_char == 'x' else 'pending'
                                    )
                                    test_cases.append(test_case)

                            # Process sub-test cases
                            sub_matches = re.finditer(sub_tc_pattern, chunk.content, re.MULTILINE)
                            for match in sub_matches:
                                status_char, tc_id, description = match.groups()

                                if tc_id not in seen_tc_ids:
                                    seen_tc_ids.add(tc_id)

                                    test_case = TestCase(
                                        tc_id=tc_id,
                                        title=description.strip(),
                                        execution_type=current_execution_type,
                                        priority=current_priority,
                                        status='complete' if status_char == 'x' else 'pending'
                                    )
                                    test_cases.append(test_case)
                                    print(f"  ✅ Found test case: {tc_id} - {description.strip()[:50]}...")

            print(f"🔍 Vector search found {len(test_cases)} test cases")
            return test_cases

        except Exception as e:
            print(f"❌ Error in vector-enhanced test case parsing: {e}")
            return []

    def _parse_merged_test_cases(self, content: str, file_path: str) -> List[TestCase]:
        """Parse test cases from merged FT-TC structure content."""
        test_cases = []

        # Pattern to match test cases using configured TC pattern
        tc_strict_pattern = self.config_manager.get_pattern_for_prefix('TC-', flexible=False)

        # Main test case pattern: - [x] **TC-ID** - Description (ExecutionType, Priority) Status
        tc_pattern = rf'- \[([x~\s])\] \*\*({tc_strict_pattern})\*\* - ([^(]+?)\s*\(([^,]+),\s*([^)]+)\).*'

        # Sub-test case pattern: - [x] **TC-ID** - Description Status (no execution type/priority)
        sub_tc_pattern = rf'\s+- \[([x~\s])\] \*\*({tc_strict_pattern})\*\* - (.+?)(?:\s+[🔶✅].*)?$'

        lines = content.split('\n')
        current_execution_type = "Unknown"
        current_priority = "Unknown"

        for line_num, line in enumerate(lines, 1):
            # Match main test cases (with execution type and priority)
            match = re.match(tc_pattern, line.strip())
            if match:
                status_char, tc_id, description, execution_type, priority = match.groups()

                # Store current execution type and priority for sub-test cases
                current_execution_type = execution_type.strip()
                current_priority = priority.strip()

                test_case = TestCase(
                    tc_id=tc_id,
                    title=description.strip(),
                    execution_type=current_execution_type,
                    priority=current_priority,
                    status='complete' if status_char == 'x' else 'pending'
                )
                test_cases.append(test_case)

            # Match sub-test cases (inherit execution type and priority from parent)
            sub_match = re.match(sub_tc_pattern, line)
            if sub_match:
                status_char, tc_id, description = sub_match.groups()

                test_case = TestCase(
                    tc_id=tc_id,
                    title=description.strip(),
                    execution_type=current_execution_type,
                    priority=current_priority,
                    status='complete' if status_char == 'x' else 'pending'
                )
                test_cases.append(test_case)

        return test_cases

class FeatureParser:
    """Parses merged FT-TC structure from docs/features/ section files."""

    def __init__(self, features_dir: str = 'docs/features',
                 config_manager: Optional[ConfigurationManager] = None):
        self.features_dir = Path(features_dir)
        self.config_manager = config_manager or ConfigurationManager('.')

    def parse_features(self) -> List[Feature]:
        """Parse all section files in docs/features/ and extract features with test cases."""
        if not self.features_dir.exists():
            print(f"⚠️  Features directory not found at {self.features_dir}")
            # Fallback to old FEATURES.md structure
            return self._parse_legacy_features()

        features = []
        section_files = list(self.features_dir.glob('*.md'))

        if not section_files:
            print(f"⚠️  No section files found in {self.features_dir}")
            return self._parse_legacy_features()

        print(f"📁 Found {len(section_files)} section files in {self.features_dir}")

        for section_file in section_files:
            try:
                with open(section_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                section_features = self._parse_section_content(content, section_file.name)
                features.extend(section_features)
                print(f"   📄 {section_file.name}: {len(section_features)} features")
            except Exception as e:
                print(f"❌ Error reading {section_file}: {e}")
                continue

        return features

    def _parse_legacy_features(self) -> List[Feature]:
        """Fallback to parse old FEATURES.md structure."""
        legacy_file = 'docs/FEATURES.md'
        if not Path(legacy_file).exists():
            print(f"⚠️  Legacy FEATURES.md not found at {legacy_file}")
            return []

        try:
            with open(legacy_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._parse_legacy_content(content)
        except Exception as e:
            print(f"❌ Error reading {legacy_file}: {e}")
            return []

    def _parse_section_content(self, content: str, section_name: str) -> List[Feature]:
        """Parse content from a section file (e.g., core.md, passes.md) with merged FT-TC structure."""
        features = []

        # Pattern to match features: ## FT-CORE-001 - Feature Name
        ft_pattern = r'^## (FT-[A-Z]+-\d+) - (.+)$'

        # Pattern to match feature bullets with criteria
        criteria_pattern = r'- \*\*Criteria:\*\* (.+)'

        # Pattern to match Code Location field
        code_location_pattern = r'- \*\*Code Location:\*\* (.+)'

        # Pattern to match test cases: - [x] **TC-CORE-001** - Test Name (with status indicators)
        tc_pattern = r'^\s+- \[([x~\s])\] \*\*TC-[A-Z]+-\d+[a-z]?\*\* - (.+?)(?:\s+[🔶✅].*)?$'

        lines = content.split('\n')
        current_feature = None
        current_tc_ids = []

        for i, line in enumerate(lines):
            # Check for feature header
            ft_match = re.match(ft_pattern, line)
            if ft_match:
                # Save previous feature if exists
                if current_feature:
                    current_feature.tc_ids = current_tc_ids.copy()
                    features.append(current_feature)

                ft_id, title = ft_match.groups()
                current_feature = Feature(
                    ft_id=ft_id,
                    title=title.strip(),
                    description="",
                    status="completed",  # Default, will be updated from bullets
                    criteria="",
                    is_sub_feature=False
                )
                current_tc_ids = []
                continue

            # If we're in a feature, look for bullets
            if current_feature:
                # Look for criteria
                criteria_match = re.match(criteria_pattern, line)
                if criteria_match:
                    current_feature.criteria = criteria_match.group(1).strip()
                    continue

                # Look for description
                if line.strip().startswith('- **Description:**'):
                    current_feature.description = line.replace('- **Description:**', '').strip()
                    continue

                # Look for Code Location
                code_location_match = re.match(code_location_pattern, line)
                if code_location_match:
                    current_feature.code_location = code_location_match.group(1).strip()
                    continue

                # Look for test cases
                tc_match = re.match(tc_pattern, line)
                if tc_match:
                    status_char, tc_name = tc_match.groups()
                    # Extract TC ID from the line
                    tc_id_match = re.search(r'TC-[A-Z]+-\d+[a-z]?', line)
                    if tc_id_match:
                        current_tc_ids.append(tc_id_match.group(0))

        # Don't forget the last feature
        if current_feature:
            current_feature.tc_ids = current_tc_ids.copy()
            features.append(current_feature)

        return features

    def _parse_legacy_content(self, content: str) -> List[Feature]:
        """Parse legacy FEATURES.md content structure."""
        features = []

        # Pattern to match features using configured FT pattern
        ft_strict_pattern = self.config_manager.get_pattern_for_prefix('FT-', flexible=False)
        # Pattern: - [x] **FT-CORE-001** Feature Name - Description (Criteria: ...)
        ft_pattern = rf'- \[([x~\s])\] \*\*({ft_strict_pattern})\*\* ([^-]+) - ([^(]+)\(Criteria: ([^)]+)\)'

        # Pattern for sub-features
        sub_ft_pattern = rf'\s+- \[([x~\s])\] \*\*({ft_strict_pattern})\*\* ([^-]+) - ([^(]+)\(Criteria: ([^)]+)\)'

        current_parent = None

        for line in content.split('\n'):
            # Check for main features
            main_match = re.match(ft_pattern, line.strip())
            if main_match:
                status_char, ft_id, title, description, criteria = main_match.groups()
                status = 'completed' if status_char == 'x' else 'pending' if status_char == '~' else 'pending'

                feature = Feature(
                    ft_id=ft_id,
                    title=title.strip(),
                    description=description.strip(),
                    status=status,
                    criteria=criteria.strip(),
                    is_sub_feature=False
                )
                features.append(feature)
                current_parent = ft_id
                continue

            # Check for sub-features
            sub_match = re.match(sub_ft_pattern, line)
            if sub_match:
                status_char, ft_id, title, description, criteria = sub_match.groups()
                status = 'completed' if status_char == 'x' else 'pending' if status_char == '~' else 'pending'

                feature = Feature(
                    ft_id=ft_id,
                    title=title.strip(),
                    description=description.strip(),
                    status=status,
                    criteria=criteria.strip(),
                    is_sub_feature=True,
                    parent_ft_id=current_parent
                )
                features.append(feature)

        return features

    def extract_ft_tc_relationships(self, content: str) -> Dict[str, List[str]]:
        """Extract FT-* to TC-* relationships from FEATURES.md content."""
        relationships = {}

        # Find all FT-* identifiers and their associated TC-* references
        ft_pattern = self.config_manager.get_pattern_for_prefix('FT-', flexible=True)
        tc_pattern = self.config_manager.get_pattern_for_prefix('TC-', flexible=True)

        ft_matches = re.finditer(ft_pattern, content)

        for ft_match in ft_matches:
            ft_id = ft_match.group(0)
            # Look for TC-* references in the same section (next 500 characters)
            start_pos = ft_match.end()
            section = content[start_pos:start_pos + 500]
            tc_matches = re.findall(tc_pattern, section)

            if tc_matches:
                relationships[ft_id] = tc_matches

        return relationships

class FTDriftAnalyzer:
    """Analyzes drift between features and test implementations, including FT-TC relationships."""

    def __init__(self, root_dir: str = '.', features_dir: str = 'docs/features',
                 test_cases_file: str = 'docs/TEST-CASES.md',
                 config_manager: Optional[ConfigurationManager] = None,
                 vector_db_manager=None):
        self.root_dir = root_dir
        self.config_manager = config_manager or ConfigurationManager(root_dir)
        self.feature_parser = FeatureParser(features_dir, self.config_manager)
        self.test_case_parser = TestCaseParser(test_cases_file, self.config_manager)
        self.vector_db_manager = vector_db_manager

    def analyze_ft_drift(self, test_functions: List[TestFunction]) -> DriftReport:
        """Analyze FT-* feature drift and FT-TC relationships."""
        print("🔍 Starting FT-* feature drift analysis...\n")

        # Parse features and test cases
        features = self.feature_parser.parse_features()
        test_cases = self.test_case_parser.parse_test_cases(self.vector_db_manager)

        print(f"📋 Found {len(features)} features and {len(test_cases)} test cases")
        print(f"🧪 Analyzing {len(test_functions)} test functions")

        # Analyze FT-* to test function mappings
        ft_mappings = self._map_features_to_tests(features, test_functions)
        features_without_tests = self._find_features_without_tests(features, ft_mappings)
        tests_without_features = self._find_tests_without_features(test_functions, ft_mappings)

        # Analyze FT-* to TC-* relationships
        ft_tc_mappings = self._analyze_ft_tc_relationships(features, test_cases)

        # Find orphaned FT IDs
        orphaned_ft_ids = self._find_orphaned_ft_ids(features, test_functions)

        metadata = {
            'total_features': len(features),
            'total_test_functions': len(test_functions),
            'total_test_cases': len(test_cases),
            'features_with_tests': len(ft_mappings),
            'features_without_tests': len(features_without_tests),
            'tests_without_features': len(tests_without_features),
            'ft_tc_mappings': len(ft_tc_mappings),
            'orphaned_ft_ids': len(orphaned_ft_ids)
        }

        return DriftReport(
            mode='ft-mapping',
            features_without_tests=features_without_tests,
            tests_without_features=tests_without_features,
            ft_mappings=ft_mappings,
            ft_tc_mappings=ft_tc_mappings,
            orphaned_ft_ids=orphaned_ft_ids,
            metadata=metadata
        )

    def _map_features_to_tests(self, features: List[Feature], test_functions: List[TestFunction]) -> Dict[str, List[TestFunction]]:
        """Map FT-* features to test functions that reference them."""
        ft_mappings = {}

        for feature in features:
            ft_id = feature.ft_id
            related_tests = []

            # Find test functions that reference this FT ID
            for test_func in test_functions:
                # Check if FT ID is mentioned in the test function's vicinity
                if self._test_references_feature(test_func, ft_id):
                    related_tests.append(test_func)

            if related_tests:
                ft_mappings[ft_id] = related_tests

        return ft_mappings

    def _test_references_feature(self, test_func: TestFunction, ft_id: str) -> bool:
        """Check if a test function references a specific FT ID."""
        # Check if FT ID is in the test function's file content near the function
        try:
            with open(test_func.file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for FT ID in the vicinity of the test function
            # This is a simplified approach - could be enhanced with more sophisticated parsing
            if ft_id in content:
                return True

        except Exception:
            pass

        return False

    def _find_features_without_tests(self, features: List[Feature], ft_mappings: Dict[str, List[TestFunction]]) -> List[Feature]:
        """Find features that don't have any test implementations."""
        features_without_tests = []

        for feature in features:
            if feature.ft_id not in ft_mappings:
                features_without_tests.append(feature)

        return features_without_tests

    def _find_tests_without_features(self, test_functions: List[TestFunction], ft_mappings: Dict[str, List[TestFunction]]) -> List[TestFunction]:
        """Find test functions that don't reference any FT IDs."""
        tests_with_features = set()

        # Collect all test functions that are mapped to features
        for ft_tests in ft_mappings.values():
            for test_func in ft_tests:
                tests_with_features.add(test_func.full_name)

        # Find tests without feature references
        tests_without_features = []
        for test_func in test_functions:
            if test_func.full_name not in tests_with_features:
                tests_without_features.append(test_func)

        return tests_without_features

    def _analyze_ft_tc_relationships(self, features: List[Feature], test_cases: List[TestCase]) -> List[FeatureTestMapping]:
        """Analyze relationships between FT-* features and TC-* test cases."""
        ft_tc_mappings = []

        for feature in features:
            # Find test cases that reference this feature
            related_tc_ids = []
            missing_tests = []
            mapping_issues = []

            # Look for TC-* references in feature description/criteria
            ft_pattern = self.config_manager.get_pattern_for_prefix('TC-', flexible=True)
            tc_matches = re.findall(ft_pattern, f"{feature.description} {feature.criteria}")

            for tc_id in tc_matches:
                # Check if this TC ID exists in test cases
                tc_exists = any(tc.tc_id == tc_id for tc in test_cases)
                if tc_exists:
                    related_tc_ids.append(tc_id)
                else:
                    missing_tests.append(tc_id)
                    mapping_issues.append(f"Referenced TC-* {tc_id} not found in TEST-CASES.md")

            # Check if feature has any test coverage
            if not related_tc_ids and not missing_tests:
                mapping_issues.append(f"Feature {feature.ft_id} has no TC-* references")

            ft_tc_mapping = FeatureTestMapping(
                ft_id=feature.ft_id,
                feature_title=feature.title,
                tc_ids=related_tc_ids,
                missing_tests=missing_tests,
                orphaned_tests=[],  # Will be populated in reverse analysis
                mapping_issues=mapping_issues
            )

            ft_tc_mappings.append(ft_tc_mapping)

        return ft_tc_mappings

    def _find_orphaned_ft_ids(self, features: List[Feature], test_functions: List[TestFunction]) -> List[str]:
        """Find FT IDs referenced in test functions but not defined in FEATURES.md."""
        defined_ft_ids = {feature.ft_id for feature in features}
        referenced_ft_ids = set()

        # Extract FT IDs from test function files
        ft_pattern = self.config_manager.get_pattern_for_prefix('FT-', flexible=True)

        for test_func in test_functions:
            try:
                with open(test_func.file, 'r', encoding='utf-8') as f:
                    content = f.read()

                ft_matches = re.findall(ft_pattern, content)
                referenced_ft_ids.update(ft_matches)

            except Exception:
                continue

        # Find orphaned FT IDs
        orphaned_ft_ids = list(referenced_ft_ids - defined_ft_ids)
        return orphaned_ft_ids

class TestImplementationScanner:
    """Scans test implementations across multiple programming languages."""

    def __init__(self, root_dir: str = '.', change_detector: Optional['GitChangeDetector'] = None,
                 config_manager: Optional[ConfigurationManager] = None):
        self.root_dir = Path(root_dir)
        self.detector = LanguageDetector()
        self.change_detector = change_detector
        self.config_manager = config_manager or ConfigurationManager(root_dir)

    def find_test_files(self, changed_files: Optional[Set[Path]] = None) -> List[Tuple[Path, str]]:
        """Find all test files and their detected languages, optionally filtered by changed files."""
        test_files = []

        for language, patterns in self.detector.LANGUAGE_PATTERNS.items():
            for pattern in patterns['file_patterns']:
                for file_path in self.root_dir.glob(pattern):
                    if file_path.is_file():
                        detected_lang = self.detector.detect_language(file_path)
                        if detected_lang == language:
                            test_files.append((file_path, language))

        # Filter by changed files if provided
        if changed_files is not None and self.change_detector:
            test_files = self.change_detector.filter_files_by_changes(test_files, changed_files)

        return test_files

    def scan_file_for_tests(self, file_path: Path, language: str) -> List[TestFunction]:
        """Scan a single file for test functions and TC IDs."""
        patterns = self.detector.get_patterns(language)
        if not patterns:
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return []

        test_functions = []

        # Language-specific scanning
        if language == 'python':
            test_functions.extend(self._scan_python_tests(file_path, content))
        elif language == 'javascript':
            test_functions.extend(self._scan_javascript_tests(file_path, content))
        elif language == 'java':
            test_functions.extend(self._scan_java_tests(file_path, content))

        elif language == 'rust':
            test_functions.extend(self._scan_rust_tests(file_path, content))

        return test_functions

    def _find_tc_ids_near_position(self, content: str, position: int, search_range: int = 1000) -> List[str]:
        """Find TC IDs near a specific position in the content."""
        start = max(0, position - search_range // 2)
        end = min(len(content), position + search_range)
        section = content[start:end]

        # Use configured pattern for TC IDs
        tc_pattern = self.config_manager.get_pattern_for_prefix('TC-', flexible=False)
        return re.findall(tc_pattern, section)

    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a position in content."""
        return content[:position].count('\n') + 1

    def _scan_python_tests(self, file_path: Path, content: str) -> List[TestFunction]:
        """Scan Python test files."""
        test_functions = []

        # Find class-based test methods
        class_pattern = r'class\s+(\w*Test\w*)\s*\([^)]*\):(.*?)(?=class|\Z)'
        class_matches = re.finditer(class_pattern, content, re.DOTALL)

        for class_match in class_matches:
            class_name = class_match.group(1)
            class_content = class_match.group(2)
            class_start = class_match.start()

            # Find test methods in this class
            method_pattern = r'def\s+(test_\w+)'
            method_matches = re.finditer(method_pattern, class_content)

            for method_match in method_matches:
                method_name = method_match.group(1)
                method_position = class_start + method_match.start()

                tc_ids = self._find_tc_ids_near_position(content, method_position)
                line_number = self._get_line_number(content, method_position)

                test_functions.append(TestFunction(
                    file=str(file_path),
                    function=method_name,
                    full_name=f"{class_name}::{method_name}",
                    type='class_method',
                    class_name=class_name,
                    tc_ids=tc_ids,
                    line_number=line_number
                ))

        # Find standalone test functions
        standalone_pattern = r'^def\s+(test_\w+)'
        standalone_matches = re.finditer(standalone_pattern, content, re.MULTILINE)

        for func_match in standalone_matches:
            func_name = func_match.group(1)
            func_position = func_match.start()

            tc_ids = self._find_tc_ids_near_position(content, func_position)
            line_number = self._get_line_number(content, func_position)

            test_functions.append(TestFunction(
                file=str(file_path),
                function=func_name,
                full_name=func_name,
                type='standalone',
                tc_ids=tc_ids,
                line_number=line_number
            ))

        return test_functions

    def _scan_javascript_tests(self, file_path: Path, content: str) -> List[TestFunction]:
        """Scan JavaScript/TypeScript test files."""
        test_functions = []

        # Find it() and test() calls
        test_pattern = r'(?:it|test)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
        test_matches = re.finditer(test_pattern, content)

        for test_match in test_matches:
            test_name = test_match.group(1)
            test_position = test_match.start()

            tc_ids = self._find_tc_ids_near_position(content, test_position)
            line_number = self._get_line_number(content, test_position)

            # Clean test name for function name
            func_name = re.sub(r'[^a-zA-Z0-9_]', '_', test_name)

            test_functions.append(TestFunction(
                file=str(file_path),
                function=func_name,
                full_name=test_name,
                type='test_case',
                tc_ids=tc_ids,
                line_number=line_number
            ))

        # Find describe() blocks
        describe_pattern = r'describe\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
        describe_matches = re.finditer(describe_pattern, content)

        for describe_match in describe_matches:
            describe_name = describe_match.group(1)
            describe_position = describe_match.start()

            tc_ids = self._find_tc_ids_near_position(content, describe_position)
            line_number = self._get_line_number(content, describe_position)

            # Clean describe name for function name
            func_name = re.sub(r'[^a-zA-Z0-9_]', '_', describe_name)

            test_functions.append(TestFunction(
                file=str(file_path),
                function=func_name,
                full_name=describe_name,
                type='describe_block',
                tc_ids=tc_ids,
                line_number=line_number
            ))

        return test_functions

    def _scan_java_tests(self, file_path: Path, content: str) -> List[TestFunction]:
        """Scan Java test files."""
        test_functions = []

        # Find @Test annotated methods
        test_pattern = r'@Test[^}]*?(?:public|private|protected)?\s+\w+\s+(\w+)\s*\('
        test_matches = re.finditer(test_pattern, content, re.DOTALL)

        for test_match in test_matches:
            method_name = test_match.group(1)
            test_position = test_match.start()

            tc_ids = self._find_tc_ids_near_position(content, test_position)
            line_number = self._get_line_number(content, test_position)

            # Try to find class name
            class_pattern = r'(?:public\s+)?class\s+(\w+)'
            class_match = re.search(class_pattern, content[:test_position])
            class_name = class_match.group(1) if class_match else None

            full_name = f"{class_name}::{method_name}" if class_name else method_name

            test_functions.append(TestFunction(
                file=str(file_path),
                function=method_name,
                full_name=full_name,
                type='test_method',
                class_name=class_name,
                tc_ids=tc_ids,
                line_number=line_number
            ))

        return test_functions



    def _scan_rust_tests(self, file_path: Path, content: str) -> List[TestFunction]:
        """Scan Rust test files."""
        test_functions = []

        # Find #[test] annotated functions
        test_pattern = r'#\[test\]\s*(?:async\s+)?fn\s+(\w+)'
        test_matches = re.finditer(test_pattern, content)

        for test_match in test_matches:
            func_name = test_match.group(1)
            test_position = test_match.start()

            tc_ids = self._find_tc_ids_near_position(content, test_position)
            line_number = self._get_line_number(content, test_position)

            test_functions.append(TestFunction(
                file=str(file_path),
                function=func_name,
                full_name=func_name,
                type='test_function',
                tc_ids=tc_ids,
                line_number=line_number
            ))

        return test_functions

    def scan_all_tests(self, changed_files: Optional[Set[Path]] = None) -> List[TestFunction]:
        """Scan all test files and return all test functions found, optionally filtered by changed files."""
        all_test_functions = []
        test_files = self.find_test_files(changed_files)

        if changed_files is not None:
            total_test_files = len(self.find_test_files())
            print(f"🔍 Found {len(test_files)} changed test files out of {total_test_files} total test files across {len(set(lang for _, lang in test_files))} languages")
        else:
            print(f"🔍 Found {len(test_files)} test files across {len(set(lang for _, lang in test_files))} languages")

        for file_path, language in test_files:
            print(f"  📁 Scanning {file_path} ({language})")
            test_functions = self.scan_file_for_tests(file_path, language)
            all_test_functions.extend(test_functions)
            print(f"    Found {len(test_functions)} test functions")

        return all_test_functions

class CodeCoverageScanner:
    """Scans for code coverage drift - missing tests for source code."""

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.detector = LanguageDetector()

    def find_source_files(self) -> List[Tuple[Path, str]]:
        """Find all source code files."""
        source_files = []

        # Language-specific source file patterns
        source_patterns = {
            'python': ['*.py', 'src/**/*.py', 'app/**/*.py'],
            'javascript': ['*.js', '*.ts', 'src/**/*.js', 'src/**/*.ts'],
            'java': ['src/main/**/*.java'],
            'rust': ['src/**/*.rs', 'src/main.rs', 'src/lib.rs']
        }

        for language, patterns in source_patterns.items():
            for pattern in patterns:
                for file_path in self.root_dir.glob(pattern):
                    if file_path.is_file() and not self._is_test_file(file_path):
                        detected_lang = self.detector.detect_language(file_path)
                        if detected_lang == language:
                            source_files.append((file_path, language))

        return source_files

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if a file is a test file."""
        name = file_path.name.lower()
        return (name.startswith('test_') or name.endswith('_test.py') or
                name.endswith('.test.js') or name.endswith('.spec.js') or
                name.endswith('Test.java'))

    def scan_coverage_issues(self, test_functions: List[TestFunction]) -> List[CoverageIssue]:
        """Scan for code coverage issues."""
        coverage_issues = []
        source_files = self.find_source_files()

        print(f"🔍 Analyzing coverage for {len(source_files)} source files...")

        # Create mapping of test files to source files
        test_file_coverage = defaultdict(set)
        for func in test_functions:
            test_file_coverage[func.file].add(func.function)

        for file_path, language in source_files:
            source_functions = self._extract_functions_from_source(file_path, language)
            corresponding_test_file = self._find_corresponding_test_file(file_path, language)

            if not corresponding_test_file:
                # No test file exists for this source file
                for func_name, line_num in source_functions:
                    coverage_issues.append(CoverageIssue(
                        file=str(file_path),
                        function=func_name,
                        line_number=line_num,
                        issue_type="missing_test_file",
                        severity="high"
                    ))
            else:
                # Check if functions are tested
                tested_functions = test_file_coverage.get(str(corresponding_test_file), set())
                for func_name, line_num in source_functions:
                    if not self._has_corresponding_test(func_name, tested_functions):
                        coverage_issues.append(CoverageIssue(
                            file=str(file_path),
                            function=func_name,
                            line_number=line_num,
                            issue_type="missing_test",
                            severity="medium"
                        ))

        return coverage_issues

    def _extract_functions_from_source(self, file_path: Path, language: str) -> List[Tuple[str, int]]:
        """Extract function names and line numbers from source file."""
        functions = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return functions

        if language == 'python':
            # Find Python functions and methods
            pattern = r'^(?:    )?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            for match in re.finditer(pattern, content, re.MULTILINE):
                func_name = match.group(1)
                if not func_name.startswith('_'):  # Skip private functions
                    line_num = content[:match.start()].count('\n') + 1
                    functions.append((func_name, line_num))

        elif language == 'javascript':
            # Find JavaScript functions
            patterns = [
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>)',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?:async\s+)?function'
            ]
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    func_name = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1
                    functions.append((func_name, line_num))

        elif language == 'java':
            # Find Java methods
            pattern = r'(?:public|private|protected)?\s+(?:static\s+)?(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{'
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                if func_name not in ['class', 'interface', 'enum']:
                    line_num = content[:match.start()].count('\n') + 1
                    functions.append((func_name, line_num))



        return functions

    def _find_corresponding_test_file(self, source_file: Path, language: str) -> Optional[Path]:
        """Find the corresponding test file for a source file."""
        if language == 'python':
            test_name = f"test_{source_file.stem}.py"
            test_path = source_file.parent / test_name
            if test_path.exists():
                return test_path
            # Also check test/ directory
            test_dir_path = Path('test') / test_name
            if test_dir_path.exists():
                return test_dir_path

        elif language == 'javascript':
            for ext in ['.test.js', '.spec.js', '.test.ts', '.spec.ts']:
                test_name = source_file.stem + ext
                test_path = source_file.parent / test_name
                if test_path.exists():
                    return test_path

        elif language == 'java':
            test_name = f"{source_file.stem}Test.java"
            # Look in src/test/java structure
            test_path = Path('src/test/java') / source_file.relative_to(Path('src/main/java')).parent / test_name
            if test_path.exists():
                return test_path



        return None

    def _has_corresponding_test(self, func_name: str, tested_functions: set) -> bool:
        """Check if a function has a corresponding test."""
        # Look for various test naming patterns
        test_patterns = [
            f"test_{func_name.lower()}",
            f"Test{func_name}",
            f"test{func_name}",
            func_name.lower()
        ]

        for test_func in tested_functions:
            test_func_lower = test_func.lower()
            for pattern in test_patterns:
                if pattern in test_func_lower:
                    return True

        return False

class TestQualityValidator:
    """Validates test quality to ensure tests actually test project code."""

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.detector = LanguageDetector()

    def validate_test_quality(self, test_functions: List[TestFunction]) -> Tuple[List[TestQualityIssue], float]:
        """Validate test quality and return issues and overall score."""
        quality_issues = []
        total_tests = len(test_functions)
        high_quality_tests = 0

        print(f"🔍 Validating quality of {total_tests} test functions...")

        for test_func in test_functions:
            issues, quality_score = self._analyze_test_function_quality(test_func)
            quality_issues.extend(issues)

            # Update test function with quality metrics
            test_func.test_quality_score = quality_score
            test_func.quality_issues = [issue.description for issue in issues]

            if quality_score >= 0.7:  # 70% threshold for high quality
                high_quality_tests += 1

        overall_score = (high_quality_tests / total_tests) if total_tests > 0 else 0.0
        print(f"📊 Test Quality Score: {overall_score:.1%} ({high_quality_tests}/{total_tests} high-quality tests)")

        return quality_issues, overall_score

    def _analyze_test_function_quality(self, test_func: TestFunction) -> Tuple[List[TestQualityIssue], float]:
        """Analyze a single test function for quality issues."""
        issues = []
        quality_score = 1.0  # Start with perfect score, deduct for issues

        try:
            with open(test_func.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            issues.append(TestQualityIssue(
                test_file=test_func.file,
                test_function=test_func.function,
                issue_type='file_read_error',
                severity='high',
                description=f"Cannot read test file {test_func.file}",
                suggestion="Ensure test file is accessible and properly formatted",
                line_number=test_func.line_number
            ))
            return issues, 0.0

        # Check 1: Does the test import project code?
        project_imports = self._find_project_imports(content, test_func)
        if not project_imports:
            issues.append(TestQualityIssue(
                test_file=test_func.file,
                test_function=test_func.function,
                issue_type='no_project_imports',
                severity='critical',
                description="Test does not import any project code - likely testing only mock data",
                suggestion="Import and test actual project modules, classes, or functions",
                line_number=test_func.line_number
            ))
            quality_score -= 0.4
            test_func.imports_project_code = False
        else:
            test_func.imports_project_code = True

        # Check 2: Does the test call actual project functions?
        function_calls = self._find_project_function_calls(content, test_func, project_imports)
        if not function_calls:
            issues.append(TestQualityIssue(
                test_file=test_func.file,
                test_function=test_func.function,
                issue_type='no_function_calls',
                severity='high',
                description="Test does not call any project functions - may only assert against hardcoded values",
                suggestion="Call actual project functions and validate their behavior",
                line_number=test_func.line_number
            ))
            quality_score -= 0.3
            test_func.calls_project_functions = False
        else:
            test_func.calls_project_functions = True

        # Check 3: Does the test use only mock data?
        if self._uses_only_mock_data(content, test_func):
            issues.append(TestQualityIssue(
                test_file=test_func.file,
                test_function=test_func.function,
                issue_type='only_mock_data',
                severity='medium',
                description="Test appears to use only mock/hardcoded data without real integration",
                suggestion="Include integration testing with real data flows where appropriate",
                line_number=test_func.line_number
            ))
            quality_score -= 0.2
            test_func.uses_only_mocks = True

        # Check 4: Does the test have meaningful assertions?
        if not self._has_meaningful_assertions(content, test_func):
            issues.append(TestQualityIssue(
                test_file=test_func.file,
                test_function=test_func.function,
                issue_type='weak_assertions',
                severity='medium',
                description="Test has weak or trivial assertions",
                suggestion="Add assertions that validate actual business logic and edge cases",
                line_number=test_func.line_number
            ))
            quality_score -= 0.1

        return issues, max(0.0, quality_score)

    def _find_project_imports(self, content: str, test_func: TestFunction) -> List[str]:
        """Find imports that reference project code (not test libraries)."""
        project_imports = []

        # Common test library patterns to exclude
        test_libraries = {
            'pytest', 'unittest', 'mock', 'MagicMock', 'Mock', 'patch',
            'json', 're', 'os', 'sys', 'pathlib', 'typing', 'dataclasses'
        }

        # Find import statements
        import_patterns = [
            r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import',
            r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
        ]

        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Skip test libraries and standard library
                if not any(lib in match for lib in test_libraries):
                    # Check if it looks like a project import (not standard library)
                    if '.' in match or not match.islower():
                        project_imports.append(match)

        return project_imports

    def _find_project_function_calls(self, content: str, test_func: TestFunction, project_imports: List[str]) -> List[str]:
        """Find calls to project functions within the test."""
        function_calls = []

        # Look for function calls that use imported modules
        for import_name in project_imports:
            # Pattern for module.function() calls
            call_pattern = rf'{import_name}\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            calls = re.findall(call_pattern, content)
            function_calls.extend([f"{import_name}.{call}" for call in calls])

        # Look for direct function calls (imported with 'from module import function')
        function_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)'
        potential_calls = re.findall(function_pattern, content)

        # Filter out obvious test framework calls
        test_framework_calls = {'assert', 'assertEqual', 'assertTrue', 'assertFalse', 'pytest', 'test'}
        for call in potential_calls:
            if call not in test_framework_calls and not call.startswith('test_'):
                function_calls.append(call)

        return function_calls

    def _uses_only_mock_data(self, content: str, test_func: TestFunction) -> bool:
        """Check if test uses only mock/hardcoded data."""
        # Look for patterns that suggest only mock data usage
        mock_indicators = [
            r'Mock\(',
            r'MagicMock\(',
            r'@patch',
            r'test_data\s*=\s*{',
            r'expected\s*=\s*["\'{]',
            r'assert.*==.*["\'{]'
        ]

        mock_count = 0
        for pattern in mock_indicators:
            if re.search(pattern, content):
                mock_count += 1

        # If many mock indicators and no real data processing, likely only mock data
        return mock_count >= 3

    def _has_meaningful_assertions(self, content: str, test_func: TestFunction) -> bool:
        """Check if test has meaningful assertions beyond trivial checks."""
        # Look for assertion patterns
        assertion_patterns = [
            r'assert\s+',
            r'assertEqual\(',
            r'assertTrue\(',
            r'assertFalse\(',
            r'assertIn\(',
            r'assertRaises\('
        ]

        assertion_count = 0
        for pattern in assertion_patterns:
            assertion_count += len(re.findall(pattern, content))

        # Trivial assertion patterns that suggest weak testing
        trivial_patterns = [
            r'assert\s+True',
            r'assert\s+1\s*==\s*1',
            r'assert\s+".*"\s*==\s*".*"',  # Hardcoded string comparison
        ]

        trivial_count = 0
        for pattern in trivial_patterns:
            trivial_count += len(re.findall(pattern, content))

        # Meaningful if has assertions and not mostly trivial
        return assertion_count > 0 and (trivial_count / assertion_count if assertion_count > 0 else 1) < 0.5

class FeatureImplementationScanner:
    """Scans for feature implementation drift between features and actual implementation."""

    def __init__(self, root_dir: str = '.', features_dir: str = 'docs/features'):
        self.root_dir = Path(root_dir)
        self.features_dir = features_dir
        self.feature_parser = FeatureParser(features_dir)

    def parse_features(self) -> List[Dict]:
        """Parse features from docs/features/ to extract feature definitions."""
        features_list = self.feature_parser.parse_features()

        # Convert Feature objects to dictionaries for compatibility
        features = []
        for feature in features_list:
            features.append({
                'name': feature.ft_id,
                'title': feature.title,
                'description': feature.description,
                'status': feature.status,
                'criteria': feature.criteria
            })

        return features

    def scan_feature_issues(self) -> List[FeatureIssue]:
        """Scan for feature implementation drift issues."""
        feature_issues = []
        features = self.parse_features()

        print(f"🔍 Analyzing {len(features)} features for implementation drift...")

        for feature in features:
            # This is a simplified implementation - in practice, you'd need more sophisticated
            # analysis to determine if a feature is actually implemented
            actual_status = self._analyze_feature_implementation(feature)

            if feature['status'] != actual_status:
                feature_issues.append(FeatureIssue(
                    feature_id=feature['name'],
                    feature_name=feature['name'],
                    documented_status=feature['status'],
                    actual_status=actual_status,
                    issue_type='status_mismatch'
                ))

        return feature_issues

    def _analyze_feature_implementation(self, feature: Dict) -> str:
        """Analyze if a feature is actually implemented (simplified)."""
        # This is a placeholder - real implementation would analyze:
        # - Code files for feature-related functions/classes
        # - Test files for feature tests
        # - Configuration files for feature flags
        # - Documentation for feature usage

        # For now, return the documented status (no drift detected)
        return feature['status']

class ComprehensiveDriftDetector:
    """Comprehensive drift detection with multiple strategies and severity levels."""

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.detector = LanguageDetector()
        self.drift_issues: List[DriftIssue] = []

    def detect_identifier_drift(self) -> List[DriftIssue]:
        """Detect drift using various identifier patterns beyond TC-."""
        patterns = {
            'TC-': 'Test Case identifiers',
            'REQ-': 'Requirement identifiers',
            'US-': 'User Story identifiers',
            'AC-': 'Acceptance Criteria identifiers',
            'BUG-': 'Bug identifiers',
            'FEAT-': 'Feature identifiers',
            'DOC-': 'Documentation identifiers',
            'API-': 'API endpoint identifiers',
            'PERF-': 'Performance requirement identifiers',
            'SEC-': 'Security requirement identifiers'
        }

        issues = []
        for pattern, description in patterns.items():
            issues.extend(self._scan_identifier_pattern(pattern, description))

        return issues

    def detect_import_drift(self) -> List[DriftIssue]:
        """Detect unused imports and missing imports in test files."""
        issues = []

        for test_file in self.root_dir.glob("test_*.py"):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract imports using AST
                import ast
                tree = ast.parse(content)

                imports = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            imports.add(alias.name)

                # Simple usage detection (could be enhanced)
                used_symbols = set()
                for line in content.split('\n'):
                    for imp in imports:
                        if imp in line and not line.strip().startswith('import') and not line.strip().startswith('from'):
                            used_symbols.add(imp)

                # Find unused imports
                unused_imports = imports - used_symbols
                for unused in unused_imports:
                    issues.append(DriftIssue(
                        strategy="import_drift",
                        drift_type="unused_import",
                        severity="info",
                        description=f"Import '{unused}' is not used",
                        location=str(test_file),
                        expected="used",
                        actual="unused",
                        suggestion=f"Remove unused import '{unused}'",
                        file_path=str(test_file)
                    ))

            except Exception as e:
                # Skip files that can't be parsed
                continue

        return issues

    def detect_assertion_pattern_drift(self) -> List[DriftIssue]:
        """Detect outdated assertion patterns that should be modernized."""
        issues = []

        old_patterns = {
            'self.assertEqual': 'assert ==',
            'self.assertTrue': 'assert',
            'self.assertFalse': 'assert not',
            'self.assertIn': 'assert in',
            'self.assertIsNone': 'assert is None',
            'self.assertIsNotNone': 'assert is not None',
            'self.fail': 'pytest.fail'
        }

        for test_file in self.root_dir.glob("test_*.py"):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                for line_num, line in enumerate(content.split('\n'), 1):
                    for old_pattern, new_pattern in old_patterns.items():
                        if old_pattern in line:
                            issues.append(DriftIssue(
                                strategy="assertion_drift",
                                drift_type="outdated_assertion",
                                severity="warning",
                                description=f"Old assertion pattern '{old_pattern}' found",
                                location=str(test_file),
                                expected=new_pattern,
                                actual=old_pattern,
                                suggestion=f"Convert '{old_pattern}' to '{new_pattern}'",
                                file_path=str(test_file),
                                line_number=line_num
                            ))

            except Exception:
                continue

        return issues

    def detect_configuration_drift(self) -> List[DriftIssue]:
        """Detect drift in configuration files vs actual project structure."""
        issues = []

        # Check pyproject.toml vs actual test structure
        pyproject_path = self.root_dir / "pyproject.toml"
        if pyproject_path.exists():
            issues.extend(self._check_pyproject_drift(pyproject_path))

        return issues

    def _scan_identifier_pattern(self, pattern: str, description: str) -> List[DriftIssue]:
        """Scan for specific identifier pattern drift."""
        issues = []

        # Find all identifiers in code
        code_identifiers = self._extract_identifiers_from_code(pattern)

        # Find all identifiers in documentation
        doc_identifiers = self._extract_identifiers_from_docs(pattern)

        # Find missing identifiers
        missing_in_code = doc_identifiers - code_identifiers
        missing_in_docs = code_identifiers - doc_identifiers

        for missing_id in missing_in_code:
            issues.append(DriftIssue(
                strategy="identifier_drift",
                drift_type="missing_implementation",
                severity="critical",
                description=f"{description} {missing_id} documented but not implemented",
                location="code",
                expected=missing_id,
                actual="not found",
                suggestion=f"Implement test case for {missing_id}"
            ))

        for missing_id in missing_in_docs:
            issues.append(DriftIssue(
                strategy="identifier_drift",
                drift_type="missing_documentation",
                severity="warning",
                description=f"{description} {missing_id} implemented but not documented",
                location="documentation",
                expected=missing_id,
                actual="not found",
                suggestion=f"Add documentation for {missing_id}"
            ))

        return issues

    def _extract_identifiers_from_code(self, pattern: str) -> set:
        """Extract identifiers matching pattern from code files."""
        identifiers = set()

        for test_file in self.root_dir.glob("test_*.py"):
            try:
                content = test_file.read_text()
                matches = re.findall(f'{pattern}[A-Z0-9]+-\\d+[a-z]?', content)
                identifiers.update(matches)
            except Exception:
                continue

        return identifiers

    def _extract_identifiers_from_docs(self, pattern: str) -> set:
        """Extract identifiers matching pattern from documentation."""
        identifiers = set()

        # Check markdown files
        for doc_file in self.root_dir.glob("**/*.md"):
            try:
                content = doc_file.read_text()
                matches = re.findall(f'{pattern}[A-Z0-9]+-\\d+[a-z]?', content)
                identifiers.update(matches)
            except Exception:
                continue

        return identifiers

    def _check_pyproject_drift(self, pyproject_path: Path) -> List[DriftIssue]:
        """Check for drift in pyproject.toml configuration."""
        issues = []

        try:
            import tomllib
            with open(pyproject_path, 'rb') as f:
                pyproject_data = tomllib.load(f)

            # Check if test paths in pyproject.toml match actual structure
            test_paths = pyproject_data.get('tool', {}).get('pytest', {}).get('testpaths', [])
            if test_paths:
                for test_path in test_paths:
                    test_dir = self.root_dir / test_path
                    if not test_dir.exists():
                        issues.append(DriftIssue(
                            strategy="configuration_drift",
                            drift_type="missing_test_path",
                            severity="warning",
                            description=f"Test path '{test_path}' in pyproject.toml doesn't exist",
                            location=str(pyproject_path),
                            expected="existing directory",
                            actual="missing directory",
                            suggestion=f"Create directory '{test_path}' or update pyproject.toml"
                        ))

        except Exception:
            # Skip if tomllib not available or file can't be parsed
            pass

        return issues

    def analyze_all_drift(self) -> List[DriftIssue]:
        """Run all comprehensive drift detection strategies."""
        all_issues = []

        all_issues.extend(self.detect_identifier_drift())
        all_issues.extend(self.detect_import_drift())
        all_issues.extend(self.detect_assertion_pattern_drift())
        all_issues.extend(self.detect_configuration_drift())

        return all_issues

class CodeLocationAnalyzer:
    """Analyzes Code Location fields in features for implementation validation."""

    def __init__(self, root_dir: str = '.', features_dir: str = 'docs/features', config_manager: Optional['ConfigurationManager'] = None):
        self.root_dir = Path(root_dir)
        self.features_dir = Path(features_dir)
        self.feature_parser = FeatureParser(features_dir)
        self.config_manager = config_manager or ConfigurationManager(root_dir)

    def analyze_code_locations(self, features: Optional[List[Feature]] = None) -> List[CodeLocationIssue]:
        """Analyze Code Location fields in features and validate implementation paths."""
        if features is None:
            features = self.feature_parser.parse_features()

        issues = []

        for feature in features:
            issues.extend(self._validate_feature_code_location(feature))

        return issues

    def _validate_feature_code_location(self, feature: Feature) -> List[CodeLocationIssue]:
        """Validate a single feature's Code Location field."""
        issues = []

        # Check if Code Location field is missing
        if not feature.code_location:
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=None,
                issue_type='missing_code_location',
                severity='medium',
                description=f"Feature {feature.ft_id} is missing Code Location field",
                suggestion="Add Code Location field pointing to implementation or use 'N/A' for documentation-only features"
            ))
            return issues

        # Skip validation for documentation-only features
        if feature.code_location.strip().upper() == 'N/A':
            return issues

        # Parse multiple locations (separated by commas)
        locations = [loc.strip() for loc in feature.code_location.split(',')]

        for location in locations:
            issues.extend(self._validate_single_location(feature, location))

        return issues

    def _validate_single_location(self, feature: Feature, location: str) -> List[CodeLocationIssue]:
        """Validate a single code location entry."""
        issues = []

        # Parse different location formats
        if '#' in location:
            # New format: relative/path/to/file.py#ClassName.method_name
            file_part, object_part = location.split('#', 1)
            file_part = file_part.strip()
            object_part = object_part.strip()

            issues.extend(self._validate_relative_path_location(feature, file_part, object_part, location))

        elif '[' in location and ']' in location:
            # Legacy format: module.path[Class/Function] or file_path[Object]
            path_part, object_part = location.split('[', 1)
            object_part = object_part.rstrip(']')
            path_part = path_part.strip()

            # Check if it's a Python module path or file path
            if '.' in path_part and not path_part.endswith('.py'):
                # Python module format: tools.drift_scanner[DriftScanner]
                issues.extend(self._validate_python_module_location(feature, path_part, object_part, location))
            else:
                # File path format: vscode-ddd-navigator/src/extension[activate]
                issues.extend(self._validate_file_path_location(feature, path_part, object_part, location))
        else:
            # Simple file path: tools/drift_scanner_mcp_server.sh
            issues.extend(self._validate_simple_file_path(feature, location))

        return issues

    def _validate_relative_path_location(self, feature: Feature, file_path: str, object_name: str, full_location: str) -> List[CodeLocationIssue]:
        """Validate relative file path with object indicator format: path/to/file.py#ClassName.method_name"""
        issues = []

        # Resolve relative path from project root
        full_file_path = self.root_dir / file_path

        # Check if file exists
        if not full_file_path.exists():
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='file_not_found',
                severity='high',
                description=f"File not found: {file_path}",
                suggestion=f"Check if {file_path} exists relative to project root or update Code Location",
                expected_path=str(full_file_path)
            ))
            return issues

        # Read file content for object validation
        try:
            with open(full_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='file_read_error',
                severity='medium',
                description=f"Cannot read file {file_path}: {e}",
                suggestion=f"Check file permissions and encoding for {file_path}",
                expected_path=str(full_file_path)
            ))
            return issues

        # Parse object name (supports Class, Class.method, function formats)
        if '.' in object_name:
            # Format: ClassName.method_name
            class_name, method_name = object_name.split('.', 1)
            issues.extend(self._validate_class_method_in_content(feature, content, class_name, method_name, full_location, file_path))
        else:
            # Format: ClassName or function_name
            issues.extend(self._validate_object_in_content(feature, content, object_name, full_location, file_path))

        return issues

    def _validate_class_method_in_content(self, feature: Feature, content: str, class_name: str, method_name: str, full_location: str, file_path: str) -> List[CodeLocationIssue]:
        """Validate that a class and its method exist in the file content."""
        issues = []

        # Look for class definition
        class_pattern = rf'class\s+{re.escape(class_name)}\s*[\(:]'
        class_match = re.search(class_pattern, content)

        if not class_match:
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='class_not_found',
                severity='medium',
                description=f"Class '{class_name}' not found in {file_path}",
                suggestion=f"Check if class '{class_name}' exists in {file_path} or update Code Location",
                expected_path=file_path
            ))
            return issues

        # Look for method within the class
        # Find the class block and search for the method within it
        class_start = class_match.start()

        # Find the end of the class (next class definition or end of file)
        next_class_pattern = r'\nclass\s+\w+'
        next_class_match = re.search(next_class_pattern, content[class_start + 1:])
        class_end = class_start + next_class_match.start() + 1 if next_class_match else len(content)

        class_content = content[class_start:class_end]

        # Look for method definition within the class
        method_pattern = rf'def\s+{re.escape(method_name)}\s*\('
        method_match = re.search(method_pattern, class_content)

        if not method_match:
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='method_not_found',
                severity='medium',
                description=f"Method '{method_name}' not found in class '{class_name}' in {file_path}",
                suggestion=f"Check if method '{method_name}' exists in class '{class_name}' or update Code Location",
                expected_path=file_path
            ))

        return issues

    def _validate_object_in_content(self, feature: Feature, content: str, object_name: str, full_location: str, file_path: str) -> List[CodeLocationIssue]:
        """Validate that a class or function exists in the file content."""
        issues = []

        # Look for class definition
        class_pattern = rf'class\s+{re.escape(object_name)}\s*[\(:]'
        # Look for function definition
        function_pattern = rf'def\s+{re.escape(object_name)}\s*\('
        # Look for variable/constant definition
        variable_pattern = rf'^{re.escape(object_name)}\s*='

        class_match = re.search(class_pattern, content)
        function_match = re.search(function_pattern, content)
        variable_match = re.search(variable_pattern, content, re.MULTILINE)

        if not (class_match or function_match or variable_match):
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='object_not_found',
                severity='medium',
                description=f"Object '{object_name}' (class, function, or variable) not found in {file_path}",
                suggestion=f"Check if '{object_name}' exists in {file_path} or update Code Location",
                expected_path=file_path
            ))

        return issues

    def _resolve_python_module_paths(self, module_path: str) -> List[Path]:
        """
        Resolve Python module path using multi-fallback approach with configuration.

        Uses .agent3d-config.yml python_paths configuration when available,
        falls back to common project structures.
        """
        possible_paths = []

        # Strategy 1: Check framework-specific module mappings first
        framework_modules = self.config_manager.get_framework_modules()
        if module_path in framework_modules:
            framework_path = self.root_dir / framework_modules[module_path]
            possible_paths.append(framework_path)

        # Strategy 2: Use configured resolution strategies
        resolution_strategies = self.config_manager.get_resolution_strategies()

        for strategy in resolution_strategies:
            if strategy == 'pyproject_toml':
                pyproject_paths = self._get_pyproject_python_paths(module_path)
                possible_paths.extend(pyproject_paths)

            elif strategy == 'direct_path':
                direct_path = self.root_dir / (module_path.replace('.', '/') + '.py')
                possible_paths.append(direct_path)

            elif strategy == 'flat_structure':
                flat_dirs = self.config_manager.get_flat_module_directories()
                for base_dir in flat_dirs:
                    if '.' in module_path:
                        flat_name = module_path.split('.')[-1]  # Get last part of module path
                        flat_path = self.root_dir / base_dir / (flat_name + '.py')
                        possible_paths.append(flat_path)

            elif strategy == 'nested_structure':
                nested_dirs = self.config_manager.get_nested_module_directories()
                for base_dir in nested_dirs:
                    nested_path = self.root_dir / base_dir / (module_path.replace('.', '/') + '.py')
                    possible_paths.append(nested_path)

            elif strategy == 'package_init':
                package_path = self.root_dir / (module_path.replace('.', '/')) / '__init__.py'
                possible_paths.append(package_path)

        # Strategy 3: Fallback to configured source directories
        source_directories = self.config_manager.get_source_directories()
        for base_dir in source_directories:
            # Standard nested structure: base_dir/module/path.py
            nested_path = self.root_dir / base_dir / (module_path.replace('.', '/') + '.py')
            possible_paths.append(nested_path)

            # Flat structure: base_dir/module_name.py
            if '.' in module_path:
                flat_name = module_path.split('.')[-1]
                flat_path = self.root_dir / base_dir / (flat_name + '.py')
                possible_paths.append(flat_path)

        # Remove duplicates while preserving order
        seen = set()
        unique_paths = []
        for path in possible_paths:
            if path not in seen:
                seen.add(path)
                unique_paths.append(path)

        return unique_paths

    def _get_pyproject_python_paths(self, module_path: str) -> List[Path]:
        """Get Python paths from pyproject.toml configuration if it exists."""
        pyproject_file = self.root_dir / 'pyproject.toml'
        if not pyproject_file.exists():
            return []

        try:
            # Try to parse pyproject.toml (requires tomli/tomllib for Python < 3.11)
            try:
                import tomllib  # Python 3.11+
            except ImportError:
                try:
                    import tomli as tomllib  # Fallback for older Python
                except ImportError:
                    # If no TOML parser available, skip pyproject.toml parsing
                    return []

            with open(pyproject_file, 'rb') as f:
                pyproject_data = tomllib.load(f)

            paths = []

            # Check for setuptools configuration
            setuptools_config = pyproject_data.get('tool', {}).get('setuptools', {})
            if 'packages' in setuptools_config:
                # packages = ["src/mypackage"]
                for package in setuptools_config['packages']:
                    if isinstance(package, str):
                        package_path = self.root_dir / package / (module_path.replace('.', '/') + '.py')
                        paths.append(package_path)

            if 'package-dir' in setuptools_config:
                # package-dir = {"" = "src"}
                package_dir = setuptools_config['package-dir']
                for key, value in package_dir.items():
                    base_path = self.root_dir / value / (module_path.replace('.', '/') + '.py')
                    paths.append(base_path)

            # Check for pytest configuration (test paths)
            pytest_config = pyproject_data.get('tool', {}).get('pytest', {}).get('ini_options', {})
            if 'pythonpath' in pytest_config:
                python_paths = pytest_config['pythonpath']
                if isinstance(python_paths, str):
                    python_paths = [python_paths]
                for python_path in python_paths:
                    path = self.root_dir / python_path / (module_path.replace('.', '/') + '.py')
                    paths.append(path)

            return paths

        except Exception as e:
            # If pyproject.toml parsing fails, continue with other strategies
            return []

    def _validate_python_module_location(self, feature: Feature, module_path: str, object_name: str, full_location: str) -> List[CodeLocationIssue]:
        """Validate Python module.path[Object] format."""
        issues = []

        # Try multiple Python path resolution strategies
        possible_paths = self._resolve_python_module_paths(module_path)

        file_path = None
        for path in possible_paths:
            if path.exists():
                file_path = path
                break

        if not file_path:
            # Generate helpful error message with relative paths (first 5 attempts)
            attempted_paths = []
            for p in possible_paths[:5]:  # Show first 5 attempts
                try:
                    rel_path = p.relative_to(self.root_dir)
                    attempted_paths.append(str(rel_path))
                except ValueError:
                    attempted_paths.append(str(p))

            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='file_not_found',
                severity='high',
                description=f"Python module '{module_path}' not found. Tried: {', '.join(attempted_paths)}",
                suggestion=f"Check if module exists in project structure. Common patterns: tools/{module_path.split('.')[-1]}.py, src/{module_path.replace('.', '/')}.py, or {module_path.replace('.', '/')}.py",
                expected_path=attempted_paths[0] if attempted_paths else f"{module_path.replace('.', '/')}.py"
            ))
            return issues

        # Check if the specified class/function exists in the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for class or function definition
            class_pattern = rf'class\s+{re.escape(object_name)}\s*[\(:]'
            function_pattern = rf'def\s+{re.escape(object_name)}\s*\('
            method_pattern = rf'def\s+{re.escape(object_name.split(".")[-1])}\s*\('  # For Class.method format

            if not (re.search(class_pattern, content) or
                   re.search(function_pattern, content) or
                   re.search(method_pattern, content)):
                issues.append(CodeLocationIssue(
                    feature_id=feature.ft_id,
                    feature_name=feature.title,
                    code_location=full_location,
                    issue_type='class_not_found',
                    severity='medium',
                    description=f"Class/function '{object_name}' not found in {file_path}",
                    suggestion=f"Check if '{object_name}' exists in {file_path} or update Code Location",
                    expected_path=str(file_path)
                ))

        except Exception as e:
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='invalid_path',
                severity='medium',
                description=f"Error reading file {file_path}: {e}",
                suggestion=f"Check file permissions and encoding for {file_path}",
                expected_path=str(file_path)
            ))

        return issues

    def _validate_file_path_location(self, feature: Feature, file_path: str, object_name: str, full_location: str) -> List[CodeLocationIssue]:
        """Validate file_path[Object] format."""
        issues = []

        full_file_path = self.root_dir / file_path

        if not full_file_path.exists():
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=full_location,
                issue_type='file_not_found',
                severity='high',
                description=f"File not found: {full_file_path}",
                suggestion=f"Check if {full_file_path} exists or update Code Location",
                expected_path=str(full_file_path)
            ))
            return issues

        # For TypeScript/JavaScript files, look for function/class/export
        if full_file_path.suffix in ['.ts', '.js', '.tsx', '.jsx']:
            try:
                with open(full_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for various TypeScript/JavaScript patterns
                patterns = [
                    rf'function\s+{re.escape(object_name)}\s*\(',
                    rf'const\s+{re.escape(object_name)}\s*=',
                    rf'export\s+function\s+{re.escape(object_name)}\s*\(',
                    rf'export\s+const\s+{re.escape(object_name)}\s*=',
                    rf'class\s+{re.escape(object_name)}\s*{{',
                    rf'export\s+class\s+{re.escape(object_name)}\s*{{'
                ]

                if not any(re.search(pattern, content) for pattern in patterns):
                    issues.append(CodeLocationIssue(
                        feature_id=feature.ft_id,
                        feature_name=feature.title,
                        code_location=full_location,
                        issue_type='class_not_found',
                        severity='medium',
                        description=f"Function/class '{object_name}' not found in {full_file_path}",
                        suggestion=f"Check if '{object_name}' exists in {full_file_path} or update Code Location",
                        expected_path=str(full_file_path)
                    ))

            except Exception as e:
                issues.append(CodeLocationIssue(
                    feature_id=feature.ft_id,
                    feature_name=feature.title,
                    code_location=full_location,
                    issue_type='invalid_path',
                    severity='medium',
                    description=f"Error reading file {full_file_path}: {e}",
                    suggestion=f"Check file permissions and encoding for {full_file_path}",
                    expected_path=str(full_file_path)
                ))

        return issues

    def _validate_simple_file_path(self, feature: Feature, file_path: str) -> List[CodeLocationIssue]:
        """Validate simple file path format."""
        issues = []

        full_file_path = self.root_dir / file_path

        if not full_file_path.exists():
            issues.append(CodeLocationIssue(
                feature_id=feature.ft_id,
                feature_name=feature.title,
                code_location=file_path,
                issue_type='file_not_found',
                severity='high',
                description=f"File not found: {full_file_path}",
                suggestion=f"Check if {full_file_path} exists or update Code Location",
                expected_path=str(full_file_path)
            ))

        return issues

class MultiModeDriftAnalyzer:
    """Multi-mode drift analyzer that can run different types of drift detection."""

    def __init__(self, root_dir: str = '.', test_cases_file: str = 'docs/TEST-CASES.md',
                 change_detector: Optional[GitChangeDetector] = None, enable_vector_db: bool = True):
        self.root_dir = root_dir
        self.test_cases_file = test_cases_file
        self.change_detector = change_detector
        self.config_manager = ConfigurationManager(root_dir)
        self.enable_vector_db = enable_vector_db and VECTOR_DB_AVAILABLE

        # Initialize vector database manager if available
        self.vector_db_manager = None
        if self.enable_vector_db:
            try:
                self.vector_db_manager = MultiRootVectorDBManager()
                print("✅ Vector database manager initialized for enhanced file discovery")
            except Exception as e:
                print(f"⚠️  Failed to initialize vector database manager: {e}")
                self.enable_vector_db = False
        elif not VECTOR_DB_AVAILABLE:
            print("⚠️  Vector database dependencies not available, using traditional file scanning")

        # Initialize individual scanners with configuration
        self.tc_analyzer = TCDriftAnalyzer(root_dir, test_cases_file, change_detector, self.config_manager, self.vector_db_manager)
        self.ft_analyzer = FTDriftAnalyzer(root_dir, 'docs/features', test_cases_file, self.config_manager, self.vector_db_manager)
        self.coverage_scanner = CodeCoverageScanner(root_dir)
        self.feature_scanner = FeatureImplementationScanner(root_dir, 'docs/features')
        self.comprehensive_detector = ComprehensiveDriftDetector(root_dir)
        self.test_quality_validator = TestQualityValidator(root_dir)
        self.code_location_analyzer = CodeLocationAnalyzer(root_dir, 'docs/features', self.config_manager)

    def get_vector_db_stats(self) -> Dict[str, Any]:
        """Get vector database statistics."""
        if not self.vector_db_manager:
            return {"status": "unavailable", "reason": "Vector database not initialized"}

        return self.vector_db_manager.get_statistics(self.root_dir)

    def search_related_files(self, query: str, top_k: int = 10,
                           filter_language: str = None, filter_chunk_type: str = None) -> List[Tuple[Any, float]]:
        """Search for files related to a query using vector database.

        Args:
            query: Search query (e.g., "test cases for authentication")
            top_k: Number of results to return
            filter_language: Filter by programming language (e.g., "python")
            filter_chunk_type: Filter by chunk type (e.g., "test", "function", "class")

        Returns:
            List of (chunk, similarity_score) tuples
        """
        if not self.vector_db_manager:
            print("⚠️  Vector database not available for search")
            return []

        return self.vector_db_manager.search(self.root_dir, query, top_k, filter_language, filter_chunk_type)

    def find_related_test_files(self, feature_description: str, top_k: int = 5) -> List[str]:
        """Find test files related to a feature description.

        Args:
            feature_description: Description of the feature to find tests for
            top_k: Number of test files to return

        Returns:
            List of test file paths
        """
        if not self.vector_db_manager:
            return []

        # Search for test-related chunks
        test_query = f"test {feature_description}"
        results = self.vector_db_manager.search(
            self.root_dir, test_query, top_k * 2,
            filter_chunk_type="test"
        )

        # Extract unique file paths
        test_files = []
        seen_files = set()
        for chunk, score in results:
            if hasattr(chunk, 'file_path') and chunk.file_path not in seen_files:
                seen_files.add(chunk.file_path)
                test_files.append(chunk.file_path)
                if len(test_files) >= top_k:
                    break

        return test_files

    def find_implementation_files(self, feature_description: str, top_k: int = 5) -> List[str]:
        """Find implementation files related to a feature description.

        Args:
            feature_description: Description of the feature to find implementation for
            top_k: Number of implementation files to return

        Returns:
            List of implementation file paths
        """
        if not self.vector_db_manager:
            return []

        # Search for implementation-related chunks (exclude tests)
        results = self.vector_db_manager.search(
            self.root_dir, feature_description, top_k * 3
        )

        # Filter out test files and extract unique file paths
        impl_files = []
        seen_files = set()
        for chunk, score in results:
            if hasattr(chunk, 'file_path') and chunk.file_path not in seen_files:
                # Skip test files
                if 'test' not in chunk.file_path.lower() and chunk.chunk_type != 'test':
                    seen_files.add(chunk.file_path)
                    impl_files.append(chunk.file_path)
                    if len(impl_files) >= top_k:
                        break

        return impl_files

    def vector_enhanced_feature_mapping(self, features: List[Feature], test_functions: List[TestFunction]) -> Dict[str, List[TestFunction]]:
        """Enhanced feature-to-test mapping using vector database semantic search.

        Args:
            features: List of features to map
            test_functions: List of test functions to search through

        Returns:
            Dictionary mapping feature IDs to related test functions
        """
        if not self.vector_db_manager:
            print("⚠️  Vector database not available, falling back to traditional mapping")
            return self.ft_analyzer._map_features_to_tests(features, test_functions)

        print("🔍 Using vector-enhanced feature mapping...")
        ft_mappings = {}

        for feature in features:
            # Create search query from feature content
            search_query = f"{feature.title} {feature.description} {feature.criteria}"

            # Search for related test chunks
            test_results = self.vector_db_manager.search(
                self.root_dir, search_query, top_k=20,
                filter_chunk_type="test"
            )

            # Also search for general code that might be related
            code_results = self.vector_db_manager.search(
                self.root_dir, search_query, top_k=10,
                filter_language="python"
            )

            # Combine and filter results
            related_tests = []
            seen_files = set()

            # Process test results first (higher priority)
            for chunk, score in test_results:
                if hasattr(chunk, 'file_path') and score > 0.3:  # Similarity threshold
                    # Find test functions in this file
                    for test_func in test_functions:
                        if (test_func.file == chunk.file_path and
                            test_func.file not in seen_files):
                            related_tests.append(test_func)
                            seen_files.add(test_func.file)

            # Process code results for additional context
            for chunk, score in code_results:
                if hasattr(chunk, 'file_path') and score > 0.4:  # Higher threshold for code
                    # Check if this is a test file we haven't seen
                    if 'test' in chunk.file_path.lower():
                        for test_func in test_functions:
                            if (test_func.file == chunk.file_path and
                                test_func.file not in seen_files):
                                related_tests.append(test_func)
                                seen_files.add(test_func.file)

            if related_tests:
                ft_mappings[feature.ft_id] = related_tests
                print(f"  📋 {feature.ft_id}: Found {len(related_tests)} related tests via vector search")
            else:
                print(f"  ❌ {feature.ft_id}: No related tests found via vector search")

        return ft_mappings

    def vector_enhanced_test_coverage_analysis(self, test_functions: List[TestFunction]) -> List[CoverageIssue]:
        """Enhanced test coverage analysis using vector database to find missing tests.

        Args:
            test_functions: List of existing test functions

        Returns:
            List of coverage issues found via vector analysis
        """
        if not self.vector_db_manager:
            print("⚠️  Vector database not available, falling back to traditional coverage analysis")
            return self.coverage_scanner.scan_coverage_issues(test_functions)

        print("🔍 Using vector-enhanced coverage analysis...")
        coverage_issues = []

        # Get all source files
        source_files = self.coverage_scanner.find_source_files()

        # Create a set of tested file patterns from existing tests
        tested_patterns = set()
        for test_func in test_functions:
            # Extract likely source file patterns from test names
            test_name = test_func.function.lower()
            if test_name.startswith('test_'):
                pattern = test_name[5:]  # Remove 'test_' prefix
                tested_patterns.add(pattern)

        for file_path, language in source_files:
            if language != 'python':  # Focus on Python for now
                continue

            # Extract functions from source file
            functions = self.coverage_scanner._extract_functions_from_source(file_path, language)

            for func_name, line_num in functions:
                # Use vector search to find related tests
                search_query = f"test {func_name} {file_path.stem}"

                test_results = self.vector_db_manager.search(
                    self.root_dir, search_query, top_k=5,
                    filter_chunk_type="test"
                )

                # Check if we found any relevant tests
                has_related_test = False
                for chunk, score in test_results:
                    if score > 0.4:  # Similarity threshold
                        # Check if any test function is in this chunk's file
                        for test_func in test_functions:
                            if test_func.file == chunk.file_path:
                                has_related_test = True
                                break
                    if has_related_test:
                        break

                if not has_related_test:
                    coverage_issues.append(CoverageIssue(
                        file=str(file_path),
                        function=func_name,
                        line_number=line_num,
                        issue_type="missing_test_vector",
                        severity="medium"
                    ))
                    print(f"  ❌ Missing test for {file_path}::{func_name} (vector analysis)")

        print(f"🔍 Vector coverage analysis found {len(coverage_issues)} potential issues")
        return coverage_issues

    def vector_enhanced_test_quality_analysis(self, test_functions: List[TestFunction]) -> Tuple[List[TestQualityIssue], float]:
        """Enhanced test quality analysis using vector database to assess test relevance.

        Args:
            test_functions: List of test functions to analyze

        Returns:
            Tuple of (quality issues, overall quality score)
        """
        if not self.vector_db_manager:
            print("⚠️  Vector database not available, falling back to traditional quality analysis")
            return self.test_quality_validator.validate_test_quality(test_functions)

        print("🔍 Using vector-enhanced test quality analysis...")
        quality_issues = []
        quality_scores = []

        for test_func in test_functions:
            # Use vector search to find related implementation code
            search_query = f"{test_func.function} {test_func.class_name or ''}"

            # Search for related implementation chunks
            impl_results = self.vector_db_manager.search(
                self.root_dir, search_query, top_k=10,
                filter_language="python"
            )

            # Filter out test files to focus on implementation
            impl_chunks = []
            for chunk, score in impl_results:
                if (hasattr(chunk, 'file_path') and
                    'test' not in chunk.file_path.lower() and
                    chunk.chunk_type != 'test' and
                    score > 0.3):
                    impl_chunks.append((chunk, score))

            # Calculate quality score based on vector similarity to implementation
            if impl_chunks:
                # High similarity to implementation code suggests good test quality
                max_similarity = max(score for _, score in impl_chunks)
                avg_similarity = sum(score for _, score in impl_chunks) / len(impl_chunks)

                # Quality score based on similarity to implementation
                quality_score = (max_similarity * 0.6 + avg_similarity * 0.4)
                quality_scores.append(quality_score)

                # Check for quality issues
                if quality_score < 0.4:
                    quality_issues.append(TestQualityIssue(
                        test_file=test_func.file,
                        test_function=test_func.function,
                        issue_type="low_implementation_similarity",
                        severity="medium",
                        description=f"Test has low similarity to implementation code (score: {quality_score:.2f})",
                        suggestion="Review test to ensure it properly tests project functionality"
                    ))
                    print(f"  ⚠️  {test_func.function}: Low implementation similarity ({quality_score:.2f})")
                else:
                    print(f"  ✅ {test_func.function}: Good implementation similarity ({quality_score:.2f})")
            else:
                # No related implementation found
                quality_scores.append(0.0)
                quality_issues.append(TestQualityIssue(
                    test_file=test_func.file,
                    test_function=test_func.function,
                    issue_type="no_related_implementation",
                    severity="high",
                    description="No related implementation code found via vector search",
                    suggestion="Ensure test is testing actual project code, not just mock data"
                ))
                print(f"  ❌ {test_func.function}: No related implementation found")

        overall_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        print(f"🔍 Vector quality analysis: {len(quality_issues)} issues, overall score: {overall_score:.2f}")

        return quality_issues, overall_score

    def vector_enhanced_code_location_analysis(self, features: List[Feature]) -> List[CodeLocationIssue]:
        """Enhanced code location analysis using vector database to validate feature locations.

        Args:
            features: List of features with code location fields

        Returns:
            List of code location issues found via vector analysis
        """
        if not self.vector_db_manager:
            print("⚠️  Vector database not available, falling back to traditional code location analysis")
            return self.code_location_analyzer.analyze_code_locations(features)

        print("🔍 Using vector-enhanced code location analysis...")
        location_issues = []

        for feature in features:
            if not feature.code_location or feature.code_location.strip().upper() == 'N/A':
                # Try to find implementation using vector search
                search_query = f"{feature.title} {feature.description}"

                impl_results = self.vector_db_manager.search(
                    self.root_dir, search_query, top_k=5,
                    filter_language="python"
                )

                # Filter out test files and documentation
                impl_candidates = []
                for chunk, score in impl_results:
                    if (hasattr(chunk, 'file_path') and
                        'test' not in chunk.file_path.lower() and
                        chunk.chunk_type in ['function', 'class'] and
                        score > 0.4):
                        impl_candidates.append((chunk.file_path, score))

                if impl_candidates:
                    # Found potential implementation
                    best_match = max(impl_candidates, key=lambda x: x[1])
                    location_issues.append(CodeLocationIssue(
                        feature_id=feature.ft_id,
                        feature_name=feature.title,
                        code_location=feature.code_location,
                        issue_type='missing_code_location_with_suggestion',
                        severity='medium',
                        description=f"Code Location missing but implementation found via vector search",
                        suggestion=f"Consider setting Code Location to: {best_match[0]}",
                        expected_path=best_match[0]
                    ))
                    print(f"  💡 {feature.ft_id}: Found potential implementation at {best_match[0]} (similarity: {best_match[1]:.2f})")
                else:
                    location_issues.append(CodeLocationIssue(
                        feature_id=feature.ft_id,
                        feature_name=feature.title,
                        code_location=feature.code_location,
                        issue_type='missing_code_location',
                        severity='low',
                        description="Code Location missing and no implementation found via vector search",
                        suggestion="Feature may be documentation-only or implementation not yet created"
                    ))
                    print(f"  ❌ {feature.ft_id}: No implementation found via vector search")

            else:
                # Validate existing code location using vector search
                search_query = f"{feature.title} {feature.description}"

                impl_results = self.vector_db_manager.search(
                    self.root_dir, search_query, top_k=10,
                    filter_language="python"
                )

                # Check if the specified location appears in results
                location_found = False
                for chunk, score in impl_results:
                    if (hasattr(chunk, 'file_path') and
                        feature.code_location in chunk.file_path and
                        score > 0.3):
                        location_found = True
                        print(f"  ✅ {feature.ft_id}: Code location validated via vector search (similarity: {score:.2f})")
                        break

                if not location_found:
                    # Check if there are better alternatives
                    better_alternatives = []
                    for chunk, score in impl_results:
                        if (hasattr(chunk, 'file_path') and
                            'test' not in chunk.file_path.lower() and
                            chunk.chunk_type in ['function', 'class'] and
                            score > 0.4):
                            better_alternatives.append((chunk.file_path, score))

                    if better_alternatives:
                        best_alt = max(better_alternatives, key=lambda x: x[1])
                        location_issues.append(CodeLocationIssue(
                            feature_id=feature.ft_id,
                            feature_name=feature.title,
                            code_location=feature.code_location,
                            issue_type='potentially_incorrect_location',
                            severity='medium',
                            description=f"Current location not found in vector search, better match available",
                            suggestion=f"Consider updating Code Location to: {best_alt[0]}",
                            expected_path=best_alt[0]
                        ))
                        print(f"  ⚠️  {feature.ft_id}: Better location found at {best_alt[0]} (similarity: {best_alt[1]:.2f})")
                    else:
                        location_issues.append(CodeLocationIssue(
                            feature_id=feature.ft_id,
                            feature_name=feature.title,
                            code_location=feature.code_location,
                            issue_type='location_not_found_vector',
                            severity='high',
                            description="Specified location not validated by vector search",
                            suggestion="Verify the Code Location field points to correct implementation"
                        ))
                        print(f"  ❌ {feature.ft_id}: Location not validated by vector search")

        print(f"🔍 Vector location analysis found {len(location_issues)} potential issues")
        return location_issues

    def analyze_drift(self, mode: str = 'tc-mapping', changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze drift based on the specified mode, optionally filtered by changed files."""
        if mode == 'tc-mapping':
            return self._analyze_tc_mapping(changed_files)
        elif mode == 'ft-mapping':
            return self._analyze_ft_mapping(changed_files)
        elif mode == 'ft-tc-mapping':
            return self._analyze_ft_tc_mapping(changed_files)
        elif mode == 'code-coverage':
            return self._analyze_code_coverage(changed_files)
        elif mode == 'feature-impl':
            return self._analyze_feature_implementation(changed_files)
        elif mode == 'code-location':
            return self._analyze_code_location(changed_files)
        elif mode == 'test-quality':
            return self._analyze_test_quality(changed_files)
        elif mode == 'all':
            return self._analyze_all_modes(changed_files)
        else:
            raise ValueError(f"Unknown drift analysis mode: {mode}")

    def _analyze_tc_mapping(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze TC ID mapping drift."""
        if changed_files is not None:
            print("🔍 Starting TC ID mapping drift analysis (change-based)...\n")
        else:
            print("🔍 Starting TC ID mapping drift analysis...\n")
        tc_report = self.tc_analyzer.analyze_drift(changed_files)
        tc_report.mode = 'tc-mapping'
        return tc_report

    def _analyze_ft_mapping(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze FT ID mapping drift with optional vector enhancement."""
        if changed_files is not None:
            print("🔍 Starting FT ID mapping drift analysis (change-based)...\n")
        else:
            print("🔍 Starting FT ID mapping drift analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Use vector-enhanced analysis if available
        if self.vector_db_manager:
            print("🚀 Using vector-enhanced feature mapping...")
            features = self.ft_analyzer.feature_parser.parse_features()

            # Use vector-enhanced mapping
            ft_mappings = self.vector_enhanced_feature_mapping(features, test_functions)

            # Find features without tests and tests without features
            features_without_tests = []
            tests_without_features = []

            for feature in features:
                if feature.ft_id not in ft_mappings:
                    features_without_tests.append(feature)

            # Find test functions not mapped to any feature
            mapped_test_files = set()
            for test_list in ft_mappings.values():
                for test_func in test_list:
                    mapped_test_files.add(test_func.file)

            for test_func in test_functions:
                if test_func.file not in mapped_test_files:
                    tests_without_features.append(test_func)

            # Generate metadata
            metadata = {
                'total_features': len(features),
                'total_test_functions': len(test_functions),
                'features_with_tests': len(ft_mappings),
                'vector_enhanced': True,
                'mapping_method': 'vector_semantic_search'
            }

            return DriftReport(
                mode='ft-mapping',
                features_without_tests=features_without_tests,
                tests_without_features=tests_without_features,
                ft_mappings=ft_mappings,
                metadata=metadata
            )
        else:
            # Fallback to traditional analysis
            ft_report = self.ft_analyzer.analyze_ft_drift(test_functions)
            ft_report.mode = 'ft-mapping'
            return ft_report

    def _analyze_ft_tc_mapping(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze FT-TC relationship mapping drift."""
        if changed_files is not None:
            print("🔍 Starting FT-TC relationship mapping drift analysis (change-based)...\n")
        else:
            print("🔍 Starting FT-TC relationship mapping drift analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Analyze both TC and FT drift
        tc_report = self.tc_analyzer.analyze_drift(changed_files)
        ft_report = self.ft_analyzer.analyze_ft_drift(test_functions)

        # Combine the reports
        combined_metadata = {
            **tc_report.metadata,
            **ft_report.metadata,
            'mode': 'ft-tc-mapping'
        }

        return DriftReport(
            mode='ft-tc-mapping',
            # TC Mapping data
            test_cases_without_implementations=tc_report.test_cases_without_implementations,
            implementations_without_test_cases=tc_report.implementations_without_test_cases,
            tc_mappings=tc_report.tc_mappings,
            orphaned_tc_ids=tc_report.orphaned_tc_ids,
            # FT Mapping data
            features_without_tests=ft_report.features_without_tests,
            tests_without_features=ft_report.tests_without_features,
            ft_mappings=ft_report.ft_mappings,
            ft_tc_mappings=ft_report.ft_tc_mappings,
            orphaned_ft_ids=ft_report.orphaned_ft_ids,
            metadata=combined_metadata
        )

    def _analyze_code_coverage(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze code coverage drift with optional vector enhancement."""
        if changed_files is not None:
            print("🔍 Starting code coverage drift analysis (change-based)...\n")
        else:
            print("🔍 Starting code coverage drift analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Use vector-enhanced analysis if available
        if self.vector_db_manager:
            print("🚀 Using vector-enhanced coverage analysis...")
            vector_coverage_issues = self.vector_enhanced_test_coverage_analysis(test_functions)
            traditional_coverage_issues = self.coverage_scanner.scan_coverage_issues(test_functions)

            # Combine both analyses
            all_coverage_issues = traditional_coverage_issues + vector_coverage_issues

            # Calculate coverage percentage
            source_files = self.coverage_scanner.find_source_files()
            total_functions = sum(len(self.coverage_scanner._extract_functions_from_source(f, lang))
                                for f, lang in source_files)

            coverage_percentage = 0.0
            if total_functions > 0:
                tested_functions = total_functions - len([issue for issue in all_coverage_issues
                                                       if issue.issue_type in ['missing_test', 'missing_test_file', 'missing_test_vector']])
                coverage_percentage = (tested_functions / total_functions) * 100

            metadata = {
                'total_source_files': len(source_files),
                'total_functions': total_functions,
                'coverage_issues_count': len(all_coverage_issues),
                'traditional_issues': len(traditional_coverage_issues),
                'vector_issues': len(vector_coverage_issues),
                'coverage_percentage': round(coverage_percentage, 2) if coverage_percentage is not None else 0.0,
                'vector_enhanced': True,
                'analysis_method': 'hybrid_traditional_vector'
            }

            return DriftReport(
                mode='code-coverage',
                coverage_issues=all_coverage_issues,
                coverage_percentage=coverage_percentage,
                metadata=metadata
            )
        else:
            # Fallback to traditional analysis
            coverage_issues = self.coverage_scanner.scan_coverage_issues(test_functions)

            # Calculate coverage percentage
            source_files = self.coverage_scanner.find_source_files()
            total_functions = sum(len(self.coverage_scanner._extract_functions_from_source(f, lang))
                                for f, lang in source_files)

            coverage_percentage = 0.0
            if total_functions > 0:
                tested_functions = total_functions - len([issue for issue in coverage_issues
                                                       if issue.issue_type in ['missing_test', 'missing_test_file']])
                coverage_percentage = (tested_functions / total_functions) * 100

            metadata = {
                'total_source_files': len(source_files),
                'total_functions': total_functions,
                'coverage_issues_count': len(coverage_issues),
                'coverage_percentage': round(coverage_percentage, 2) if coverage_percentage is not None else 0.0,
                'vector_enhanced': False,
                'analysis_method': 'traditional_only'
            }

            return DriftReport(
                mode='code-coverage',
                coverage_issues=coverage_issues,
                coverage_percentage=coverage_percentage,
                metadata=metadata
            )

    def _analyze_feature_implementation(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze feature implementation drift."""
        if changed_files is not None:
            print("🔍 Starting feature implementation drift analysis (change-based)...\n")
        else:
            print("🔍 Starting feature implementation drift analysis...\n")

        feature_issues = self.feature_scanner.scan_feature_issues()

        metadata = {
            'total_features': len(self.feature_scanner.parse_features()),
            'feature_issues_count': len(feature_issues)
        }

        return DriftReport(
            mode='feature-impl',
            feature_issues=feature_issues,
            metadata=metadata
        )

    def _analyze_code_location(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze Code Location field validation with optional vector enhancement."""
        if changed_files is not None:
            print("🔍 Starting Code Location analysis (change-based)...\n")
        else:
            print("🔍 Starting Code Location analysis...\n")

        # Parse features and analyze their Code Location fields
        features = self.ft_analyzer.feature_parser.parse_features()

        # Use vector-enhanced analysis if available
        if self.vector_db_manager:
            print("🚀 Using vector-enhanced code location analysis...")
            vector_location_issues = self.vector_enhanced_code_location_analysis(features)
            traditional_location_issues = self.code_location_analyzer.analyze_code_locations(features)

            # Combine both analyses, prioritizing vector results
            all_location_issues = vector_location_issues + traditional_location_issues

            # Calculate statistics
            total_features = len(features)
            features_with_code_location = len([f for f in features if f.code_location])
            features_with_valid_location = len([f for f in features
                                              if f.code_location and f.code_location.strip().upper() != 'N/A'])
            documentation_only_features = len([f for f in features
                                             if f.code_location and f.code_location.strip().upper() == 'N/A'])

            metadata = {
                'total_features': total_features,
                'features_with_code_location': features_with_code_location,
                'features_with_valid_location': features_with_valid_location,
                'documentation_only_features': documentation_only_features,
                'code_location_issues_count': len(all_location_issues),
                'vector_issues': len(vector_location_issues),
                'traditional_issues': len(traditional_location_issues),
                'vector_enhanced': True,
                'analysis_method': 'hybrid_vector_traditional',
                'missing_code_location': len([issue for issue in all_location_issues
                                            if issue.issue_type == 'missing_code_location']),
                'file_not_found': len([issue for issue in all_location_issues
                                     if issue.issue_type == 'file_not_found']),
                'class_not_found': len([issue for issue in all_location_issues
                                      if issue.issue_type == 'class_not_found']),
                'coverage_percentage': round((features_with_code_location / total_features) * 100, 2) if total_features > 0 else 0
            }

            return DriftReport(
                mode='code-location',
                code_location_issues=all_location_issues,
                metadata=metadata
            )
        else:
            # Fallback to traditional analysis
            code_location_issues = self.code_location_analyzer.analyze_code_locations(features)

            # Calculate statistics
            total_features = len(features)
            features_with_code_location = len([f for f in features if f.code_location])
            features_with_valid_location = len([f for f in features
                                              if f.code_location and f.code_location.strip().upper() != 'N/A'])
            documentation_only_features = len([f for f in features
                                             if f.code_location and f.code_location.strip().upper() == 'N/A'])

            metadata = {
                'total_features': total_features,
                'features_with_code_location': features_with_code_location,
                'features_with_valid_location': features_with_valid_location,
                'documentation_only_features': documentation_only_features,
                'code_location_issues_count': len(code_location_issues),
                'vector_enhanced': False,
                'analysis_method': 'traditional_only',
                'missing_code_location': len([issue for issue in code_location_issues
                                            if issue.issue_type == 'missing_code_location']),
                'file_not_found': len([issue for issue in code_location_issues
                                     if issue.issue_type == 'file_not_found']),
                'class_not_found': len([issue for issue in code_location_issues
                                      if issue.issue_type == 'class_not_found']),
                'coverage_percentage': round((features_with_code_location / total_features) * 100, 2) if total_features > 0 else 0
            }

            return DriftReport(
                mode='code-location',
                code_location_issues=code_location_issues,
                metadata=metadata
            )

    def _analyze_test_quality(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze test quality to ensure tests actually test project code with optional vector enhancement."""
        if changed_files is not None:
            print("🔍 Starting test quality analysis (change-based)...\n")
        else:
            print("🔍 Starting test quality analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Use vector-enhanced analysis if available
        if self.vector_db_manager:
            print("🚀 Using vector-enhanced test quality analysis...")
            vector_quality_issues, vector_overall_score = self.vector_enhanced_test_quality_analysis(test_functions)
            traditional_quality_issues, traditional_overall_score = self.test_quality_validator.validate_test_quality(test_functions)

            # Combine both analyses
            all_quality_issues = traditional_quality_issues + vector_quality_issues

            # Calculate combined overall score (weighted average)
            combined_score = (traditional_overall_score * 0.6 + vector_overall_score * 0.4)

            # Identify low-quality tests based on combined analysis
            low_quality_tests = [func for func in test_functions
                               if (hasattr(func, 'test_quality_score') and func.test_quality_score < 0.7)]

            metadata = {
                'total_test_functions': len(test_functions),
                'test_quality_score': round(combined_score, 3) if combined_score is not None else 0.0,
                'traditional_score': round(traditional_overall_score, 3) if traditional_overall_score is not None else 0.0,
                'vector_score': round(vector_overall_score, 3) if vector_overall_score is not None else 0.0,
                'vector_enhanced': True,
                'analysis_method': 'hybrid_traditional_vector',
                'high_quality_tests': len([func for func in test_functions
                                         if hasattr(func, 'test_quality_score') and func.test_quality_score >= 0.7]),
                'low_quality_tests': len(low_quality_tests),
                'quality_issues_count': len(all_quality_issues),
                'traditional_issues': len(traditional_quality_issues),
                'vector_issues': len(vector_quality_issues),
                'critical_quality_issues': len([issue for issue in all_quality_issues if issue.severity == 'critical']),
                'tests_without_project_imports': len([func for func in test_functions
                                                    if hasattr(func, 'imports_project_code') and not func.imports_project_code]),
                'tests_without_function_calls': len([func for func in test_functions
                                                   if hasattr(func, 'calls_project_functions') and not func.calls_project_functions]),
                'tests_using_only_mocks': len([func for func in test_functions
                                             if hasattr(func, 'uses_only_mocks') and func.uses_only_mocks])
            }

            return DriftReport(
                mode='test-quality',
                test_quality_issues=all_quality_issues,
                low_quality_tests=low_quality_tests,
                test_quality_score=combined_score,
                metadata=metadata
            )
        else:
            # Fallback to traditional analysis
            quality_issues, overall_score = self.test_quality_validator.validate_test_quality(test_functions)

            # Identify low-quality tests
            low_quality_tests = [func for func in test_functions
                               if hasattr(func, 'test_quality_score') and func.test_quality_score < 0.7]

            metadata = {
                'total_test_functions': len(test_functions),
                'test_quality_score': round(overall_score, 3) if overall_score is not None else 0.0,
                'vector_enhanced': False,
                'analysis_method': 'traditional_only',
                'high_quality_tests': len([func for func in test_functions
                                         if hasattr(func, 'test_quality_score') and func.test_quality_score >= 0.7]),
                'low_quality_tests': len(low_quality_tests),
                'quality_issues_count': len(quality_issues),
                'critical_quality_issues': len([issue for issue in quality_issues if issue.severity == 'critical']),
                'tests_without_project_imports': len([func for func in test_functions
                                                    if hasattr(func, 'imports_project_code') and not func.imports_project_code]),
                'tests_without_function_calls': len([func for func in test_functions
                                                   if hasattr(func, 'calls_project_functions') and not func.calls_project_functions]),
                'tests_using_only_mocks': len([func for func in test_functions
                                             if hasattr(func, 'uses_only_mocks') and func.uses_only_mocks])
            }

            return DriftReport(
                mode='test-quality',
                test_quality_issues=quality_issues,
                low_quality_tests=low_quality_tests,
                test_quality_score=overall_score,
                metadata=metadata
            )

    def _analyze_all_modes(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Analyze all drift modes and combine results."""
        if changed_files is not None:
            print("🔍 Starting comprehensive drift analysis (change-based)...\n")
        else:
            print("🔍 Starting comprehensive drift analysis...\n")

        # Run all individual analyses
        tc_report = self._analyze_tc_mapping(changed_files)
        ft_report = self._analyze_ft_mapping(changed_files)
        ft_tc_report = self._analyze_ft_tc_mapping(changed_files)
        coverage_report = self._analyze_code_coverage(changed_files)
        feature_report = self._analyze_feature_implementation(changed_files)
        code_location_report = self._analyze_code_location(changed_files)
        quality_report = self._analyze_test_quality(changed_files)

        # Run comprehensive drift detection
        print("🔍 Running comprehensive drift detection strategies...\n")
        comprehensive_issues = self.comprehensive_detector.analyze_all_drift()

        # Combine results
        combined_metadata = {
            **tc_report.metadata,
            **ft_tc_report.metadata,  # This includes both FT and TC metadata
            **coverage_report.metadata,
            **feature_report.metadata,
            **code_location_report.metadata,
            **quality_report.metadata,
            'comprehensive_issues_count': len(comprehensive_issues),
            'critical_issues': len([i for i in comprehensive_issues if i.severity == 'critical']),
            'warning_issues': len([i for i in comprehensive_issues if i.severity == 'warning']),
            'info_issues': len([i for i in comprehensive_issues if i.severity == 'info'])
        }

        return DriftReport(
            mode='all',
            # TC Mapping data
            test_cases_without_implementations=tc_report.test_cases_without_implementations,
            implementations_without_test_cases=tc_report.implementations_without_test_cases,
            tc_mappings=tc_report.tc_mappings,
            orphaned_tc_ids=tc_report.orphaned_tc_ids,
            # FT Mapping data (from ft_tc_report which has the most complete FT data)
            features_without_tests=ft_tc_report.features_without_tests,
            tests_without_features=ft_tc_report.tests_without_features,
            ft_mappings=ft_tc_report.ft_mappings,
            ft_tc_mappings=ft_tc_report.ft_tc_mappings,
            orphaned_ft_ids=ft_tc_report.orphaned_ft_ids,
            # Other data
            coverage_issues=coverage_report.coverage_issues,
            coverage_percentage=coverage_report.coverage_percentage,
            feature_issues=feature_report.feature_issues,
            # Code Location data
            code_location_issues=code_location_report.code_location_issues,
            # Test Quality data
            test_quality_issues=quality_report.test_quality_issues,
            low_quality_tests=quality_report.low_quality_tests,
            test_quality_score=quality_report.test_quality_score,
            drift_issues=comprehensive_issues,
            metadata=combined_metadata
        )

class TCDriftAnalyzer:
    """Analyzes drift between merged FT-TC structure and test implementations."""

    def __init__(self, root_dir: str = '.', features_dir: str = 'docs/features',
                 change_detector: Optional[GitChangeDetector] = None,
                 config_manager: Optional[ConfigurationManager] = None,
                 vector_db_manager=None):
        self.root_dir = root_dir
        self.config_manager = config_manager or ConfigurationManager(root_dir)
        self.test_case_parser = TestCaseParser(features_dir, self.config_manager)
        self.change_detector = change_detector
        self.implementation_scanner = TestImplementationScanner(root_dir, change_detector, self.config_manager)
        self.vector_db_manager = vector_db_manager

    def analyze_drift(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Perform complete drift analysis, optionally filtered by changed files."""
        if changed_files is not None:
            print("🔍 Starting TC ID drift analysis (change-based)...\n")
        else:
            print("🔍 Starting TC ID drift analysis...\n")

        # Parse test cases from merged FT-TC structure in docs/features/
        print("📋 Parsing test cases from docs/features/...")
        test_cases = self.test_case_parser.parse_test_cases(self.vector_db_manager)
        print(f"  Found {len(test_cases)} test cases")

        # Scan test implementations
        if changed_files is not None:
            print("\n🔍 Scanning test implementations (changed files only)...")
        else:
            print("\n🔍 Scanning test implementations...")
        test_functions = self.implementation_scanner.scan_all_tests(changed_files)
        print(f"  Found {len(test_functions)} test functions")

        # Build mappings
        tc_id_to_test_case = {tc.tc_id: tc for tc in test_cases}
        tc_id_to_implementations = defaultdict(list)

        # Group implementations by TC ID
        for func in test_functions:
            for tc_id in func.tc_ids:
                tc_id_to_implementations[tc_id].append(func)

        # Find drift
        test_cases_without_implementations = []
        implementations_without_test_cases = []
        orphaned_tc_ids = []

        # Test cases without implementations
        for test_case in test_cases:
            if test_case.tc_id not in tc_id_to_implementations:
                test_cases_without_implementations.append(test_case)

        # Implementations without test cases (orphaned TC IDs)
        for tc_id in tc_id_to_implementations:
            if tc_id not in tc_id_to_test_case:
                orphaned_tc_ids.append(tc_id)

        # Functions without any TC IDs
        for func in test_functions:
            if not func.tc_ids:
                implementations_without_test_cases.append(func)

        # Detect duplicate TC IDs
        duplicate_tc_issues = self._detect_duplicate_tc_ids(tc_id_to_implementations)

        # Generate metadata
        metadata = {
            'total_test_cases': len(test_cases),
            'total_test_functions': len(test_functions),
            'test_cases_with_implementations': len(test_cases) - len(test_cases_without_implementations),
            'test_functions_with_tc_ids': len([f for f in test_functions if f.tc_ids]),
            'unique_tc_ids_in_code': len(tc_id_to_implementations),
            'orphaned_tc_ids_count': len(orphaned_tc_ids),
            'duplicate_tc_ids_count': len(duplicate_tc_issues),
            'languages_detected': list(set(lang for f in test_functions
                                         if (lang := self.implementation_scanner.detector.detect_language(Path(f.file))) is not None))
        }

        return DriftReport(
            mode='tc-mapping',
            test_cases_without_implementations=test_cases_without_implementations,
            implementations_without_test_cases=implementations_without_test_cases,
            tc_mappings=dict(tc_id_to_implementations),
            orphaned_tc_ids=orphaned_tc_ids,
            duplicate_tc_issues=duplicate_tc_issues,
            metadata=metadata
        )

    def _detect_duplicate_tc_ids(self, tc_id_to_implementations: Dict[str, List[TestFunction]]) -> List[DuplicateTCIssue]:
        """Detect TC IDs that are used in multiple test functions."""
        duplicate_issues = []

        for tc_id, test_functions in tc_id_to_implementations.items():
            if len(test_functions) > 1:
                # This TC ID is used in multiple test functions
                duplicate_issue = DuplicateTCIssue(
                    tc_id=tc_id,
                    test_functions=test_functions
                )
                duplicate_issues.append(duplicate_issue)

        return duplicate_issues

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in YYYY-MM-DD_HH:MM:SS format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    def generate_report(self, report: DriftReport, output_file: str = 'tc-drift-report.yaml') -> None:
        """Generate YAML report file."""
        # Convert dataclasses to dictionaries for YAML serialization
        metadata = report.metadata or {}
        total_test_cases = metadata.get('total_test_cases', 0)
        total_test_functions = metadata.get('total_test_functions', 0)

        drift_items = len(report.test_cases_without_implementations) + len(report.implementations_without_test_cases)
        total_items = max(1, total_test_cases + total_test_functions)
        drift_percentage = (drift_items / total_items) * 100

        report_dict = {
            'metadata': metadata,
            'summary': {
                'total_test_cases': total_test_cases,
                'total_test_functions': total_test_functions,
                'test_cases_without_implementations': len(report.test_cases_without_implementations),
                'implementations_without_test_cases': len(report.implementations_without_test_cases),
                'orphaned_tc_ids': len(report.orphaned_tc_ids),
                'duplicate_tc_ids': len(report.duplicate_tc_issues),
                'drift_percentage': round(drift_percentage, 2) if drift_percentage is not None else 0.0
            },
            'test_cases_without_implementations': [asdict(tc) for tc in report.test_cases_without_implementations],
            'implementations_without_test_cases': [asdict(func) for func in report.implementations_without_test_cases],
            'orphaned_tc_ids_in_code': report.orphaned_tc_ids,
            'duplicate_tc_issues': [asdict(issue) for issue in report.duplicate_tc_issues],
            'tc_mappings': {tc_id: [asdict(func) for func in funcs]
                           for tc_id, funcs in report.tc_mappings.items()},
            'generated_at': self._get_current_timestamp()
        }

        # Write YAML report
        with open(output_file, 'w') as f:
            yaml.dump(report_dict, f, default_flow_style=False, sort_keys=False, indent=2)

        print(f"📄 Generated drift report: {output_file}")

    def print_summary(self, report: DriftReport) -> None:
        """Print a human-readable summary of the drift analysis."""
        print("\n" + "="*80)
        print("🎯 TC ID DRIFT ANALYSIS SUMMARY")
        print("="*80)

        metadata = report.metadata or {}

        print(f"\n📊 OVERVIEW:")
        print(f"  Test Cases in docs/features/: {metadata.get('total_test_cases', 0)}")
        print(f"  Test Functions in Code: {metadata.get('total_test_functions', 0)}")
        print(f"  Languages Detected: {', '.join(metadata.get('languages_detected', []))}")
        print(f"  Unique TC IDs in Code: {metadata.get('unique_tc_ids_in_code', 0)}")
        print(f"  Duplicate TC IDs: {metadata.get('duplicate_tc_ids_count', 0)}")

        # Calculate drift metrics
        total_items = metadata.get('total_test_cases', 0) + metadata.get('total_test_functions', 0)
        drift_items = len(report.test_cases_without_implementations) + len(report.implementations_without_test_cases)
        drift_percentage = (drift_items / max(1, total_items)) * 100

        print(f"\n🎯 DRIFT METRICS:")
        print(f"  Total Drift Items: {drift_items}")
        print(f"  Drift Percentage: {drift_percentage:.1f}%")

        if drift_percentage < 10:
            print("  Status: ✅ EXCELLENT - Low drift detected")
        elif drift_percentage < 25:
            print("  Status: ⚠️  MODERATE - Some drift detected")
        else:
            print("  Status: ❌ HIGH - Significant drift detected")

        # Test cases without implementations
        if report.test_cases_without_implementations:
            print(f"\n❌ TEST CASES WITHOUT IMPLEMENTATIONS ({len(report.test_cases_without_implementations)}):")
            print("-" * 60)
            for tc in sorted(report.test_cases_without_implementations, key=lambda x: x.tc_id):
                status_icon = "✅" if tc.status == "completed" else "⏸️" if tc.status == "pending" else "⏭️"
                print(f"  {status_icon} {tc.tc_id} - {tc.title[:60]}...")
                print(f"      Type: {tc.execution_type}, Priority: {tc.priority}")

        # Implementations without test cases
        if report.implementations_without_test_cases:
            print(f"\n❌ IMPLEMENTATIONS WITHOUT TC IDs ({len(report.implementations_without_test_cases)}):")
            print("-" * 60)
            by_file = defaultdict(list)
            for func in report.implementations_without_test_cases:
                by_file[func.file].append(func)

            for file_path, functions in sorted(by_file.items()):
                print(f"  📁 {file_path} ({len(functions)} functions):")
                for func in sorted(functions, key=lambda x: x.line_number or 0):
                    line_info = f":{func.line_number}" if func.line_number else ""
                    print(f"    - {func.full_name}{line_info}")

        # Orphaned TC IDs
        if report.orphaned_tc_ids:
            print(f"\n⚠️  ORPHANED TC IDs IN CODE ({len(report.orphaned_tc_ids)}):")
            print("-" * 60)
            print("  These TC IDs exist in code but not in docs/features/:")
            for tc_id in sorted(report.orphaned_tc_ids):
                implementations = report.tc_mappings.get(tc_id, [])
                print(f"    {tc_id} (used in {len(implementations)} implementations)")

        # Duplicate TC IDs
        if report.duplicate_tc_issues:
            print(f"\n⚠️  DUPLICATE TC IDs ({len(report.duplicate_tc_issues)}):")
            print("-" * 60)
            print("  These TC IDs are used in multiple test functions:")
            for issue in sorted(report.duplicate_tc_issues, key=lambda x: x.tc_id):
                print(f"    {issue.tc_id} (used in {len(issue.test_functions)} test functions)")
                for func in issue.test_functions:
                    line_info = f":{func.line_number}" if func.line_number else ""
                    print(f"      - {func.full_name} in {func.file}{line_info}")

        # Success cases
        if report.tc_mappings:
            mapped_count = len([tc_id for tc_id in report.tc_mappings
                              if tc_id not in report.orphaned_tc_ids])
            print(f"\n✅ SUCCESSFUL MAPPINGS ({mapped_count}):")
            print(f"  {mapped_count} TC IDs have proper documentation-to-implementation mapping")

        print("\n" + "="*80)

def get_current_timestamp() -> str:
    """Get current timestamp in YYYY-MM-DD_HH:MM:SS format."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def generate_multi_mode_report(report: DriftReport, output_file: str = 'drift-report.yaml') -> None:
    """Generate YAML report file for multi-mode analysis."""
    # Convert dataclasses to dictionaries for YAML serialization
    report_dict = {
        'mode': report.mode,
        'metadata': report.metadata or {},
        'generated_at': get_current_timestamp()
    }

    # Add mode-specific data
    if report.mode in ['tc-mapping', 'all']:
        report_dict.update({
            'tc_mapping_summary': {
                'total_test_cases': len(report.test_cases_without_implementations or []) + len(report.tc_mappings or {}),
                'test_cases_without_implementations': len(report.test_cases_without_implementations or []),
                'implementations_without_test_cases': len(report.implementations_without_test_cases or []),
                'orphaned_tc_ids': len(report.orphaned_tc_ids or []),
                'duplicate_tc_ids': len(report.duplicate_tc_issues or [])
            },
            'test_cases_without_implementations': [asdict(tc) for tc in (report.test_cases_without_implementations or [])],
            'implementations_without_test_cases': [asdict(func) for func in (report.implementations_without_test_cases or [])],
            'orphaned_tc_ids_in_code': report.orphaned_tc_ids or [],
            'duplicate_tc_issues': [asdict(issue) for issue in (report.duplicate_tc_issues or [])],
            'tc_mappings': {tc_id: [asdict(func) for func in funcs]
                           for tc_id, funcs in (report.tc_mappings or {}).items()}
        })

    # Add FT mapping data for ft-mapping, ft-tc-mapping, and all modes
    if report.mode in ['ft-mapping', 'ft-tc-mapping', 'all']:
        report_dict.update({
            'ft_mapping_summary': {
                'total_features': len(report.features_without_tests or []) + len(report.ft_mappings or {}),
                'features_without_tests': len(report.features_without_tests or []),
                'tests_without_features': len(report.tests_without_features or []),
                'orphaned_ft_ids': len(report.orphaned_ft_ids or []),
                'ft_tc_mappings': len(report.ft_tc_mappings or [])
            },
            'features_without_tests': [asdict(feature) for feature in (report.features_without_tests or [])],
            'tests_without_features': [asdict(func) for func in (report.tests_without_features or [])],
            'orphaned_ft_ids_in_code': report.orphaned_ft_ids or [],
            'ft_mappings': {ft_id: [asdict(func) for func in funcs]
                           for ft_id, funcs in (report.ft_mappings or {}).items()},
            'ft_tc_mappings': [asdict(mapping) for mapping in (report.ft_tc_mappings or [])]
        })

    if report.mode in ['code-coverage', 'all']:
        report_dict.update({
            'coverage_summary': {
                'coverage_percentage': report.coverage_percentage or 0.0,
                'coverage_issues_count': len(report.coverage_issues or [])
            },
            'coverage_issues': [asdict(issue) for issue in (report.coverage_issues or [])]
        })

    if report.mode in ['feature-impl', 'all']:
        report_dict.update({
            'feature_summary': {
                'feature_issues_count': len(report.feature_issues or [])
            },
            'feature_issues': [asdict(issue) for issue in (report.feature_issues or [])]
        })

    if report.mode in ['code-location', 'all']:
        report_dict.update({
            'code_location_summary': {
                'total_features': report.metadata.get('total_features', 0),
                'features_with_code_location': report.metadata.get('features_with_code_location', 0),
                'features_with_valid_location': report.metadata.get('features_with_valid_location', 0),
                'documentation_only_features': report.metadata.get('documentation_only_features', 0),
                'code_location_issues_count': len(report.code_location_issues or []),
                'coverage_percentage': report.metadata.get('coverage_percentage', 0)
            },
            'code_location_issues': [asdict(issue) for issue in (report.code_location_issues or [])]
        })

    if report.mode in ['test-quality', 'all']:
        report_dict.update({
            'test_quality_summary': {
                'test_quality_score': report.test_quality_score or 0.0,
                'quality_issues_count': len(report.test_quality_issues or []),
                'low_quality_tests_count': len(report.low_quality_tests or [])
            },
            'test_quality_issues': [asdict(issue) for issue in (report.test_quality_issues or [])],
            'low_quality_tests': [asdict(func) for func in (report.low_quality_tests or [])]
        })

    # Add comprehensive drift issues for 'all' mode
    if report.mode == 'all' and report.drift_issues:
        report_dict.update({
            'comprehensive_drift_summary': {
                'total_issues': len(report.drift_issues),
                'critical_issues': len([i for i in report.drift_issues if i.severity == 'critical']),
                'warning_issues': len([i for i in report.drift_issues if i.severity == 'warning']),
                'info_issues': len([i for i in report.drift_issues if i.severity == 'info'])
            },
            'comprehensive_drift_issues': [asdict(issue) for issue in report.drift_issues]
        })

    # Write YAML report
    with open(output_file, 'w') as f:
        yaml.dump(report_dict, f, default_flow_style=False, sort_keys=False, indent=2)

    print(f"📄 Generated drift report: {output_file}")

def print_multi_mode_summary(report: DriftReport) -> None:
    """Print a human-readable summary of the multi-mode drift analysis."""
    print("\n" + "="*80)
    print(f"🎯 {report.mode.upper().replace('-', ' ')} DRIFT ANALYSIS SUMMARY")
    print("="*80)

    if report.mode == 'tc-mapping':
        print_tc_mapping_summary(report)
    elif report.mode == 'ft-mapping':
        print_ft_mapping_summary(report)
    elif report.mode == 'ft-tc-mapping':
        print_tc_mapping_summary(report)
        print_ft_mapping_summary(report)
    elif report.mode == 'code-coverage':
        print_coverage_summary(report)
    elif report.mode == 'feature-impl':
        print_feature_summary(report)
    elif report.mode == 'code-location':
        print_code_location_summary(report)
    elif report.mode == 'test-quality':
        print_test_quality_summary(report)
    elif report.mode == 'all':
        print_tc_mapping_summary(report)
        print_ft_mapping_summary(report)
        print_coverage_summary(report)
        print_feature_summary(report)
        print_code_location_summary(report)
        print_test_quality_summary(report)
        print_comprehensive_drift_summary(report)

    print("\n" + "="*80)

def print_tc_mapping_summary(report: DriftReport) -> None:
    """Print TC mapping specific summary."""
    if not report.test_cases_without_implementations and not report.implementations_without_test_cases and not report.duplicate_tc_issues:
        return

    print(f"\n📊 TC MAPPING OVERVIEW:")
    print(f"  Test Cases Without Implementations: {len(report.test_cases_without_implementations or [])}")
    print(f"  Implementations Without TC IDs: {len(report.implementations_without_test_cases or [])}")
    print(f"  Orphaned TC IDs: {len(report.orphaned_tc_ids or [])}")
    print(f"  Duplicate TC IDs: {len(report.duplicate_tc_issues or [])}")

    # Show duplicate TC ID details if any exist
    if report.duplicate_tc_issues:
        print(f"\n⚠️  DUPLICATE TC ID DETAILS:")
        for issue in sorted(report.duplicate_tc_issues, key=lambda x: x.tc_id)[:5]:  # Show first 5
            print(f"    {issue.tc_id} used in {len(issue.test_functions)} functions:")
            for func in issue.test_functions:
                print(f"      - {func.full_name} ({func.file})")
        if len(report.duplicate_tc_issues) > 5:
            print(f"    ... and {len(report.duplicate_tc_issues) - 5} more duplicate TC IDs")

def print_ft_mapping_summary(report: DriftReport) -> None:
    """Print FT mapping specific summary."""
    if not report.features_without_tests and not report.tests_without_features and not report.ft_tc_mappings:
        return

    print(f"\n📊 FT MAPPING OVERVIEW:")
    print(f"  Features Without Tests: {len(report.features_without_tests or [])}")
    print(f"  Tests Without Features: {len(report.tests_without_features or [])}")
    print(f"  Orphaned FT IDs: {len(report.orphaned_ft_ids or [])}")
    print(f"  FT-TC Mappings: {len(report.ft_tc_mappings or [])}")

def print_coverage_summary(report: DriftReport) -> None:
    """Print code coverage specific summary."""
    if not report.coverage_issues:
        return

    print(f"\n📊 CODE COVERAGE OVERVIEW:")
    print(f"  Coverage Percentage: {report.coverage_percentage or 0:.1f}%")
    print(f"  Coverage Issues: {len(report.coverage_issues or [])}")

    # Group issues by type
    issue_types = defaultdict(int)
    for issue in (report.coverage_issues or []):
        issue_types[issue.issue_type] += 1

    for issue_type, count in issue_types.items():
        print(f"    {issue_type.replace('_', ' ').title()}: {count}")

def print_feature_summary(report: DriftReport) -> None:
    """Print feature implementation specific summary."""
    if not report.feature_issues:
        return

    print(f"\n📊 FEATURE IMPLEMENTATION OVERVIEW:")
    print(f"  Feature Issues: {len(report.feature_issues or [])}")

def print_code_location_summary(report: DriftReport) -> None:
    """Print Code Location field analysis summary."""
    if not report.code_location_issues and not hasattr(report, 'metadata'):
        return

    print(f"\n📊 CODE LOCATION ANALYSIS OVERVIEW:")

    # Get metadata with safe defaults
    metadata = report.metadata or {}
    total_features = metadata.get('total_features', 0)
    features_with_code_location = metadata.get('features_with_code_location', 0)
    features_with_valid_location = metadata.get('features_with_valid_location', 0)
    documentation_only_features = metadata.get('documentation_only_features', 0)
    coverage_percentage = metadata.get('coverage_percentage', 0)

    print(f"  Total Features: {total_features}")
    print(f"  Features with Code Location: {features_with_code_location}")
    print(f"  Features with Valid Implementation Location: {features_with_valid_location}")
    print(f"  Documentation-Only Features: {documentation_only_features}")
    print(f"  Code Location Coverage: {coverage_percentage:.1f}%")

    if report.code_location_issues:
        print(f"  Code Location Issues: {len(report.code_location_issues)}")

        # Group issues by type
        issue_types = defaultdict(int)
        for issue in report.code_location_issues:
            issue_types[issue.issue_type] += 1

        for issue_type, count in issue_types.items():
            print(f"    {issue_type.replace('_', ' ').title()}: {count}")

        # Show critical issues
        critical_issues = [issue for issue in report.code_location_issues if issue.severity == 'critical']
        high_issues = [issue for issue in report.code_location_issues if issue.severity == 'high']

        if critical_issues or high_issues:
            print(f"\n❌ HIGH PRIORITY CODE LOCATION ISSUES:")
            for issue in (critical_issues + high_issues)[:5]:  # Show first 5 high priority issues
                severity_icon = "🔴" if issue.severity == 'critical' else "🟠"
                print(f"  {severity_icon} {issue.feature_id} - {issue.feature_name}")
                print(f"    Issue: {issue.description}")
                print(f"    Suggestion: {issue.suggestion}")
                if issue.expected_path:
                    print(f"    Expected Path: {issue.expected_path}")

            total_high_priority = len(critical_issues) + len(high_issues)
            if total_high_priority > 5:
                print(f"  ... and {total_high_priority - 5} more high priority issues")
    else:
        print("  ✅ No Code Location issues found")

def print_test_quality_summary(report: DriftReport) -> None:
    """Print test quality specific summary."""
    if not report.test_quality_issues and not report.low_quality_tests:
        return

    print(f"\n📊 TEST QUALITY OVERVIEW:")
    print(f"  Test Quality Score: {(report.test_quality_score or 0) * 100:.1f}%")
    print(f"  Quality Issues: {len(report.test_quality_issues or [])}")
    print(f"  Low Quality Tests: {len(report.low_quality_tests or [])}")

    # Group issues by severity
    if report.test_quality_issues:
        issue_severities = defaultdict(int)
        for issue in report.test_quality_issues:
            issue_severities[issue.severity] += 1

        for severity, count in issue_severities.items():
            print(f"    {severity.title()} Issues: {count}")

    # Show critical quality issues
    if report.test_quality_issues:
        critical_issues = [issue for issue in report.test_quality_issues if issue.severity == 'critical']
        if critical_issues:
            print(f"\n❌ CRITICAL TEST QUALITY ISSUES:")
            for issue in critical_issues[:3]:  # Show first 3 critical issues
                print(f"  - {issue.test_function} in {issue.test_file}")
                print(f"    Issue: {issue.description}")
                print(f"    Suggestion: {issue.suggestion}")

            if len(critical_issues) > 3:
                print(f"  ... and {len(critical_issues) - 3} more critical issues")

def print_comprehensive_drift_summary(report: DriftReport) -> None:
    """Print comprehensive drift detection summary."""
    if not report.drift_issues:
        return

    print(f"\n📊 COMPREHENSIVE DRIFT OVERVIEW:")
    print(f"  Total Issues: {len(report.drift_issues)}")

    # Group by severity
    critical = [i for i in report.drift_issues if i.severity == 'critical']
    warnings = [i for i in report.drift_issues if i.severity == 'warning']
    info = [i for i in report.drift_issues if i.severity == 'info']

    print(f"  Critical Issues: {len(critical)}")
    print(f"  Warning Issues: {len(warnings)}")
    print(f"  Info Issues: {len(info)}")

    # Group by strategy
    strategies = {}
    for issue in report.drift_issues:
        if issue.strategy not in strategies:
            strategies[issue.strategy] = 0
        strategies[issue.strategy] += 1

    print(f"\n  Issues by Strategy:")
    for strategy, count in sorted(strategies.items()):
        print(f"    {strategy.replace('_', ' ').title()}: {count}")

    # Show critical issues details
    if critical:
        print(f"\n❌ CRITICAL ISSUES:")
        for issue in critical[:5]:  # Show first 5 critical issues
            print(f"  - {issue.description}")
            print(f"    Location: {issue.location}")
            print(f"    Suggestion: {issue.suggestion}")

        if len(critical) > 5:
            print(f"  ... and {len(critical) - 5} more critical issues")

def calculate_exit_code(report: DriftReport) -> int:
    """Calculate exit code based on drift level across all modes."""
    if report.mode == 'tc-mapping':
        total_items = len(report.test_cases_without_implementations or []) + len(report.implementations_without_test_cases or [])
        if total_items == 0:
            return 0
        # Use original TC mapping logic
        drift_percentage = (total_items / max(1, len(report.tc_mappings or {}) + total_items)) * 100
        if drift_percentage > 25:
            return 2
        elif drift_percentage > 10:
            return 1
        else:
            return 0
    elif report.mode == 'code-coverage':
        coverage_percentage = report.coverage_percentage or 0
        if coverage_percentage >= 80:
            return 0
        elif coverage_percentage >= 60:
            return 1
        else:
            return 2
    elif report.mode == 'feature-impl':
        issue_count = len(report.feature_issues or [])
        if issue_count == 0:
            return 0
        elif issue_count <= 3:
            return 1
        else:
            return 2
    elif report.mode == 'code-location':
        issue_count = len(report.code_location_issues or [])
        critical_issues = len([issue for issue in (report.code_location_issues or []) if issue.severity in ['critical', 'high']])
        coverage_percentage = report.metadata.get('coverage_percentage', 0) if report.metadata else 0

        if issue_count == 0 and coverage_percentage >= 90:
            return 0
        elif critical_issues == 0 and coverage_percentage >= 70:
            return 1
        else:
            return 2
    elif report.mode == 'test-quality':
        quality_score = report.test_quality_score or 0
        critical_issues = len([issue for issue in (report.test_quality_issues or []) if issue.severity == 'critical'])
        if quality_score >= 0.8 and critical_issues == 0:
            return 0
        elif quality_score >= 0.6 and critical_issues <= 2:
            return 1
        else:
            return 2
    elif report.mode == 'all':
        # Return highest exit code from all modes
        tc_code = calculate_exit_code(DriftReport(mode='tc-mapping',
                                                test_cases_without_implementations=report.test_cases_without_implementations,
                                                implementations_without_test_cases=report.implementations_without_test_cases,
                                                tc_mappings=report.tc_mappings))
        coverage_code = calculate_exit_code(DriftReport(mode='code-coverage',
                                                      coverage_percentage=report.coverage_percentage,
                                                      coverage_issues=report.coverage_issues))
        feature_code = calculate_exit_code(DriftReport(mode='feature-impl',
                                                     feature_issues=report.feature_issues))
        code_location_code = calculate_exit_code(DriftReport(mode='code-location',
                                                           code_location_issues=report.code_location_issues,
                                                           metadata=report.metadata))
        quality_code = calculate_exit_code(DriftReport(mode='test-quality',
                                                     test_quality_score=report.test_quality_score,
                                                     test_quality_issues=report.test_quality_issues))
        return max(tc_code, coverage_code, feature_code, code_location_code, quality_code)

    return 0

def main():
    """Main function to run multi-mode drift analysis."""
    import argparse

    parser = argparse.ArgumentParser(description='Multi-mode drift scanner for Agent3D framework')
    parser.add_argument('--mode', default='tc-mapping',
                       choices=['tc-mapping', 'ft-mapping', 'ft-tc-mapping', 'code-coverage', 'feature-impl', 'code-location', 'test-quality', 'all'],
                       help='Drift analysis mode (default: tc-mapping)')
    parser.add_argument('--root-dir', default='.', help='Root directory to scan (default: current directory)')
    parser.add_argument('--test-cases-file', default='docs/features',
                       help='Path to features directory or legacy TEST-CASES.md file (default: docs/features)')
    parser.add_argument('--output', default=None,
                       help='Output YAML file (default: auto-generated in .agent3d-tmp/drift-reports/)')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')
    parser.add_argument('--enable-vector-db', action='store_true',
                       help='Enable vector database for enhanced file discovery (requires vector dependencies)')

    # Change-based scanning options
    parser.add_argument('--changed-only', action='store_true',
                       help='Only scan files changed since last commit (requires Git)')
    parser.add_argument('--changed-since', default=None,
                       help='Only scan files changed since specified commit/branch (e.g., main, HEAD~5)')
    parser.add_argument('--pr-diff', action='store_true',
                       help='Only scan files changed in current branch vs main (requires Git)')
    parser.add_argument('--recent-days', type=int, default=None,
                       help='Only scan files changed in the last N days (requires Git)')

    args = parser.parse_args()

    # Initialize change detector and determine changed files
    change_detector = GitChangeDetector(args.root_dir)
    changed_files = None

    if args.changed_only:
        changed_files = change_detector.get_changed_files()
        if not args.quiet:
            print(f"🔄 Change-based scanning: {len(changed_files)} changed files detected")
    elif args.changed_since:
        changed_files = change_detector.get_changed_files(since=args.changed_since)
        if not args.quiet:
            print(f"🔄 Change-based scanning since {args.changed_since}: {len(changed_files)} changed files detected")
    elif args.pr_diff:
        changed_files = change_detector.get_changed_files_in_pr()
        if not args.quiet:
            print(f"🔄 PR diff scanning: {len(changed_files)} changed files detected")
    elif args.recent_days:
        changed_files = change_detector.get_recently_changed_files(args.recent_days)
        if not args.quiet:
            print(f"🔄 Recent changes ({args.recent_days} days): {len(changed_files)} changed files detected")

    # Initialize logging
    log_file = get_log_file_path()
    log_analysis_start(args.mode, args.root_dir, log_file)

    # Initialize multi-mode analyzer
    analyzer = MultiModeDriftAnalyzer(args.root_dir, args.test_cases_file, change_detector,
                                    enable_vector_db=args.enable_vector_db)

    # Determine output file path - always use .agent3d-tmp directory
    if args.output:
        # Ensure custom output is also in .agent3d-tmp directory
        if not args.output.startswith('.agent3d-tmp/'):
            output_file = f".agent3d-tmp/drift-reports/{args.output}"
        else:
            output_file = args.output
    else:
        output_file = get_default_output_path(args.mode)

    if not args.quiet:
        print(f"📁 Working directory: {args.root_dir}")
        print(f"📄 Output file: {output_file}")
        print(f"📝 Log file: {log_file}")

    # Perform analysis
    try:
        report = analyzer.analyze_drift(args.mode, changed_files)
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1

    # Generate report
    try:
        generate_multi_mode_report(report, output_file)
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1

    # Print summary unless quiet mode
    if not args.quiet:
        print_multi_mode_summary(report)

    # Return exit code based on drift level
    return calculate_exit_code(report)

if __name__ == "__main__":
    exit(main())