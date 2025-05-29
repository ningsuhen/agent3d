#!/usr/bin/env python3
"""
Simple Mermaid syntax test using CLI
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


def test_mermaid_file(mermaid_file):
    """Test if a Mermaid file renders correctly."""
    print(f"🧪 Testing Mermaid file: {mermaid_file}")
    
    if not Path(mermaid_file).exists():
        print(f"❌ File not found: {mermaid_file}")
        return False
    
    # Test with Mermaid CLI
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            result = subprocess.run(
                ['mmdc', '-i', mermaid_file, '-o', tmp.name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Check if output file was created and has content
                if os.path.exists(tmp.name) and os.path.getsize(tmp.name) > 1000:
                    print(f"✅ Mermaid file renders successfully!")
                    print(f"   Output size: {os.path.getsize(tmp.name)} bytes")
                    os.unlink(tmp.name)  # Clean up
                    return True
                else:
                    print(f"❌ Output file is empty or too small")
                    return False
            else:
                print(f"❌ Mermaid CLI failed:")
                print(f"   Error: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print(f"❌ Mermaid CLI timed out")
        return False
    except FileNotFoundError:
        print(f"❌ Mermaid CLI (mmdc) not found. Install with:")
        print(f"   npm install -g @mermaid-js/mermaid-cli")
        return False
    except Exception as e:
        print(f"❌ Error testing Mermaid file: {e}")
        return False


def main():
    """Test the DDD workflow Mermaid file."""
    mermaid_file = "workflows/ddd-workflow.mmd"
    
    if len(sys.argv) > 1:
        mermaid_file = sys.argv[1]
    
    success = test_mermaid_file(mermaid_file)
    
    if success:
        print("\n🎉 Mermaid file is valid and renders correctly!")
        print("\n📋 You can:")
        print("   • View in VS Code with Mermaid Preview extension")
        print("   • Copy content to https://mermaid.live/")
        print("   • Generate images with: mmdc -i file.mmd -o output.png")
    else:
        print("\n💥 Mermaid file has issues that need to be fixed.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
