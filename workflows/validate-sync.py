#!/usr/bin/env python3
"""
DDD Workflow Synchronization Validator

This script validates that the YAML workflow definition and Mermaid flowchart
are properly synchronized and consistent.

Usage:
    python workflows/validate-sync.py

Returns:
    0 if synchronized
    1 if synchronization issues found
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class WorkflowSyncValidator:
    """Validates synchronization between YAML workflow and Mermaid flowchart."""

    def __init__(self, yaml_path: str, mermaid_path: str):
        self.yaml_path = Path(yaml_path)
        self.mermaid_path = Path(mermaid_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if synchronized."""
        print("🔍 Validating DDD Workflow Synchronization...")
        print(f"📄 YAML: {self.yaml_path}")
        print(f"📊 Mermaid: {self.mermaid_path}")
        print()

        # Load files
        yaml_data = self._load_yaml()
        mermaid_content = self._load_mermaid()

        if not yaml_data or not mermaid_content:
            return False

        # Run validation checks
        self._validate_metadata(yaml_data, mermaid_content)
        self._validate_steps(yaml_data, mermaid_content)
        self._validate_decisions(yaml_data, mermaid_content)
        self._validate_deliverables(yaml_data, mermaid_content)

        # Report results
        self._report_results()

        return len(self.errors) == 0

    def _load_yaml(self) -> Dict:
        """Load and parse YAML workflow file."""
        try:
            with open(self.yaml_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load YAML file: {e}")
            return {}

    def _load_mermaid(self) -> str:
        """Load Mermaid flowchart content."""
        try:
            with open(self.mermaid_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.errors.append(f"Failed to load Mermaid file: {e}")
            return ""

    def _validate_metadata(self, yaml_data: Dict, mermaid_content: str):
        """Validate metadata synchronization."""
        print("📋 Validating metadata...")

        # Check version synchronization
        yaml_version = yaml_data.get('metadata', {}).get('version', 'unknown')

        # Extract version from Mermaid file
        version_match = re.search(r'Version:\s*([^\n]+)', mermaid_content)
        mermaid_version = version_match.group(1).strip() if version_match else 'unknown'

        if yaml_version != mermaid_version:
            self.errors.append(f"Version mismatch: YAML={yaml_version}, Mermaid={mermaid_version}")

        # Check sync file references
        yaml_sync = yaml_data.get('metadata', {}).get('sync_with', '')
        if 'ddd-workflow-flowchart.md' not in yaml_sync:
            self.warnings.append("YAML doesn't reference Mermaid sync file")

    def _validate_steps(self, yaml_data: Dict, mermaid_content: str):
        """Validate workflow steps synchronization."""
        print("🔄 Validating workflow steps...")

        # Extract YAML steps
        yaml_steps = set(yaml_data.get('workflow', {}).get('steps', {}).keys())

        # Extract Mermaid step nodes
        step_pattern = r'STEP\d+\[.*?Step \d+:'
        mermaid_steps = set(re.findall(step_pattern, mermaid_content))

        # Map YAML step IDs to expected Mermaid nodes
        expected_mappings = {
            'start': 'START',
            'step-0-requirements': 'STEP0',
            'step-1-foundation': 'STEP1',
            'step-2-development': 'STEP2',
            'step-3-synchronization': 'STEP3',
            'step-4-code-review': 'STEP4',
            'step-5-refactoring': 'STEP5',
            'step-6-documentation': 'STEP6',
            'workflow_complete': 'COMPLETE'
        }

        # Validate step presence
        for yaml_step in yaml_steps:
            if yaml_step in expected_mappings:
                expected_node = expected_mappings[yaml_step]
                if expected_node not in mermaid_content:
                    self.errors.append(f"Missing Mermaid node for YAML step: {yaml_step} -> {expected_node}")

        # Check for extra Mermaid nodes
        defined_nodes = set(expected_mappings.values())
        mermaid_nodes = set(re.findall(r'(\w+)\[', mermaid_content))
        extra_nodes = mermaid_nodes - defined_nodes - {'DECISION_START', 'DELIVERABLES'}  # Allow some extra nodes

        if extra_nodes:
            self.warnings.append(f"Extra Mermaid nodes not in YAML: {extra_nodes}")

    def _validate_decisions(self, yaml_data: Dict, mermaid_content: str):
        """Validate decision logic synchronization."""
        print("🤔 Validating decision logic...")

        # Extract decision conditions from YAML
        yaml_decisions = []
        for step_id, step_data in yaml_data.get('workflow', {}).get('steps', {}).items():
            decisions = step_data.get('decisions', [])
            for decision in decisions:
                yaml_decisions.append({
                    'step': step_id,
                    'condition': decision.get('condition', ''),
                    'next': decision.get('next', '')
                })

        # Extract decision diamonds from Mermaid
        decision_pattern = r'(\w+_DECISION)\{([^}]+)\}'
        mermaid_decisions = re.findall(decision_pattern, mermaid_content)

        # Basic validation - ensure we have decision nodes
        if len(yaml_decisions) > 0 and len(mermaid_decisions) == 0:
            self.errors.append("YAML has decisions but Mermaid has no decision diamonds")

        # Check for major decision points
        critical_decisions = ['Requirements', 'Foundation', 'Testing', 'Sync']
        for decision in critical_decisions:
            if not any(decision in str(md) for md in mermaid_decisions):
                self.warnings.append(f"Missing critical decision in Mermaid: {decision}")

    def _validate_deliverables(self, yaml_data: Dict, mermaid_content: str):
        """Validate final deliverables synchronization."""
        print("📦 Validating deliverables...")

        # Extract YAML deliverables
        yaml_deliverables = set()
        complete_step = yaml_data.get('workflow', {}).get('steps', {}).get('workflow_complete', {})
        deliverables = complete_step.get('final_deliverables', [])

        for deliverable in deliverables:
            # Extract key terms from deliverable descriptions
            if 'REQUIREMENTS.md' in deliverable:
                yaml_deliverables.add('REQUIREMENTS.md')
            if 'FEATURES.md' in deliverable:
                yaml_deliverables.add('FEATURES.md')
            if 'TEST-CASES.md' in deliverable:
                yaml_deliverables.add('TEST-CASES.md')

        # Check Mermaid deliverables section
        deliverables_section = re.search(r'DELIVERABLES\[.*?\]', mermaid_content, re.DOTALL)
        if deliverables_section:
            mermaid_deliverables_text = deliverables_section.group(0)

            for yaml_deliverable in yaml_deliverables:
                if yaml_deliverable not in mermaid_deliverables_text:
                    self.errors.append(f"Missing deliverable in Mermaid: {yaml_deliverable}")
        else:
            self.errors.append("No deliverables section found in Mermaid")

    def _report_results(self):
        """Report validation results."""
        print("\n" + "="*60)
        print("📊 VALIDATION RESULTS")
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
            print("✅ PERFECT SYNCHRONIZATION")
            print("   YAML and Mermaid files are perfectly synchronized!")
        elif not self.errors:
            print("✅ SYNCHRONIZED (with warnings)")
            print("   Files are synchronized but have minor issues.")
        else:
            print("❌ SYNCHRONIZATION FAILED")
            print("   Critical synchronization issues found.")

        print("="*60)


def main():
    """Main validation function."""
    yaml_path = "workflows/ddd-workflow.yml"
    mermaid_path = "workflows/ddd-workflow.mmd"

    validator = WorkflowSyncValidator(yaml_path, mermaid_path)
    is_synchronized = validator.validate()

    # Exit with appropriate code
    sys.exit(0 if is_synchronized else 1)


if __name__ == "__main__":
    main()
