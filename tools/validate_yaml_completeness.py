#!/usr/bin/env python3
"""
Validate YAML completeness against Markdown versions
Ensure no critical information is lost in YAML conversion
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Tuple

def analyze_markdown_content(md_file: Path) -> Dict:
    """Analyze Markdown content for key information"""
    content = md_file.read_text()
    
    analysis = {
        'has_purpose': '**Purpose:**' in content or 'Purpose:' in content,
        'has_role': '**Role:**' in content or 'Role:' in content,
        'has_when_to_use': '## When to Use' in content,
        'has_process': '## Process' in content,
        'has_expected_outcomes': '## Expected Outcomes' in content,
        'has_quality_gates': '## Quality Gates' in content or 'Quality Gates' in content,
        'has_critical_notes': '**CRITICAL**' in content or 'CRITICAL:' in content,
        'has_examples': 'Example' in content or 'example' in content,
        'has_commit_message': 'Commit Message' in content or 'commit message' in content,
        'line_count': len(content.split('\n')),
        'word_count': len(content.split()),
        'critical_count': content.count('**CRITICAL**') + content.count('CRITICAL:')
    }
    
    return analysis

def analyze_yaml_content(yml_file: Path) -> Dict:
    """Analyze YAML content for completeness"""
    try:
        with yml_file.open() as f:
            data = yaml.safe_load(f)
        
        analysis = {
            'has_metadata': 'metadata' in data,
            'has_purpose': data.get('metadata', {}).get('purpose') is not None,
            'has_role': data.get('metadata', {}).get('role') is not None,
            'has_when_to_use': 'when_to_use' in data,
            'has_process': 'process' in data,
            'has_expected_outcomes': 'expected_outcomes' in data,
            'has_quality_gates': 'quality_gates' in data,
            'has_critical_flags': check_critical_flags(data),
            'structure_depth': calculate_depth(data),
            'total_keys': count_keys(data)
        }
        
        return analysis
    except Exception as e:
        return {'error': str(e)}

def check_critical_flags(data: Dict) -> bool:
    """Check if YAML has critical flags or requirements"""
    def search_critical(obj):
        if isinstance(obj, dict):
            if obj.get('critical') is True:
                return True
            for value in obj.values():
                if search_critical(value):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if search_critical(item):
                    return True
        elif isinstance(obj, str):
            if 'CRITICAL' in obj.upper():
                return True
        return False
    
    return search_critical(data)

def calculate_depth(obj, current_depth=0):
    """Calculate maximum nesting depth"""
    if isinstance(obj, dict):
        if not obj:
            return current_depth
        return max(calculate_depth(value, current_depth + 1) for value in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return current_depth
        return max(calculate_depth(item, current_depth + 1) for item in obj)
    else:
        return current_depth

def count_keys(obj):
    """Count total number of keys in nested structure"""
    count = 0
    if isinstance(obj, dict):
        count += len(obj)
        for value in obj.values():
            count += count_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            count += count_keys(item)
    return count

def compare_files(md_file: Path, yml_file: Path) -> Dict:
    """Compare Markdown and YAML versions"""
    md_analysis = analyze_markdown_content(md_file)
    yml_analysis = analyze_yaml_content(yml_file)
    
    comparison = {
        'file_pair': f"{md_file.name} vs {yml_file.name}",
        'markdown_analysis': md_analysis,
        'yaml_analysis': yml_analysis,
        'completeness_score': 0,
        'missing_elements': [],
        'recommendations': []
    }
    
    # Check completeness
    essential_elements = ['has_purpose', 'has_when_to_use', 'has_process', 'has_expected_outcomes']
    
    for element in essential_elements:
        if md_analysis.get(element, False) and not yml_analysis.get(element, False):
            comparison['missing_elements'].append(element)
    
    # Calculate completeness score
    total_elements = len(essential_elements)
    missing_count = len(comparison['missing_elements'])
    comparison['completeness_score'] = ((total_elements - missing_count) / total_elements) * 100
    
    # Generate recommendations
    if comparison['completeness_score'] < 80:
        comparison['recommendations'].append("YAML version needs enhancement")
    
    if md_analysis.get('critical_count', 0) > 0 and not yml_analysis.get('has_critical_flags', False):
        comparison['recommendations'].append("Critical information may be missing in YAML")
    
    if yml_analysis.get('structure_depth', 0) < 3:
        comparison['recommendations'].append("YAML structure could be more detailed")
    
    return comparison

def main():
    """Main validation function"""
    
    # File pairs to compare
    file_pairs = [
        # Passes
        ("passes/simplified/0_requirements_pass.md", "passes.yml/0_requirements_pass.yml"),
        ("passes/simplified/1_foundation_pass.md", "passes.yml/1_foundation_pass.yml"),
        ("passes/simplified/2_documentation_pass.md", "passes.yml/2_documentation_pass.yml"),
        ("passes/simplified/3_development_pass.md", "passes.yml/3_development_pass.yml"),
        ("passes/simplified/5_testing_pass.md", "passes.yml/5_testing_pass.yml"),
        ("passes/simplified/6_refactoring_pass.md", "passes.yml/6_refactoring_pass.yml"),
        ("passes/simplified/7_code_review_pass.md", "passes.yml/7_code_review_pass.yml"),
        ("passes/simplified/9_synchronization_pass.md", "passes.yml/9_synchronization_pass.yml"),
        ("passes/simplified/8_prune_pass.md", "passes.yml/8_prune_pass.yml"),
        ("passes/simplified/10_reverse_pass.md", "passes.yml/10_reverse_pass.yml"),
        ("passes/simplified/full_pass.md", "passes.yml/full_pass.yml"),
        
        # Rules
        ("rules/python.md", "rules.yml/python.yml"),
        ("rules/javascript.md", "rules.yml/javascript.yml"),
        ("rules/java.md", "rules.yml/java.yml"),
        ("rules/go.md", "rules.yml/go.yml"),
        ("rules/markdown.md", "rules.yml/markdown.yml"),
    ]
    
    results = []
    safe_to_delete = []
    needs_enhancement = []
    
    print("🔍 Validating YAML completeness against Markdown versions...\n")
    
    for md_path, yml_path in file_pairs:
        md_file = Path(md_path)
        yml_file = Path(yml_path)
        
        if md_file.exists() and yml_file.exists():
            comparison = compare_files(md_file, yml_file)
            results.append(comparison)
            
            print(f"📄 {comparison['file_pair']}")
            print(f"   Completeness: {comparison['completeness_score']:.1f}%")
            
            if comparison['missing_elements']:
                print(f"   Missing: {', '.join(comparison['missing_elements'])}")
                needs_enhancement.append(yml_path)
            
            if comparison['recommendations']:
                print(f"   Recommendations: {'; '.join(comparison['recommendations'])}")
                
            if comparison['completeness_score'] >= 90 and not comparison['recommendations']:
                safe_to_delete.append(md_path)
                print("   ✅ Safe to delete Markdown version")
            else:
                print("   ⚠️  Needs review before deletion")
                
            print()
        else:
            print(f"❌ Missing files: {md_path} or {yml_path}")
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Total comparisons: {len(results)}")
    print(f"   Safe to delete: {len(safe_to_delete)}")
    print(f"   Need enhancement: {len(needs_enhancement)}")
    
    print(f"\n✅ Safe to delete ({len(safe_to_delete)}):")
    for file_path in safe_to_delete:
        print(f"   - {file_path}")
    
    if needs_enhancement:
        print(f"\n⚠️  Need enhancement ({len(needs_enhancement)}):")
        for file_path in needs_enhancement:
            print(f"   - {file_path}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("1. Delete Markdown versions that are safe to delete")
    print("2. Enhance YAML versions that need improvement")
    print("3. Keep Markdown versions for human reference where YAML is insufficient")
    print("4. Focus on manually created YAML files (Foundation Pass, Python rules) as examples")
    
    return safe_to_delete, needs_enhancement

if __name__ == '__main__':
    safe_to_delete, needs_enhancement = main()
