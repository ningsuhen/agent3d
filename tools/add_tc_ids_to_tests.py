#!/usr/bin/env python3
"""
Script to add TC ID comments to test functions for drift scanner detection.
"""

import re
from pathlib import Path

def add_tc_ids_to_test_file(file_path):
    """Add TC ID comments to test functions in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match test function definitions with TC IDs in docstrings
    pattern = r'def (test_tc_[^(]+)\([^)]*\):\s*\n\s*"""([^"]+)"""'
    
    def replace_func(match):
        func_name = match.group(1)
        docstring = match.group(2)
        
        # Extract TC ID from function name or docstring
        tc_id_match = re.search(r'(TC-[A-Z]+-\d+[a-z]?)', func_name.upper())
        if not tc_id_match:
            tc_id_match = re.search(r'(TC-[A-Z]+-\d+[a-z]?)', docstring)
        
        if tc_id_match:
            tc_id = tc_id_match.group(1)
            # Check if TC ID comment already exists
            if f'# {tc_id}' not in match.group(0):
                return f'def {func_name}({match.group(0).split("(", 1)[1].split(")", 1)[0]}):\n        """{docstring}"""\n        # {tc_id}'
        
        return match.group(0)
    
    # Apply replacements
    updated_content = re.sub(pattern, replace_func, content, flags=re.MULTILINE | re.DOTALL)
    
    # Write back if changed
    if updated_content != content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
        return True
    else:
        print(f"No changes needed for {file_path}")
        return False

def main():
    """Main function to process all test files."""
    test_dir = Path('tests')
    test_files = list(test_dir.glob('test_*.py'))
    
    updated_files = []
    for test_file in test_files:
        if add_tc_ids_to_test_file(test_file):
            updated_files.append(test_file)
    
    print(f"\nProcessed {len(test_files)} test files")
    print(f"Updated {len(updated_files)} files")
    
    if updated_files:
        print("\nUpdated files:")
        for file_path in updated_files:
            print(f"  - {file_path}")

if __name__ == '__main__':
    main()
