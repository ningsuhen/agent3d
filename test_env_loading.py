#!/usr/bin/env python3
"""
Simple test to verify environment loading and Gemini API key availability.
"""

import os
import subprocess

def load_environment_keys():
    """Load environment keys from ~/.env.keys.sh if available."""
    env_keys_path = os.path.expanduser("~/.env.keys.sh")
    if os.path.exists(env_keys_path):
        try:
            # Read and execute the shell script to extract environment variables
            result = subprocess.run(
                f"source {env_keys_path} && env",
                shell=True,
                capture_output=True,
                text=True,
                executable="/bin/bash"
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if '=' in line and not line.startswith('_'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
                print(f"✅ Loaded environment keys from {env_keys_path}")
                return True
            else:
                print(f"⚠️ Failed to load environment keys: {result.stderr}")
                return False
        except Exception as e:
            print(f"⚠️ Error loading environment keys: {e}")
            return False
    else:
        print(f"❌ Environment keys file not found: {env_keys_path}")
        return False

def main():
    print("🔍 Testing Environment Key Loading")
    print("=" * 40)
    
    # Check initial state
    print(f"1. Initial state:")
    print(f"   GOOGLE_API_KEY present: {'GOOGLE_API_KEY' in os.environ}")
    
    # Load environment keys
    print(f"\n2. Loading environment keys...")
    success = load_environment_keys()
    
    # Check after loading
    print(f"\n3. After loading:")
    print(f"   GOOGLE_API_KEY present: {'GOOGLE_API_KEY' in os.environ}")
    if 'GOOGLE_API_KEY' in os.environ:
        print(f"   Key length: {len(os.environ['GOOGLE_API_KEY'])}")
        print(f"   Key starts with: {os.environ['GOOGLE_API_KEY'][:10]}...")
    
    # Test Google AI import
    print(f"\n4. Testing Google AI import...")
    try:
        import google.generativeai as genai
        print("   ✅ Google AI package imported successfully")
        
        if 'GOOGLE_API_KEY' in os.environ:
            try:
                genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
                print("   ✅ Google AI configured successfully")
            except Exception as e:
                print(f"   ❌ Failed to configure Google AI: {e}")
        else:
            print("   ⚠️ No API key available for configuration")
            
    except ImportError as e:
        print(f"   ❌ Failed to import Google AI: {e}")
    
    print(f"\n5. Summary:")
    if success and 'GOOGLE_API_KEY' in os.environ:
        print("   🎉 Environment loading successful!")
        print("   🚀 Ready to run DDD pass with Gemini")
    else:
        print("   ❌ Environment loading failed")
        print("   💡 Check ~/.env.keys.sh file")

if __name__ == "__main__":
    main()
