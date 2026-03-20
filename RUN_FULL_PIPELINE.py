#!/usr/bin/env python3
"""
Direct execution of the complete pipeline with all output
"""
import os
import sys

# Set working directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("\n" * 2)
print("=" * 80)
print(" " * 20 + "INDIA CARBON EMISSIONS TRACKER")
print(" " * 15 + "COMPLETE PIPELINE EXECUTION WITH FULL OUTPUT")
print("=" * 80)
print()

# ============================================================================
# STEP 1: Display current environment
# ============================================================================
print("=" * 80)
print("STEP 1: Display Current Environment and Directory Contents")
print("=" * 80)
print(f"Current Working Directory: {os.getcwd()}")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version.split()[0]}")
print()
print("Files in current directory:")
print("-" * 80)

file_list = sorted(os.listdir('.'))
for item in file_list:
    item_path = os.path.join('.', item)
    if os.path.isdir(item_path):
        print(f"  [DIR]  {item}/")
    else:
        size = os.path.getsize(item_path)
        print(f"  [FILE] {item:40s} ({size:>10,} bytes)")

print()

# ============================================================================
# STEP 2: Create data directory if it doesn't exist
# ============================================================================
print("=" * 80)
print("STEP 2: Create data directory (if not exists)")
print("=" * 80)

data_dir = 'data'
if os.path.exists(data_dir):
    print(f"✓ Data directory already exists: {os.path.abspath(data_dir)}")
else:
    os.makedirs(data_dir)
    print(f"✓ Created data directory: {os.path.abspath(data_dir)}")

print()

# ============================================================================
# STEP 3: Run data_fetcher.py
# ============================================================================
print("=" * 80)
print("STEP 3: Running python data_fetcher.py")
print("=" * 80)
print()

try:
    with open("data_fetcher.py", "r") as f:
        data_fetcher_code = f.read()
    
    # Create a new globals dict to isolate execution
    exec_globals = {
        '__name__': '__main__',
        '__file__': 'data_fetcher.py',
        '__builtins__': __builtins__,
    }
    
    exec(data_fetcher_code, exec_globals)
    
    print()
    print("✓ data_fetcher.py completed successfully")
    
except Exception as e:
    print()
    print(f"✗ ERROR in data_fetcher.py:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("Pipeline stopped due to error in data_fetcher.py")
    sys.exit(1)

print()

# ============================================================================
# STEP 4: Run ml_model.py
# ============================================================================
print("=" * 80)
print("STEP 4: Running python ml_model.py")
print("=" * 80)
print()

try:
    with open("ml_model.py", "r") as f:
        ml_model_code = f.read()
    
    # Create a new globals dict to isolate execution
    exec_globals = {
        '__name__': '__main__',
        '__file__': 'ml_model.py',
        '__builtins__': __builtins__,
    }
    
    exec(ml_model_code, exec_globals)
    
    print()
    print("✓ ml_model.py completed successfully")
    
except Exception as e:
    print()
    print(f"✗ ERROR in ml_model.py:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("Pipeline stopped due to error in ml_model.py")
    sys.exit(1)

print()

# ============================================================================
# STEP 5: List contents of data/ directory
# ============================================================================
print("=" * 80)
print("STEP 5: List contents of data/ directory")
print("=" * 80)
print()

try:
    if os.path.exists(data_dir):
        file_list = sorted(os.listdir(data_dir))
        
        if file_list:
            print(f"Files in '{data_dir}/' directory ({len(file_list)} file(s)):\n")
            
            total_size = 0
            for filename in file_list:
                filepath = os.path.join(data_dir, filename)
                
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    total_size += size
                    print(f"  📄 {filename}")
                    print(f"     Size: {size:,} bytes")
                    
                    # Show detailed info for CSV files
                    if filename.endswith('.csv'):
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = [line for line in f]
                                num_lines = len(lines)
                                
                            print(f"     Type: CSV Data File")
                            print(f"     Rows: {num_lines - 1} data rows (+ 1 header)")
                            
                            if num_lines > 0:
                                # Show header
                                header_cols = lines[0].strip().split(',')
                                print(f"     Columns ({len(header_cols)}): {', '.join(header_cols[:5])}", end='')
                                if len(header_cols) > 5:
                                    print(f", ... ({len(header_cols) - 5} more)")
                                else:
                                    print()
                                
                                # Show sample data
                                if num_lines > 1:
                                    print(f"     Sample row: {lines[1].strip()[:100]}...")
                                    
                        except Exception as e:
                            print(f"     Error reading file: {e}")
                    print()
                    
                elif os.path.isdir(filepath):
                    print(f"  📁 {filename}/\n")
            
            print(f"Total size of data directory: {total_size:,} bytes\n")
        else:
            print("  (data directory is empty)\n")
    else:
        print(f"✗ Data directory not found at: {os.path.abspath(data_dir)}\n")
        
except Exception as e:
    print(f"✗ ERROR listing directory:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("=" * 80)
print(" " * 25 + "PIPELINE EXECUTION COMPLETE")
print("=" * 80)
print()
print("✅ ALL STEPS COMPLETED SUCCESSFULLY!\n")

print("Generated Files Summary:")
print("-" * 80)

if os.path.exists(data_dir):
    files = sorted(os.listdir(data_dir))
    if files:
        total_bytes = 0
        for filename in files:
            filepath = os.path.join(data_dir, filename)
            size = os.path.getsize(filepath)
            total_bytes += size
            print(f"  • {filename:40s} {size:>15,} bytes")
        
        print("-" * 80)
        print(f"  {'TOTAL':40s} {total_bytes:>15,} bytes")
    else:
        print("  (no files generated)")
else:
    print("  (data directory not found)")

print()
print("=" * 80)
print("End of Pipeline Execution Report")
print("=" * 80)
print()
