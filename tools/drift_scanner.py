#!/usr/bin/env python3
"""
Multi-mode drift scanner for Agent3D framework.
Detects various types of drift between documentation and implementation.

Supported drift detection modes:
- tc-mapping: TC ID mapping between TEST-CASES.md and test implementations
- ft-mapping: FT ID mapping between FEATURES.md and test implementations
- ft-tc-mapping: FT-* ↔ TC-* relationship mapping and validation
- code-coverage: Test coverage analysis and missing test detection
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
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict

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

    def __post_init__(self):
        if self.tc_ids is None:
            self.tc_ids = []

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
class DriftReport:
    """Complete multi-mode drift analysis report."""
    mode: str
    # TC Mapping (original)
    test_cases_without_implementations: List[TestCase] = None
    implementations_without_test_cases: List[TestFunction] = None
    tc_mappings: Dict[str, List[TestFunction]] = None
    orphaned_tc_ids: List[str] = None
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
        'go': {
            'file_patterns': ['*_test.go'],
            'test_function_patterns': [
                r'func\s+(Test\w+)\s*\(',  # func TestSomething(
                r'func\s+(Benchmark\w+)\s*\(',  # func BenchmarkSomething(
            ],
            'class_patterns': [],
            'tc_id_pattern': r'TC-[A-Z0-9]+-\d+[a-z]?',
            'comment_patterns': ['//'],
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
        elif suffix == '.go':
            return 'go'
        elif suffix == '.rs':
            return 'rust'
        return None

    @classmethod
    def get_patterns(cls, language: str) -> Dict:
        """Get language-specific patterns."""
        return cls.LANGUAGE_PATTERNS.get(language, {})

class TestCaseParser:
    """Parses TEST-CASES.md to extract test case definitions."""

    def __init__(self, test_cases_file: str = 'docs/TEST-CASES.md',
                 config_manager: Optional[ConfigurationManager] = None):
        self.test_cases_file = test_cases_file
        self.config_manager = config_manager or ConfigurationManager('.')

    def parse_test_cases(self) -> List[TestCase]:
        """Parse TEST-CASES.md and extract all test cases."""
        if not Path(self.test_cases_file).exists():
            print(f"⚠️  TEST-CASES.md not found at {self.test_cases_file}")
            return []

        test_cases = []

        try:
            with open(self.test_cases_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {self.test_cases_file}: {e}")
            return []

        # Pattern to match test cases using configured TC pattern
        tc_strict_pattern = self.config_manager.get_pattern_for_prefix('TC-', flexible=False)
        tc_pattern = rf'- \[([x~\s])\] \*\*({tc_strict_pattern})\*\* - ([^(]+)\(([^,]+),\s*([^)]+)\)'

        # Pattern for sub-test cases using configured TC pattern
        sub_tc_pattern = rf'\s+- \[([x~\s])\] \*\*({tc_strict_pattern})\*\* - ([^(]+)\(([^,]+),\s*([^)]+)\)'

        current_parent = None

        for line in content.split('\n'):
            # Check for main test cases
            main_match = re.match(tc_pattern, line.strip())
            if main_match:
                status_char, tc_id, title, exec_type, priority = main_match.groups()
                status = 'completed' if status_char == 'x' else 'pending' if status_char == '~' else 'pending'

                test_case = TestCase(
                    tc_id=tc_id,
                    title=title.strip(),
                    status=status,
                    execution_type=exec_type.strip(),
                    priority=priority.strip(),
                    is_sub_case=False
                )
                test_cases.append(test_case)
                current_parent = tc_id
                continue

            # Check for sub-test cases
            sub_match = re.match(sub_tc_pattern, line)
            if sub_match:
                status_char, tc_id, title, exec_type, priority = sub_match.groups()
                status = 'completed' if status_char == 'x' else 'pending' if status_char == '~' else 'pending'

                test_case = TestCase(
                    tc_id=tc_id,
                    title=title.strip(),
                    status=status,
                    execution_type=exec_type.strip(),
                    priority=priority.strip(),
                    is_sub_case=True,
                    parent_tc_id=current_parent
                )
                test_cases.append(test_case)

        return test_cases

class FeatureParser:
    """Parses FEATURES.md to extract feature definitions."""

    def __init__(self, features_file: str = 'docs/FEATURES.md',
                 config_manager: Optional[ConfigurationManager] = None):
        self.features_file = features_file
        self.config_manager = config_manager or ConfigurationManager('.')

    def parse_features(self) -> List[Feature]:
        """Parse FEATURES.md and extract all features."""
        if not Path(self.features_file).exists():
            print(f"⚠️  FEATURES.md not found at {self.features_file}")
            return []

        features = []

        try:
            with open(self.features_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {self.features_file}: {e}")
            return []

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
    """Analyzes drift between FEATURES.md and test implementations, including FT-TC relationships."""

    def __init__(self, root_dir: str = '.', features_file: str = 'docs/FEATURES.md',
                 test_cases_file: str = 'docs/TEST-CASES.md',
                 config_manager: Optional[ConfigurationManager] = None):
        self.root_dir = root_dir
        self.config_manager = config_manager or ConfigurationManager(root_dir)
        self.feature_parser = FeatureParser(features_file, self.config_manager)
        self.test_case_parser = TestCaseParser(test_cases_file, self.config_manager)

    def analyze_ft_drift(self, test_functions: List[TestFunction]) -> DriftReport:
        """Analyze FT-* feature drift and FT-TC relationships."""
        print("🔍 Starting FT-* feature drift analysis...\n")

        # Parse features and test cases
        features = self.feature_parser.parse_features()
        test_cases = self.test_case_parser.parse_test_cases()

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
        elif language == 'go':
            test_functions.extend(self._scan_go_tests(file_path, content))
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

    def _scan_go_tests(self, file_path: Path, content: str) -> List[TestFunction]:
        """Scan Go test files."""
        test_functions = []

        # Find Test functions
        test_pattern = r'func\s+(Test\w+)\s*\('
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

        # Find Benchmark functions
        benchmark_pattern = r'func\s+(Benchmark\w+)\s*\('
        benchmark_matches = re.finditer(benchmark_pattern, content)

        for benchmark_match in benchmark_matches:
            func_name = benchmark_match.group(1)
            test_position = benchmark_match.start()

            tc_ids = self._find_tc_ids_near_position(content, test_position)
            line_number = self._get_line_number(content, test_position)

            test_functions.append(TestFunction(
                file=str(file_path),
                function=func_name,
                full_name=func_name,
                type='benchmark_function',
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
            'go': ['*.go', 'cmd/**/*.go', 'pkg/**/*.go'],
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
                name.endswith('Test.java') or name.endswith('_test.go'))

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

        elif language == 'go':
            # Find Go functions
            pattern = r'func\s+(?:\([^)]*\)\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                if func_name[0].isupper():  # Only public functions
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

        elif language == 'go':
            test_name = f"{source_file.stem}_test.go"
            test_path = source_file.parent / test_name
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

class FeatureImplementationScanner:
    """Scans for feature implementation drift between FEATURES.md and actual implementation."""

    def __init__(self, root_dir: str = '.', features_file: str = 'docs/FEATURES.md'):
        self.root_dir = Path(root_dir)
        self.features_file = features_file

    def parse_features(self) -> List[Dict]:
        """Parse FEATURES.md to extract feature definitions."""
        if not Path(self.features_file).exists():
            print(f"⚠️  FEATURES.md not found at {self.features_file}")
            return []

        features = []

        try:
            with open(self.features_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {self.features_file}: {e}")
            return []

        # Pattern to match features: - [x] Feature name - Description
        feature_pattern = r'- \[([x~\s])\] \*\*([^*]+)\*\* - ([^(]+)(?:\(([^)]+)\))?'

        for match in re.finditer(feature_pattern, content):
            status_char, feature_name, description, priority = match.groups()
            status = 'completed' if status_char == 'x' else 'pending' if status_char == '~' else 'pending'

            features.append({
                'name': feature_name.strip(),
                'description': description.strip(),
                'status': status,
                'priority': priority.strip() if priority else 'Medium'
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

class MultiModeDriftAnalyzer:
    """Multi-mode drift analyzer that can run different types of drift detection."""

    def __init__(self, root_dir: str = '.', test_cases_file: str = 'docs/TEST-CASES.md',
                 change_detector: Optional[GitChangeDetector] = None):
        self.root_dir = root_dir
        self.test_cases_file = test_cases_file
        self.change_detector = change_detector
        self.config_manager = ConfigurationManager(root_dir)

        # Initialize individual scanners with configuration
        self.tc_analyzer = TCDriftAnalyzer(root_dir, test_cases_file, change_detector, self.config_manager)
        self.ft_analyzer = FTDriftAnalyzer(root_dir, 'docs/FEATURES.md', test_cases_file, self.config_manager)
        self.coverage_scanner = CodeCoverageScanner(root_dir)
        self.feature_scanner = FeatureImplementationScanner(root_dir, self.config_manager)
        self.comprehensive_detector = ComprehensiveDriftDetector(root_dir, self.config_manager)

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
        """Analyze FT ID mapping drift."""
        if changed_files is not None:
            print("🔍 Starting FT ID mapping drift analysis (change-based)...\n")
        else:
            print("🔍 Starting FT ID mapping drift analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Analyze FT drift
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
        """Analyze code coverage drift."""
        if changed_files is not None:
            print("🔍 Starting code coverage drift analysis (change-based)...\n")
        else:
            print("🔍 Starting code coverage drift analysis...\n")

        # Get test functions first
        test_functions = self.tc_analyzer.implementation_scanner.scan_all_tests(changed_files)

        # Analyze coverage issues
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
            'coverage_percentage': round(coverage_percentage, 2)
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

        # Run comprehensive drift detection
        print("🔍 Running comprehensive drift detection strategies...\n")
        comprehensive_issues = self.comprehensive_detector.analyze_all_drift()

        # Combine results
        combined_metadata = {
            **tc_report.metadata,
            **ft_tc_report.metadata,  # This includes both FT and TC metadata
            **coverage_report.metadata,
            **feature_report.metadata,
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
            drift_issues=comprehensive_issues,
            metadata=combined_metadata
        )

class TCDriftAnalyzer:
    """Analyzes drift between TEST-CASES.md and test implementations."""

    def __init__(self, root_dir: str = '.', test_cases_file: str = 'docs/TEST-CASES.md',
                 change_detector: Optional[GitChangeDetector] = None,
                 config_manager: Optional[ConfigurationManager] = None):
        self.root_dir = root_dir
        self.config_manager = config_manager or ConfigurationManager(root_dir)
        self.test_case_parser = TestCaseParser(test_cases_file, self.config_manager)
        self.change_detector = change_detector
        self.implementation_scanner = TestImplementationScanner(root_dir, change_detector, self.config_manager)

    def analyze_drift(self, changed_files: Optional[Set[Path]] = None) -> DriftReport:
        """Perform complete drift analysis, optionally filtered by changed files."""
        if changed_files is not None:
            print("🔍 Starting TC ID drift analysis (change-based)...\n")
        else:
            print("🔍 Starting TC ID drift analysis...\n")

        # Parse test cases from TEST-CASES.md
        print("📋 Parsing TEST-CASES.md...")
        test_cases = self.test_case_parser.parse_test_cases()
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

        # Generate metadata
        metadata = {
            'total_test_cases': len(test_cases),
            'total_test_functions': len(test_functions),
            'test_cases_with_implementations': len(test_cases) - len(test_cases_without_implementations),
            'test_functions_with_tc_ids': len([f for f in test_functions if f.tc_ids]),
            'unique_tc_ids_in_code': len(tc_id_to_implementations),
            'orphaned_tc_ids_count': len(orphaned_tc_ids),
            'languages_detected': list(set(self.implementation_scanner.detector.detect_language(Path(f.file))
                                         for f in test_functions if self.implementation_scanner.detector.detect_language(Path(f.file))))
        }

        return DriftReport(
            mode='tc-mapping',
            test_cases_without_implementations=test_cases_without_implementations,
            implementations_without_test_cases=implementations_without_test_cases,
            tc_mappings=dict(tc_id_to_implementations),
            orphaned_tc_ids=orphaned_tc_ids,
            metadata=metadata
        )

    def generate_report(self, report: DriftReport, output_file: str = 'tc-drift-report.yaml') -> None:
        """Generate YAML report file."""
        # Convert dataclasses to dictionaries for YAML serialization
        report_dict = {
            'metadata': report.metadata,
            'summary': {
                'total_test_cases': report.metadata['total_test_cases'],
                'total_test_functions': report.metadata['total_test_functions'],
                'test_cases_without_implementations': len(report.test_cases_without_implementations),
                'implementations_without_test_cases': len(report.implementations_without_test_cases),
                'orphaned_tc_ids': len(report.orphaned_tc_ids),
                'drift_percentage': round((len(report.test_cases_without_implementations) +
                                         len(report.implementations_without_test_cases)) /
                                        max(1, report.metadata['total_test_cases'] +
                                            report.metadata['total_test_functions']) * 100, 2)
            },
            'test_cases_without_implementations': [asdict(tc) for tc in report.test_cases_without_implementations],
            'implementations_without_test_cases': [asdict(func) for func in report.implementations_without_test_cases],
            'orphaned_tc_ids_in_code': report.orphaned_tc_ids,
            'tc_mappings': {tc_id: [asdict(func) for func in funcs]
                           for tc_id, funcs in report.tc_mappings.items()},
            'generated_at': f"$(date +%Y-%m-%d_%H:%M:%S)"
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

        print(f"\n📊 OVERVIEW:")
        print(f"  Test Cases in TEST-CASES.md: {report.metadata['total_test_cases']}")
        print(f"  Test Functions in Code: {report.metadata['total_test_functions']}")
        print(f"  Languages Detected: {', '.join(report.metadata['languages_detected'])}")
        print(f"  Unique TC IDs in Code: {report.metadata['unique_tc_ids_in_code']}")

        # Calculate drift metrics
        total_items = report.metadata['total_test_cases'] + report.metadata['total_test_functions']
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
            print("  These TC IDs exist in code but not in TEST-CASES.md:")
            for tc_id in sorted(report.orphaned_tc_ids):
                implementations = report.tc_mappings.get(tc_id, [])
                print(f"    {tc_id} (used in {len(implementations)} implementations)")

        # Success cases
        if report.tc_mappings:
            mapped_count = len([tc_id for tc_id in report.tc_mappings
                              if tc_id not in report.orphaned_tc_ids])
            print(f"\n✅ SUCCESSFUL MAPPINGS ({mapped_count}):")
            print(f"  {mapped_count} TC IDs have proper documentation-to-implementation mapping")

        print("\n" + "="*80)

def generate_multi_mode_report(report: DriftReport, output_file: str = 'drift-report.yaml') -> None:
    """Generate YAML report file for multi-mode analysis."""
    # Convert dataclasses to dictionaries for YAML serialization
    report_dict = {
        'mode': report.mode,
        'metadata': report.metadata or {},
        'generated_at': f"$(date +%Y-%m-%d_%H:%M:%S)"
    }

    # Add mode-specific data
    if report.mode in ['tc-mapping', 'all']:
        report_dict.update({
            'tc_mapping_summary': {
                'total_test_cases': len(report.test_cases_without_implementations or []) + len(report.tc_mappings or {}),
                'test_cases_without_implementations': len(report.test_cases_without_implementations or []),
                'implementations_without_test_cases': len(report.implementations_without_test_cases or []),
                'orphaned_tc_ids': len(report.orphaned_tc_ids or [])
            },
            'test_cases_without_implementations': [asdict(tc) for tc in (report.test_cases_without_implementations or [])],
            'implementations_without_test_cases': [asdict(func) for func in (report.implementations_without_test_cases or [])],
            'orphaned_tc_ids_in_code': report.orphaned_tc_ids or [],
            'tc_mappings': {tc_id: [asdict(func) for func in funcs]
                           for tc_id, funcs in (report.tc_mappings or {}).items()}
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
    elif report.mode == 'code-coverage':
        print_coverage_summary(report)
    elif report.mode == 'feature-impl':
        print_feature_summary(report)
    elif report.mode == 'all':
        print_tc_mapping_summary(report)
        print_coverage_summary(report)
        print_feature_summary(report)
        print_comprehensive_drift_summary(report)

    print("\n" + "="*80)

def print_tc_mapping_summary(report: DriftReport) -> None:
    """Print TC mapping specific summary."""
    if not report.test_cases_without_implementations and not report.implementations_without_test_cases:
        return

    print(f"\n📊 TC MAPPING OVERVIEW:")
    print(f"  Test Cases Without Implementations: {len(report.test_cases_without_implementations or [])}")
    print(f"  Implementations Without TC IDs: {len(report.implementations_without_test_cases or [])}")
    print(f"  Orphaned TC IDs: {len(report.orphaned_tc_ids or [])}")

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
        return max(tc_code, coverage_code, feature_code)

    return 0

def main():
    """Main function to run multi-mode drift analysis."""
    import argparse

    parser = argparse.ArgumentParser(description='Multi-mode drift scanner for Agent3D framework')
    parser.add_argument('--mode', default='tc-mapping',
                       choices=['tc-mapping', 'ft-mapping', 'ft-tc-mapping', 'code-coverage', 'feature-impl', 'all'],
                       help='Drift analysis mode (default: tc-mapping)')
    parser.add_argument('--root-dir', default='.', help='Root directory to scan (default: current directory)')
    parser.add_argument('--test-cases-file', default='docs/TEST-CASES.md',
                       help='Path to TEST-CASES.md file (default: docs/TEST-CASES.md)')
    parser.add_argument('--output', default=None,
                       help='Output YAML file (default: auto-generated in .agent3d-tmp/drift-reports/)')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

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
    analyzer = MultiModeDriftAnalyzer(args.root_dir, args.test_cases_file, change_detector)

    # Determine output file path
    output_file = args.output if args.output else get_default_output_path(args.mode)

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