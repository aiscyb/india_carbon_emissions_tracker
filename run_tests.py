"""
Test runner script to initialize data and verify all modules
"""

import os
import sys

def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_module(module_name, description):
    """Run a Python module and check for errors."""
    print_banner(f"RUNNING: {description}")
    
    try:
        result = os.system(f"python {module_name}")
        if result != 0:
            print(f"\n⚠️  Warning: {module_name} exited with code {result}")
            return False
        print(f"\n✅ {description} completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error running {module_name}: {e}")
        return False

def check_data_files():
    """Check if data files were generated."""
    print_banner("CHECKING DATA FILES")
    
    required_files = [
        "data/state_emissions.csv",
        "data/emissions_forecast.csv",
        "data/state_tiers.csv",
        "data/net_zero_gaps.csv"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Main test runner."""
    print_banner("INDIA CARBON EMISSIONS TRACKER - INITIALIZATION")
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Create data directory
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created data/ directory")
    
    # Step 1: Run data fetcher
    success1 = run_module("data_fetcher.py", "Data Fetcher Module")
    
    if not success1:
        print("\n❌ Data fetcher failed. Cannot proceed.")
        return
    
    # Step 2: Run ML model
    success2 = run_module("ml_model.py", "ML Forecasting Module")
    
    if not success2:
        print("\n❌ ML model failed. Cannot proceed.")
        return
    
    # Step 3: Check data files
    files_ok = check_data_files()
    
    if not files_ok:
        print("\n❌ Some data files are missing.")
        return
    
    # Final banner
    print_banner("INITIALIZATION COMPLETE ✅")
    
    print("🎉 All modules tested successfully!\n")
    print("Next steps:")
    print("  1. (Optional) Set your ANTHROPIC_API_KEY in .env file")
    print("  2. Run the dashboard: streamlit run app.py")
    print("  3. Open browser to http://localhost:8501\n")

if __name__ == "__main__":
    main()
