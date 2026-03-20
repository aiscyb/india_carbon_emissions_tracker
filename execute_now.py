#!/usr/bin/env python3
"""
Direct execution of the India Carbon Emissions Tracker setup
"""
import os
import sys

# Change to the project directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("=" * 80)
print("INDIA CARBON EMISSIONS TRACKER - EXECUTION")
print("=" * 80)
print()

# Step 1-2: Create data directory
print("STEP 1-2: Creating data directory...")
print("-" * 80)
if not os.path.exists("data"):
    os.makedirs("data")
    print("✓ Created data/ directory")
else:
    print("✓ data/ directory already exists")
print()

# Step 3: Run data_fetcher.py
print("=" * 80)
print("STEP 3: Running data_fetcher.py")
print("=" * 80)
print()
try:
    with open("data_fetcher.py", "r") as f:
        code = f.read()
    exec(code, {"__name__": "__main__"})
    print()
except Exception as e:
    print(f"ERROR in data_fetcher.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Run ml_model.py  
print("=" * 80)
print("STEP 4: Running ml_model.py")
print("=" * 80)
print()
try:
    with open("ml_model.py", "r") as f:
        code = f.read()
    exec(code, {"__name__": "__main__"})
    print()
except Exception as e:
    print(f"ERROR in ml_model.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: List data directory contents
print("=" * 80)
print("STEP 5: Contents of data/ directory")
print("=" * 80)
print()
if os.path.exists("data"):
    files = sorted(os.listdir("data"))
    if files:
        print("Files created:")
        for f in files:
            filepath = os.path.join("data", f)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✓ {f:40s} ({size:>12,} bytes)")
        print()
        print(f"Total files: {len(files)}")
    else:
        print("  (directory is empty)")
else:
    print("  ERROR: data/ directory does not exist!")
    sys.exit(1)

print()
print("=" * 80)
print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
print("=" * 80)
