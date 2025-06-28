#!/usr/bin/env python3
"""
Test runner script for the mentor-mentee backend application.
This script sets up the test environment and runs all tests.
"""

import sys
import os
import subprocess

def run_tests():
    """Run all tests"""
    print("🧪 Running backend tests...")
    
    # Add the app directory to Python path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, app_dir)
    
    # Run pytest
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v",
            "--tb=short"
        ], cwd=app_dir)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
