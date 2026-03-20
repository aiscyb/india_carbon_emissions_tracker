import sys
import os

# Ensure we're in the right directory
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("=" * 70)
print("  EXECUTING: ml_model.py")
print("=" * 70)
print()

# Execute ml_model.py by importing it
try:
    exec(open("ml_model.py").read())
except Exception as e:
    print(f"Error running ml_model.py: {e}")
    sys.exit(1)
