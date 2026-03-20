#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")

print("Executing EXECUTE_ALL.py...")
print("=" * 70)

result = subprocess.run([sys.executable, "EXECUTE_ALL.py"], capture_output=False, text=True)

sys.exit(result.returncode)
