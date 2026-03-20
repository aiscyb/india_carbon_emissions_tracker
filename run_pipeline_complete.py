#!/usr/bin/env python3
"""
Complete Pipeline Execution Script
Runs both data_fetcher.py and ml_model.py with full output
"""

import os
import sys
import subprocess
import time

def run_command(description, command):
    """Run a command and capture all output"""
    print("\n" + "=" * 70)
    print(f"STEP: {description}")
    print("=" * 70)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,  # Show output in real-time
            text=True,
            timeout=180  # 3 minutes timeout
        )
        
        if result.returncode != 0:
            print(f"\n⚠ Command exited with code: {result.returncode}")
            return False
        else:
            print(f"\n✓ Command completed successfully")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"\n✗ ERROR: Command timed out after 180 seconds")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

def main():
    """Main execution"""
    os.chdir(r'c:\Users\KIIT0001\OneDrive\Desktop\tryingit')
    
    print("\n" + "=" * 70)
    print("INDIA CARBON EMISSIONS TRACKER - COMPLETE PIPELINE")
    print("=" * 70)
    
    # Step 0: Show current state
    print("\n" + "=" * 70)
    print("STEP 0: Current Environment")
    print("=" * 70)
    print(f"Current Directory: {os.getcwd()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print("\nDirectory Contents:")
    for item in sorted(os.listdir('.')):
        item_path = os.path.join('.', item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            size = os.path.getsize(item_path)
            print(f"  📄 {item} ({size} bytes)")
    
    # Step 1: Create data directory
    print("\n" + "=" * 70)
    print("STEP 1: Create data directory")
    print("=" * 70)
    data_dir = 'data'
    if os.path.exists(data_dir):
        print(f"✓ Data directory already exists at: {os.path.abspath(data_dir)}")
    else:
        os.makedirs(data_dir)
        print(f"✓ Created data directory at: {os.path.abspath(data_dir)}")
    
    # Step 2: Run data_fetcher.py
    success = run_command(
        "2 - Run data_fetcher.py",
        f"{sys.executable} data_fetcher.py"
    )
    
    if not success:
        print("\n✗ data_fetcher.py failed. Stopping pipeline.")
        sys.exit(1)
    
    # Step 3: Run ml_model.py
    success = run_command(
        "3 - Run ml_model.py",
        f"{sys.executable} ml_model.py"
    )
    
    if not success:
        print("\n✗ ml_model.py failed. Stopping pipeline.")
        sys.exit(1)
    
    # Step 4: List data directory contents
    print("\n" + "=" * 70)
    print("STEP 4: List contents of data/ directory")
    print("=" * 70)
    
    try:
        if os.path.exists(data_dir):
            print(f"\nContents of '{data_dir}/' directory:\n")
            files = sorted(os.listdir(data_dir))
            
            if files:
                for filename in files:
                    filepath = os.path.join(data_dir, filename)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        # Show preview of first few lines
                        print(f"  📄 {filename} ({size} bytes)")
                        if filename.endswith('.csv'):
                            with open(filepath, 'r') as f:
                                lines = f.readlines()
                                print(f"     Lines: {len(lines)}")
                                if lines:
                                    print(f"     Header: {lines[0].strip()}")
                    else:
                        print(f"  📁 {filename}/")
            else:
                print("  (empty directory)")
        else:
            print(f"✗ Data directory not found: {os.path.abspath(data_dir)}")
            
    except Exception as e:
        print(f"✗ ERROR listing directory: {e}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETE")
    print("=" * 70)
    print("\n✓ All steps completed successfully!")
    print("\nGenerated files:")
    if os.path.exists(data_dir):
        for filename in sorted(os.listdir(data_dir)):
            filepath = os.path.join(data_dir, filename)
            size = os.path.getsize(filepath)
            print(f"  - {filename} ({size} bytes)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
