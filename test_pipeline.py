import subprocess
import sys

# Run the test
print("Testing data pipeline...\n")
result = subprocess.run([sys.executable, "run_tests.py"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("\nExit code:", result.returncode)
