import os
import sys
import subprocess

# Ensure we're in the right directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("=" * 70)
print("Step 1-2: Creating data directory")
print("=" * 70)
if not os.path.exists("data"):
    os.makedirs("data")
    print("✓ Created data/ directory")
else:
    print("✓ data/ directory already exists")
print()

print("=" * 70)
print("Step 3: Running python data_fetcher.py")
print("=" * 70)
print()
result1 = subprocess.run([sys.executable, "data_fetcher.py"])
print()

print("=" * 70)
print("Step 4: Running python ml_model.py")
print("=" * 70)
print()
result2 = subprocess.run([sys.executable, "ml_model.py"])
print()

print("=" * 70)
print("Step 5: Listing contents of data/ directory")
print("=" * 70)
print()
if os.path.exists("data"):
    files = os.listdir("data")
    if files:
        for f in files:
            filepath = os.path.join("data", f)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                print(f"  {f} ({size:,} bytes)")
    else:
        print("  (empty directory)")
else:
    print("  data/ directory does not exist")
