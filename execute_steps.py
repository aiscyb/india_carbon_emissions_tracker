#!/usr/bin/env python3
"""
Execute all the required steps and show output
"""
import os
import subprocess
import sys

os.chdir(r'c:\Users\KIIT0001\OneDrive\Desktop\tryingit')

print("=" * 80)
print("STEP 1: CURRENT DIRECTORY AND FILES")
print("=" * 80)
print(f"Current Directory: {os.getcwd()}")
print("\nFiles and Directories:")
for item in sorted(os.listdir('.')):
    full_path = os.path.join('.', item)
    if os.path.isdir(full_path):
        print(f"  [DIR]  {item}")
    else:
        print(f"  [FILE] {item}")

print("\n" + "=" * 80)
print("STEP 2: CREATE DATA DIRECTORY")
print("=" * 80)
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")
else:
    print(f"Directory already exists: {data_dir}")

print("\n" + "=" * 80)
print("STEP 3: RUN python data_fetcher.py")
print("=" * 80)
try:
    result = subprocess.run([sys.executable, 'data_fetcher.py'], 
                          capture_output=True, 
                          text=True, 
                          timeout=300)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    print(f"\nReturn code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("ERROR: Command timed out after 300 seconds")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 80)
print("STEP 4: RUN python ml_model.py")
print("=" * 80)
try:
    result = subprocess.run([sys.executable, 'ml_model.py'], 
                          capture_output=True, 
                          text=True, 
                          timeout=300)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    print(f"\nReturn code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("ERROR: Command timed out after 300 seconds")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 80)
print("STEP 5: LIST CONTENTS OF DATA/ DIRECTORY")
print("=" * 80)
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
                print(f"  [FILE] {item} ({file_size} bytes)")
    else:
        print(f"Directory {data_dir}/ is empty")
else:
    print(f"ERROR: Directory {data_dir}/ does not exist")

print("\n" + "=" * 80)
print("ALL STEPS COMPLETED")
print("=" * 80)
