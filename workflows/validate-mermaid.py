#!/usr/bin/env python3
"""
Mermaid Syntax Validator

This script validates Mermaid diagram syntax by checking for common issues
and optionally using the Mermaid CLI if available.

Usage:
    python workflows/validate-mermaid.py [file.mmd]

Returns:
    0 if valid
    1 if syntax issues found
"""

import sys
import re
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple


class MermaidValidator:
    """Validates Mermaid diagram syntax."""

    def __init__(self, mermaid_file: str):
        self.mermaid_file = Path(mermaid_file)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if valid."""
        print(f"🔍 Validating Mermaid syntax: {self.mermaid_file}")
        print()

        if not self.mermaid_file.exists():
            self.errors.append(f"File not found: {self.mermaid_file}")
            self._report_results()
            return False

        content = self._load_content()
        if not content:
            return False

        # Run validation checks
        self._validate_basic_syntax(content)
        self._validate_node_definitions(content)
        self._validate_connections(content)
        self._validate_text_content(content)

        # Try CLI validation if available
        self._validate_with_cli()

        # Report results
        self._report_results()

        return len(self.errors) == 0

    def _load_content(self) -> str:
        """Load Mermaid file content."""
        try:
            with open(self.mermaid_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.errors.append(f"Failed to read file: {e}")
            return ""

    def _validate_basic_syntax(self, content: str):
        """Validate basic Mermaid syntax."""
        print("📋 Validating basic syntax...")

        # Check for diagram type
        if not re.search(r'^(flowchart|graph|sequenceDiagram|classDiagram)', content, re.MULTILINE):
            self.errors.append("No valid diagram type found (flowchart, graph, etc.)")

        # Check for flowchart direction
        if 'flowchart' in content and not re.search(r'flowchart\s+(TD|TB|BT|RL|LR)', content):
            self.warnings.append("Flowchart direction not specified (TD, TB, BT, RL, LR)")

    def _validate_node_definitions(self, content: str):
        """Validate node definitions."""
        print("🔗 Validating node definitions...")

        # Find all node definitions (rectangles, diamonds, etc.)
        node_patterns = [
            r'(\w+)\[([^\]]*)\]',  # Rectangle nodes
            r'(\w+)\{([^}]*)\}',   # Diamond nodes
            r'(\w+)\(([^)]*)\)',   # Round nodes
        ]

        defined_nodes = set()
        for pattern in node_patterns:
            nodes = re.findall(pattern, content)
            for node_id, node_text in nodes:
                defined_nodes.add(node_id)
                if not node_text.strip():
                    self.warnings.append(f"Empty node text for: {node_id}")

        # Find all node references in connections
        reference_pattern = r'(\w+)\s*-->'
        references = re.findall(reference_pattern, content)

        # Also find nodes that are targets of connections
        target_pattern = r'-->\s*(\w+)'
        targets = re.findall(target_pattern, content)

        all_referenced = set(references + targets)

        # Check for undefined nodes (but allow some common patterns)
        undefined = all_referenced - defined_nodes
        # Filter out nodes that are defined inline in connections
        inline_defined = re.findall(r'-->\s*(\w+)\[', content)
        undefined = undefined - set(inline_defined)

        if undefined:
            self.warnings.append(f"Referenced but not explicitly defined nodes: {undefined}")

    def _validate_connections(self, content: str):
        """Validate node connections."""
        print("🔄 Validating connections...")

        # Check for valid connection syntax
        connection_patterns = [
            r'\w+\s*-->\s*\w+',  # Basic arrow
            r'\w+\s*-->\|\w*\|\s*\w+',  # Arrow with label
            r'\w+\s*-\.\s*\w+',  # Dotted line
        ]

        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if '-->' in line or '-.' in line:
                # Check if it matches any valid pattern
                valid = any(re.search(pattern, line) for pattern in connection_patterns)
                if not valid and not line.startswith('%%') and line:
                    self.warnings.append(f"Line {i}: Potentially invalid connection syntax: {line}")

    def _validate_text_content(self, content: str):
        """Validate text content for problematic characters."""
        print("📝 Validating text content...")

        # Check for problematic characters in node text
        problematic_chars = ['(', ')', '{', '}', '[', ']', '"', "'"]

        # Find text within brackets
        text_pattern = r'\[([^\]]*)\]'
        texts = re.findall(text_pattern, content)

        for text in texts:
            # Check for unescaped problematic characters
            for char in problematic_chars:
                if char in text and f'#{char}' not in text:  # Simple check for HTML entities
                    self.warnings.append(f"Potentially problematic character '{char}' in text: {text[:50]}...")

            # Check for very long text that might cause rendering issues
            if len(text) > 200:
                self.warnings.append(f"Very long node text (>{len(text)} chars): {text[:50]}...")

    def _validate_with_cli(self):
        """Validate using Mermaid CLI if available."""
        print("🛠️ Checking for Mermaid CLI...")

        # Check if mmdc (Mermaid CLI) is available
        if not shutil.which('mmdc'):
            self.warnings.append("Mermaid CLI (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli")
            return

        print("✅ Mermaid CLI found, validating...")

        try:
            # Try to parse the diagram (output to temp file)
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                result = subprocess.run(
                    ['mmdc', '-i', str(self.mermaid_file), '-o', tmp.name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            if result.returncode != 0:
                self.errors.append(f"Mermaid CLI validation failed: {result.stderr}")
            else:
                print("✅ Mermaid CLI validation passed")

        except subprocess.TimeoutExpired:
            self.warnings.append("Mermaid CLI validation timed out")
        except Exception as e:
            self.warnings.append(f"Mermaid CLI validation error: {e}")

    def _report_results(self):
        """Report validation results."""
        print("\n" + "="*60)
        print("📊 MERMAID VALIDATION RESULTS")
        print("="*60)

        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
            print()

        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ PERFECT MERMAID SYNTAX")
            print("   No issues found!")
        elif not self.errors:
            print("✅ VALID MERMAID SYNTAX (with warnings)")
            print("   Syntax is valid but has minor issues.")
        else:
            print("❌ INVALID MERMAID SYNTAX")
            print("   Critical syntax errors found.")

        print("="*60)


def main():
    """Main validation function."""
    if len(sys.argv) > 1:
        mermaid_file = sys.argv[1]
    else:
        mermaid_file = "workflows/ddd-workflow.mmd"

    validator = MermaidValidator(mermaid_file)
    is_valid = validator.validate()

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
