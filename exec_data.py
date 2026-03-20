import sys
import os

# Ensure we're in the right directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("=" * 70)
print("  EXECUTING: data_fetcher.py")
print("=" * 70)
print()

# Execute data_fetcher.py by importing it
try:
    exec(open("data_fetcher.py").read())
except Exception as e:
    print(f"Error running data_fetcher.py: {e}")
    sys.exit(1)
