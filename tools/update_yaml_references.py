#!/usr/bin/env python3
"""
Update all references to use YAML versions when available
Systematic update of all DDD framework references
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def update_file_references(file_path: Path, replacements: List[Tuple[str, str]]) -> bool:
    """Update references in a file"""
    try:
        content = file_path.read_text()
        original_content = content

        for old_ref, new_ref in replacements:
            content = content.replace(old_ref, new_ref)

        if content != original_content:
            file_path.write_text(content)
            print(f"Updated: {file_path}")
            return True

        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Main update function"""

    # Define replacement patterns
    replacements = [
        # Pass references
        ("passes/simplified/", "passes.yml/ (LLM) | passes/simplified/ (human)"),
        ("~/.agent3d/passes/simplified/", "~/.agent3d/passes.yml/ (LLM) | ~/.agent3d/passes/simplified/ (human)"),

        # Rule references
        ("rules/", "rules.yml/ (LLM) | rules/ (human)"),
        ("~/.agent3d/rules/", "~/.agent3d/rules.yml/ (LLM) | ~/.agent3d/rules/ (human)"),

        # Template references - now unified in templates/
        ("templates/DDD-STATUS.template.md", "templates/DDD-STATUS.template.yml"),
        ("templates/EXEC-PLAN.template.md", "templates/EXEC-PLAN.template.yml"),
        ("templates/migration.template.yml", "templates/migration.template.yml"),

        # Specific file references
        ("~/.agent3d/rules/python.md", "~/.agent3d/rules.yml/python.yml (LLM) | ~/.agent3d/rules/python.md (human)"),
        ("~/.agent3d/rules/javascript.md", "~/.agent3d/rules.yml/javascript.yml (LLM) | ~/.agent3d/rules/javascript.md (human)"),
        ("~/.agent3d/rules/java.md", "~/.agent3d/rules.yml/java.yml (LLM) | ~/.agent3d/rules/java.md (human)"),
        ("~/.agent3d/rules/go.md", "~/.agent3d/rules.yml/go.yml (LLM) | ~/.agent3d/rules/go.md (human)"),
        ("~/.agent3d/rules/markdown.md", "~/.agent3d/rules.yml/markdown.yml (LLM) | ~/.agent3d/rules/markdown.md (human)"),
    ]

    # Files to update
    files_to_update = [
        "docs/CONFIGURATION-GUIDE.md",
        "docs/QUICK-START.md",
        "docs/ADVANCED-FEATURES.md",
        "docs/GITHUB-CLI-INTEGRATION.md",
        "docs/OTHER-PLATFORMS-INTEGRATION.md",
        "docs/RAPID-PROTOTYPING.md",
        "docs/TC-SUBTEST-GUIDELINES.md",
        "docs/designs/DDD-PASSES.md",
        "docs/designs/LANGUAGE-RULES.md",
        "docs/proposals/PROPOSALS-README.md",
        "docs/runs/README.md",
        "passes/simplified/0_requirements_pass.md",
        "passes/simplified/2_documentation_pass.md",
        "passes/simplified/3_development_pass.md",
        "passes/simplified/4_implementation_pass.md",
        "passes/simplified/5_testing_pass.md",
        "passes/simplified/8_prune_pass.md",
        "passes/simplified/9_synchronization_pass.md",
        "passes/simplified/10_reverse_pass.md",
        "passes/simplified/full_pass.md",
        "templates/BASE.template.md",
        "templates/DETAILED-DESIGN.template.md",
        "templates/HIGH-LEVEL-DESIGN.template.md",
        "templates/PROPOSAL.template.md",
        "templates/README.template.md",
        "templates/REQUIREMENTS.template.md",
        "templates/USER-JOURNEY-MAP.template.md",
        "templates/USER-STORIES.template.md",
        "templates/UX-SPECIFICATIONS.template.md",
        "vscode-ddd-navigator/README.md",
        "workflows/README.md",
    ]

    updated_count = 0

    # Update each file
    for file_path_str in files_to_update:
        file_path = Path(file_path_str)

        if file_path.exists():
            if update_file_references(file_path, replacements):
                updated_count += 1
        else:
            print(f"File not found: {file_path}")

    print(f"\nUpdate complete! Updated {updated_count} files.")

    # Create a summary of changes
    print("\nSummary of YAML reference updates:")
    print("✅ Pass references now point to YAML versions for LLM agents")
    print("✅ Rule references now point to YAML versions for LLM agents")
    print("✅ Template references updated for LLM tracking templates")
    print("✅ Dual format strategy clearly indicated (LLM | human)")

    # Recommendations
    print("\nRecommendations for LLM agents:")
    print("1. Use YAML versions for all automated processing")
    print("2. Cache YAML configurations at session start")
    print("3. Reference Markdown versions only for human communication")
    print("4. Update documentation to reflect dual format strategy")

if __name__ == '__main__':
    main()
