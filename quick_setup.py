import subprocess
import sys
import os

print("=" * 70)
print("  INDIA CARBON EMISSIONS TRACKER - SETUP")
print("=" * 70)
print()

# Check Python version
print(f"Python version: {sys.version}")
print()

# Create data directory
if not os.path.exists("data"):
    os.makedirs("data")
    print("✓ Created data/ directory")
else:
    print("✓ data/ directory exists")

print()
print("=" * 70)
print("  STEP 1: Running data_fetcher.py")
print("=" * 70)
print()

result1 = subprocess.run([sys.executable, "data_fetcher.py"], capture_output=False, text=True)

if result1.returncode == 0:
    print("\n✅ Data fetcher completed successfully!")
else:
    print(f"\n❌ Data fetcher failed with code {result1.returncode}")
    sys.exit(1)

print()
print("=" * 70)
print("  STEP 2: Running ml_model.py")
print("=" * 70)
print()

result2 = subprocess.run([sys.executable, "ml_model.py"], capture_output=False, text=True)

if result2.returncode == 0:
    print("\n✅ ML model completed successfully!")
else:
    print(f"\n❌ ML model failed with code {result2.returncode}")
    sys.exit(1)

print()
print("=" * 70)
print("  CHECKING DATA FILES")
print("=" * 70)
print()

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

print()
if all_exist:
    print("=" * 70)
    print("  🎉 SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("Next step: Run the dashboard")
    print("  streamlit run app.py")
    print()
else:
    print("❌ Some files are missing. Check errors above.")
    sys.exit(1)
