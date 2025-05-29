#!/usr/bin/env python3
"""
Version Manager for Agent3D Templates and Framework Files
Automatically updates versions when writing templates or framework YAML files
"""

import re
import yaml
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime


class VersionManager:
    """Manages automatic version updates for templates and framework files"""

    def __init__(self):
        self.template_patterns = [
            "templates/*.template.yml",
            "templates/*.template.md",
            "templates/index.yml"
        ]

        self.framework_patterns = [
            "procedures/*.yml",
            "procedures.yml/*.yml",  # Legacy support
            "passes/*.yml",
            "passes.yml/*.yml",      # Legacy support
            "rules/*.yml",
            "rules.yml/*.yml",       # Legacy support
            "guidelines/*.yml",
            "workflows/*.yml",
            ".agent3d-config.yml",
            "AGENT-GUIDELINES.yml"
        ]

        # Standardized version format
        self.version_format = "X.Y.Z"  # Major.Minor.Patch

    def should_update_version(self, file_path: Path) -> bool:
        """Check if file requires version updates"""
        file_str = str(file_path)

        # Check template patterns
        for pattern in self.template_patterns:
            if file_path.match(pattern.replace("*", "**")):
                return True

        # Check framework patterns
        for pattern in self.framework_patterns:
            if file_path.match(pattern.replace("*", "**")):
                return True

        return False

    def parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string into components"""
        if not version_str:
            return (1, 0, 0)

        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str.strip())
        if not match:
            return (1, 0, 0)

        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))

    def increment_version(self, current_version: str, change_type: str = "patch") -> str:
        """Increment version based on change type"""
        major, minor, patch = self.parse_version(current_version)

        if change_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif change_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        return f"{major}.{minor}.{patch}"

    def get_current_version_from_yaml(self, content: str) -> Optional[str]:
        """Extract version from YAML content"""
        try:
            data = yaml.safe_load(content)
            if not data:
                return None

            # Try different version field locations
            version_fields = [
                "version",
                "metadata.version",
                "template_version"
            ]

            for field in version_fields:
                if "." in field:
                    # Nested field
                    parts = field.split(".")
                    value = data
                    for part in parts:
                        if isinstance(value, dict) and part in value:
                            value = value[part]
                        else:
                            value = None
                            break
                    if value:
                        return str(value)
                else:
                    # Top-level field
                    if field in data:
                        return str(data[field])

            return None

        except yaml.YAMLError:
            return None

    def get_current_version_from_markdown(self, content: str) -> Optional[str]:
        """Extract version from Markdown content"""
        # Try version comment pattern
        comment_match = re.search(r'<!-- Template Version: (\d+\.\d+\.\d+) -->', content)
        if comment_match:
            return comment_match.group(1)

        # Try YAML frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            try:
                yaml_content = frontmatter_match.group(1)
                data = yaml.safe_load(yaml_content)
                if data and "version" in data:
                    return str(data["version"])
            except yaml.YAMLError:
                pass

        return None

    def update_yaml_version(self, content: str, new_version: str) -> str:
        """Update version in YAML content"""
        try:
            data = yaml.safe_load(content) or {}

            # Determine where to put version
            if "metadata" in data:
                if not isinstance(data["metadata"], dict):
                    data["metadata"] = {}
                data["metadata"]["version"] = new_version
                data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            else:
                data["version"] = new_version
                data["last_updated"] = datetime.now().strftime("%Y-%m-%d")

            # Convert back to YAML
            return yaml.dump(data, default_flow_style=False, sort_keys=False)

        except yaml.YAMLError:
            # If parsing fails, try simple replacement
            version_patterns = [
                (r'version:\s*["\']?[\d.]+["\']?', f'version: {new_version}'),
                (r'version:\s*["\']?[\d.]+["\']?', f'version: "{new_version}"')
            ]

            updated_content = content
            for pattern, replacement in version_patterns:
                updated_content = re.sub(pattern, replacement, updated_content, count=1)
                if updated_content != content:
                    break

            return updated_content

    def update_markdown_version(self, content: str, new_version: str) -> str:
        """Update version in Markdown content"""
        # Update version comment
        comment_pattern = r'<!-- Template Version: \d+\.\d+\.\d+ -->'
        new_comment = f'<!-- Template Version: {new_version} -->'

        if re.search(comment_pattern, content):
            content = re.sub(comment_pattern, new_comment, content)
        else:
            # Add version comment after first heading
            heading_match = re.search(r'^(# .+)$', content, re.MULTILINE)
            if heading_match:
                insert_pos = heading_match.end()
                content = content[:insert_pos] + f'\n\n{new_comment}' + content[insert_pos:]

        # Update YAML frontmatter if present
        frontmatter_match = re.search(r'^(---\n)(.*?)(\n---)', content, re.DOTALL)
        if frontmatter_match:
            try:
                yaml_content = frontmatter_match.group(2)
                data = yaml.safe_load(yaml_content) or {}
                data["version"] = new_version
                data["last_updated"] = datetime.now().strftime("%Y-%m-%d")

                new_yaml = yaml.dump(data, default_flow_style=False, sort_keys=False)
                content = content.replace(
                    frontmatter_match.group(0),
                    f"---\n{new_yaml}---"
                )
            except yaml.YAMLError:
                pass

        return content

    def update_file_version(self, file_path: Path, change_type: str = "patch") -> bool:
        """Update version in a file"""
        if not self.should_update_version(file_path):
            return False

        if not file_path.exists():
            return False

        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Get current version
            if file_path.suffix.lower() in ['.yml', '.yaml']:
                current_version = self.get_current_version_from_yaml(content)
                update_func = self.update_yaml_version
            else:
                current_version = self.get_current_version_from_markdown(content)
                update_func = self.update_markdown_version

            # Calculate new version
            if not current_version:
                current_version = "1.0.0"

            new_version = self.increment_version(current_version, change_type)

            # Update content
            updated_content = update_func(content, new_version)

            # Write back if changed
            if updated_content != original_content:
                file_path.write_text(updated_content, encoding='utf-8')
                print(f"Version updated: {file_path} {current_version} → {new_version} ({change_type})")
                return True

            return False

        except Exception as e:
            print(f"Error updating version for {file_path}: {e}")
            return False


def update_file_version_before_write(file_path: str, change_type: str = "patch") -> bool:
    """Convenience function to update file version before writing"""
    manager = VersionManager()
    return manager.update_file_version(Path(file_path), change_type)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python version_manager.py <file_path> [change_type]")
        print("Change types: patch (default), minor, major")
        sys.exit(1)

    file_path = sys.argv[1]
    change_type = sys.argv[2] if len(sys.argv) > 2 else "patch"

    success = update_file_version_before_write(file_path, change_type)
    if success:
        print(f"Successfully updated version for {file_path}")
    else:
        print(f"No version update needed for {file_path}")
