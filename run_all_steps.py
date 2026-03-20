#!/usr/bin/env python3
"""
Execute all the required steps and show output
"""
import os
import sys
import subprocess

def run_command(description, cmd):
    """Run a command and return its output"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print('='*80)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# Change to working directory
os.chdir(r'c:\Users\KIIT0001\OneDrive\Desktop\tryingit')

# Step 1
print("\n" + "="*80)
print("STEP 1: CURRENT DIRECTORY AND FILES")
print("="*80)
print(f"Current Directory: {os.getcwd()}\n")
print("Files and Directories:")
for item in sorted(os.listdir('.')):
    full_path = os.path.join('.', item)
    if os.path.isdir(full_path):
        print(f"  [DIR]  {item}")
    else:
        print(f"  [FILE] {item}")

# Step 2
print("\n" + "="*80)
print("STEP 2: CREATE DATA DIRECTORY")
print("="*80)
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"✓ Created directory: {data_dir}")
else:
    print(f"✓ Directory already exists: {data_dir}")

# Step 3
run_command("STEP 3: RUN python data_fetcher.py", f"{sys.executable} data_fetcher.py")

# Step 4
run_command("STEP 4: RUN python ml_model.py", f"{sys.executable} ml_model.py")

# Step 5
print("\n" + "="*80)
print("STEP 5: LIST CONTENTS OF DATA/ DIRECTORY")
print("="*80)
if os.path.exists(data_dir):
    files = os.listdir(data_dir)
    if files:
        print(f"Files in {data_dir}/:")
        for item in sorted(files):
            full_path = os.path.join(data_dir, item)
            if os.path.isdir(full_path):
                print(f"  [DIR]  {item}")
            else:
                file_size = os.path.getsize(full_path)
                print(f"  [FILE] {item} ({file_size:,} bytes)")
    else:
        print(f"Directory {data_dir}/ is empty")
else:
    print(f"ERROR: Directory {data_dir}/ does not exist")

print("\n" + "="*80)
print("ALL STEPS COMPLETED")
print("="*80)
