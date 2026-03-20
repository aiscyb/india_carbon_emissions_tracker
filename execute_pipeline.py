#!/usr/bin/env python
"""Execute the data and ML pipeline commands."""

import os
import subprocess
import sys

# Navigate to the working directory
os.chdir(r'c:\Users\KIIT0001\OneDrive\Desktop\tryingit')

print("=" * 50)
print("Current Directory:")
print("=" * 50)
print(os.getcwd())
print()

print("=" * 50)
print("Step 1: Creating data directory (if not exists)")
print("=" * 50)
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Data directory created at: {os.path.abspath(data_dir)}")
else:
    print(f"Data directory already exists at: {os.path.abspath(data_dir)}")
print()

print("=" * 50)
print("Step 2: Running python data_fetcher.py")
print("=" * 50)
try:
    result = subprocess.run([sys.executable, 'data_fetcher.py'], 
                          capture_output=False, text=True, timeout=120)
    print(f"data_fetcher.py exited with code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("ERROR: data_fetcher.py timed out after 120 seconds")
except Exception as e:
    print(f"ERROR: {e}")
print()

print("=" * 50)
print("Step 3: Running python ml_model.py")
print("=" * 50)
try:
    result = subprocess.run([sys.executable, 'ml_model.py'], 
                          capture_output=False, text=True, timeout=120)
    print(f"ml_model.py exited with code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("ERROR: ml_model.py timed out after 120 seconds")
except Exception as e:
    print(f"ERROR: {e}")
print()

print("=" * 50)
print("Step 4: List contents of data/ directory")
print("=" * 50)
try:
    for root, dirs, files in os.walk(data_dir):
        level = root.replace(data_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            print(f'{sub_indent}{file} ({size} bytes)')
except Exception as e:
    print(f"ERROR listing directory: {e}")
print()

print("=" * 50)
print("All commands completed")
print("=" * 50)
