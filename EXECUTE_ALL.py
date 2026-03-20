import sys
import os

# Ensure we're in the right directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("=" * 70)
print("COMPLETE PIPELINE EXECUTION")
print("=" * 70)
print()

# Step 1: Show current state
print("=" * 70)
print("STEP 1: Display Current Environment and Directory Contents")
print("=" * 70)
print(f"Current Directory: {os.getcwd()}")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print()
print("Files in current directory:")
for item in sorted(os.listdir('.')):
    item_path = os.path.join('.', item)
    if os.path.isdir(item_path):
        print(f"  📁 {item}/")
    else:
        size = os.path.getsize(item_path)
        print(f"  📄 {item} ({size} bytes)")
print()

# Step 2: Create data directory
print("=" * 70)
print("STEP 2: Create data directory (if not exists)")
print("=" * 70)
data_dir = 'data'
if os.path.exists(data_dir):
    print(f"✓ Data directory already exists at: {os.path.abspath(data_dir)}")
else:
    os.makedirs(data_dir)
    print(f"✓ Created data directory at: {os.path.abspath(data_dir)}")
print()

# Step 3: Run data_fetcher.py
print("=" * 70)
print("STEP 3: Running python data_fetcher.py")
print("=" * 70)
print()

try:
    exec(open("data_fetcher.py").read())
    print("\n✓ data_fetcher.py executed successfully")
except Exception as e:
    print(f"\n✗ Error running data_fetcher.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Step 4: Run ml_model.py
print("=" * 70)
print("STEP 4: Running python ml_model.py")
print("=" * 70)
print()

try:
    exec(open("ml_model.py").read())
    print("\n✓ ml_model.py executed successfully")
except Exception as e:
    print(f"\n✗ Error running ml_model.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Step 5: List data directory contents
print("=" * 70)
print("STEP 5: List contents of data/ directory")
print("=" * 70)
print()

try:
    if os.path.exists(data_dir):
        print(f"Contents of '{data_dir}/' directory:\n")
        files = sorted(os.listdir(data_dir))
        
        if files:
            for filename in files:
                filepath = os.path.join(data_dir, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    print(f"  📄 {filename}")
                    print(f"     Size: {size} bytes")
                    
                    # Show preview for CSV files
                    if filename.endswith('.csv'):
                        try:
                            with open(filepath, 'r') as f:
                                lines = f.readlines()
                                print(f"     Lines: {len(lines)}")
                                if lines:
                                    print(f"     Header: {lines[0].strip()}")
                                if len(lines) > 1:
                                    print(f"     First data row: {lines[1].strip()}")
                        except Exception as e:
                            print(f"     Error reading file: {e}")
                    print()
                else:
                    print(f"  📁 {filename}/\n")
        else:
            print("  (empty directory)\n")
    else:
        print(f"✗ Data directory not found: {os.path.abspath(data_dir)}\n")
        
except Exception as e:
    print(f"✗ ERROR listing directory: {e}\n")
    import traceback
    traceback.print_exc()

# Final summary
print("=" * 70)
print("PIPELINE EXECUTION COMPLETE")
print("=" * 70)
print()
print("✓ All steps completed successfully!")
print()
print("Summary of generated files:")
if os.path.exists(data_dir):
    files = sorted(os.listdir(data_dir))
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        size = os.path.getsize(filepath)
        print(f"  - {filename} ({size:,} bytes)")
else:
    print(f"  (data directory not found)")

print()
print("=" * 70)
