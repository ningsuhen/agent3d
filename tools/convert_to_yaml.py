#!/usr/bin/env python3
"""
Convert DDD passes and rules from Markdown to YAML format
Automated conversion tool for better LLM processing
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any

def extract_metadata_from_md(content: str, filename: str) -> Dict[str, Any]:
    """Extract metadata and structure from Markdown content"""
    
    # Extract title (first # heading)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else filename.replace('.md', '').replace('_', ' ').title()
    
    # Extract purpose/description
    purpose_match = re.search(r'\*\*Purpose:\*\* (.+?)(?:\n|$)', content)
    purpose = purpose_match.group(1) if purpose_match else ""
    
    # Extract role information
    role_match = re.search(r'\*\*Role:\*\* (.+?)(?:\n|$)', content)
    role = role_match.group(1) if role_match else ""
    
    # Extract when to use section
    when_match = re.search(r'## When to Use\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    when_to_use = when_match.group(1).strip() if when_match else ""
    
    # Extract process section
    process_match = re.search(r'## Process\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    process = process_match.group(1).strip() if process_match else ""
    
    # Extract expected outcomes
    outcomes_match = re.search(r'## Expected Outcomes\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    outcomes = outcomes_match.group(1).strip() if outcomes_match else ""
    
    # Extract quality gates
    gates_match = re.search(r'## Quality Gates\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    quality_gates = gates_match.group(1).strip() if gates_match else ""
    
    return {
        'title': title,
        'purpose': purpose,
        'role': role,
        'when_to_use': when_to_use,
        'process': process,
        'expected_outcomes': outcomes,
        'quality_gates': quality_gates
    }

def convert_pass_to_yaml(md_file: Path) -> Dict[str, Any]:
    """Convert a pass Markdown file to YAML structure"""
    
    content = md_file.read_text()
    metadata = extract_metadata_from_md(content, md_file.name)
    
    # Extract pass number from filename
    pass_number = None
    if md_file.name[0].isdigit():
        pass_number = int(md_file.name.split('_')[0])
    
    yaml_structure = {
        'metadata': {
            'name': metadata['title'],
            'number': pass_number,
            'purpose': metadata['purpose'],
            'role': metadata['role'],
            'description': f"Converted from {md_file.name}"
        },
        'when_to_use': {
            'conditions': parse_bullet_points(metadata['when_to_use']),
            'prerequisites': []
        },
        'process': {
            'workflow_pattern': "SCAN → DRAFT → ASK → SYNC → CONFIRM",
            'phases': parse_process_phases(metadata['process'])
        },
        'expected_outcomes': parse_bullet_points(metadata['expected_outcomes']),
        'quality_gates': parse_quality_gates(metadata['quality_gates'])
    }
    
    return yaml_structure

def convert_rule_to_yaml(md_file: Path) -> Dict[str, Any]:
    """Convert a rule Markdown file to YAML structure"""
    
    content = md_file.read_text()
    language = md_file.stem
    
    yaml_structure = {
        'metadata': {
            'language': language,
            'description': f"{language.title()} development rules for DDD framework",
            'last_updated': "2025-01-27"
        },
        'standards': extract_standards_from_content(content),
        'code_review': extract_code_review_standards(content),
        'quality_gates': extract_quality_gates_from_content(content)
    }
    
    return yaml_structure

def parse_bullet_points(text: str) -> List[str]:
    """Parse bullet points from text"""
    if not text:
        return []
    
    bullets = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            bullets.append(line[2:].strip())
    
    return bullets

def parse_process_phases(text: str) -> Dict[str, Any]:
    """Parse process phases from text"""
    phases = {}
    
    # Look for numbered steps
    steps = re.findall(r'(\d+)\.\s*\*\*([^*]+)\*\*[:\s]*([^0-9]+?)(?=\d+\.|$)', text, re.DOTALL)
    
    for step_num, phase_name, description in steps:
        phase_key = phase_name.lower().replace(' ', '_')
        phases[phase_key] = {
            'description': description.strip(),
            'actions': []
        }
    
    return phases

def parse_quality_gates(text: str) -> List[Dict[str, Any]]:
    """Parse quality gates from text"""
    gates = []
    
    # Look for checkbox items
    checkboxes = re.findall(r'- \[ \] (.+)', text)
    
    for checkbox in checkboxes:
        gates.append({
            'name': checkbox.strip(),
            'validation': f"check_{checkbox.lower().replace(' ', '_')}"
        })
    
    return gates

def extract_standards_from_content(content: str) -> Dict[str, Any]:
    """Extract coding standards from content"""
    standards = {}
    
    # Extract major sections
    sections = re.findall(r'## ([^#\n]+)\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    
    for section_title, section_content in sections:
        section_key = section_title.lower().replace(' ', '_').replace('&', 'and')
        standards[section_key] = {
            'description': section_title,
            'content': section_content.strip()
        }
    
    return standards

def extract_code_review_standards(content: str) -> Dict[str, Any]:
    """Extract code review standards"""
    review_match = re.search(r'## Code Review Standards\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    
    if not review_match:
        return {}
    
    return {
        'role': 'Senior Engineer',
        'standards': review_match.group(1).strip()
    }

def extract_quality_gates_from_content(content: str) -> List[str]:
    """Extract quality gates from content"""
    gates_match = re.search(r'### Quality Gates\n(.*?)(?=\n## |\n# |$)', content, re.DOTALL)
    
    if not gates_match:
        return []
    
    return parse_bullet_points(gates_match.group(1))

def main():
    """Main conversion function"""
    
    # Convert passes
    passes_dir = Path('passes/simplified')
    passes_yml_dir = Path('passes.yml')
    passes_yml_dir.mkdir(exist_ok=True)
    
    print("Converting passes to YAML...")
    for md_file in passes_dir.glob('*.md'):
        if md_file.name == '1_foundation_pass.md':
            continue  # Already converted manually
            
        print(f"Converting {md_file.name}...")
        yaml_structure = convert_pass_to_yaml(md_file)
        
        yml_file = passes_yml_dir / md_file.name.replace('.md', '.yml')
        with yml_file.open('w') as f:
            yaml.dump(yaml_structure, f, default_flow_style=False, sort_keys=False)
    
    # Convert rules
    rules_dir = Path('rules')
    rules_yml_dir = Path('rules.yml')
    rules_yml_dir.mkdir(exist_ok=True)
    
    print("Converting rules to YAML...")
    for md_file in rules_dir.glob('*.md'):
        if md_file.name == 'python.md':
            continue  # Already converted manually
            
        print(f"Converting {md_file.name}...")
        yaml_structure = convert_rule_to_yaml(md_file)
        
        yml_file = rules_yml_dir / md_file.name.replace('.md', '.yml')
        with yml_file.open('w') as f:
            yaml.dump(yaml_structure, f, default_flow_style=False, sort_keys=False)
    
    print("Conversion complete!")
    print(f"Passes converted to: {passes_yml_dir}")
    print(f"Rules converted to: {rules_yml_dir}")

if __name__ == '__main__':
    main()
