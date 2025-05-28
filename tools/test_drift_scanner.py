#!/usr/bin/env python3
"""Test script for drift scanner."""

import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent / 'tools'
sys.path.insert(0, str(tools_dir))

try:
    print("Testing drift scanner import...")
    import drift_scanner
    print("✅ Import successful")
    
    print("Testing MultiModeDriftAnalyzer...")
    analyzer = drift_scanner.MultiModeDriftAnalyzer()
    print("✅ Analyzer created successfully")
    
    print("Testing tc-mapping mode...")
    report = analyzer.analyze_drift('tc-mapping')
    print(f"✅ Analysis completed. Mode: {report.mode}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
