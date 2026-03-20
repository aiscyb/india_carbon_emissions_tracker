"""
Complete Pipeline Execution with Detailed Output
India Carbon Emissions Tracker
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def run_command(cmd, description):
    """Run a command and report results"""
    print(f"Running: {description}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"\n✓ SUCCESS: {description}")
            return True
        else:
            print(f"\n✗ FAILED: {description} (Exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"\n✗ ERROR: {description}")
        print(f"Exception: {str(e)}")
        return False

def main():
    """Execute the complete pipeline"""
    
    # Set working directory
    os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")
    
    print_section("INDIA CARBON EMISSIONS TRACKER - COMPLETE PIPELINE EXECUTION")
    
    # Step 1: Environment Info
    print_section("STEP 1: Environment Information")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Current Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 2: Check dependencies
    print_section("STEP 2: Checking Python Dependencies")
    print("Required packages:")
    with open("requirements.txt", "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                print(f"  - {line.strip()}")
    
    # Step 3: Create data directory
    print_section("STEP 3: Creating Data Directory")
    data_dir = Path("data")
    if data_dir.exists():
        print(f"✓ Data directory already exists: {data_dir.absolute()}")
    else:
        data_dir.mkdir(parents=True)
        print(f"✓ Created data directory: {data_dir.absolute()}")
    
    # Step 4: Run data_fetcher.py
    print_section("STEP 4: Running data_fetcher.py")
    print("This will:")
    print("  - Download OWID CO2 dataset")
    print("  - Generate state-level emissions for 15 Indian states")
    print("  - Calculate net-zero gaps")
    print()
    
    success = run_command(
        "python data_fetcher.py",
        "Data Fetcher Module"
    )
    
    if not success:
        print_section("PIPELINE FAILED")
        print("✗ Could not run data_fetcher.py")
        return False
    
    # Step 5: Run ml_model.py
    print_section("STEP 5: Running ml_model.py")
    print("This will:")
    print("  - Train ML models for each state")
    print("  - Generate emissions forecasts through 2035")
    print("  - Classify states into performance tiers")
    print()
    
    success = run_command(
        "python ml_model.py",
        "ML Model Training and Forecasting"
    )
    
    if not success:
        print_section("PIPELINE FAILED")
        print("✗ Could not run ml_model.py")
        return False
    
    # Step 6: List generated files
    print_section("STEP 6: Verifying Generated CSV Files")
    
    csv_files = list(data_dir.glob("*.csv"))
    
    if csv_files:
        print(f"✓ Found {len(csv_files)} CSV files in data/ directory:\n")
        
        total_size = 0
        for csv_file in sorted(csv_files):
            size = csv_file.stat().st_size
            size_mb = size / (1024 * 1024)
            total_size += size
            
            # Count lines in CSV
            try:
                with open(csv_file, 'r') as f:
                    lines = len(f.readlines())
                print(f"  📄 {csv_file.name}")
                print(f"     Size: {size:,} bytes ({size_mb:.2f} MB)")
                print(f"     Lines: {lines}")
                
                # Show header
                with open(csv_file, 'r') as f:
                    header = f.readline().strip()
                    print(f"     Header: {header[:80]}{'...' if len(header) > 80 else ''}")
            except Exception as e:
                print(f"  📄 {csv_file.name} (Error reading: {e})")
            
            print()
        
        print(f"Total Size: {total_size:,} bytes ({total_size / (1024 * 1024):.2f} MB)\n")
    else:
        print("✗ WARNING: No CSV files found in data/ directory")
        return False
    
    # Step 7: Final Summary
    print_section("PIPELINE EXECUTION COMPLETE")
    print("✓ ALL STEPS COMPLETED SUCCESSFULLY!\n")
    
    print("Summary of Generated Files:")
    for csv_file in sorted(csv_files):
        size = csv_file.stat().st_size
        print(f"  ✓ {csv_file.name} ({size:,} bytes)")
    
    print("\n" + "=" * 80)
    print("NEXT STEP: Start Streamlit Dashboard")
    print("=" * 80 + "\n")
    
    print("To start the dashboard, run:")
    print("  streamlit run app.py --server.headless false")
    print("\nThe dashboard will be available at:")
    print("  http://localhost:8501")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
