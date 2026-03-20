#!/usr/bin/env python3
"""
India Carbon Emissions Tracker - Setup Runner
Executes all setup steps in sequence
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report output"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            print(f"\n❌ Command failed with exit code {result.returncode}")
            return False
        print(f"\n✅ Step completed successfully")
        return True
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out after 300 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    # Set working directory
    project_dir = r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit"
    os.chdir(project_dir)
    
    print(f"Working directory: {os.getcwd()}")
    
    # Step 1: Create data directory
    print(f"\n{'='*70}")
    print("STEP 1: Create data directory")
    print(f"{'='*70}")
    data_dir = Path(project_dir) / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Data directory created/verified at: {data_dir}")
    
    # Step 2: Run data_fetcher.py
    if not run_command(f"python data_fetcher.py", "Run data_fetcher.py"):
        print("\n⚠️ data_fetcher.py encountered issues. Continuing to ml_model.py...")
    
    # Step 3: Run ml_model.py
    if not run_command(f"python ml_model.py", "Run ml_model.py"):
        print("\n⚠️ ml_model.py encountered issues.")
    
    # Step 4: List data directory
    print(f"\n{'='*70}")
    print("STEP 4: Verify data directory contents")
    print(f"{'='*70}")
    try:
        files = sorted(data_dir.iterdir())
        if files:
            print(f"\nFiles created in {data_dir}:")
            for f in files:
                size = f.stat().st_size if f.is_file() else 0
                size_mb = size / (1024*1024)
                print(f"  - {f.name:<30} ({size_mb:.2f} MB)")
        else:
            print(f"⚠️ No files found in {data_dir}")
    except Exception as e:
        print(f"❌ Error listing directory: {e}")
    
    print(f"\n{'='*70}")
    print("SETUP COMPLETE")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
