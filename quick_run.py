#!/usr/bin/env python3
"""
Minimal runner to execute the full pipeline
This script imports and runs the pipeline directly
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Add the directory to path
    script_dir = r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit"
    sys.path.insert(0, script_dir)
    os.chdir(script_dir)
    
    # Import and execute the full pipeline script
    import RUN_FULL_PIPELINE
