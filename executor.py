import subprocess
import sys

result = subprocess.run(
    [sys.executable, r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit\run_pipeline_complete.py"],
    cwd=r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit"
)
sys.exit(result.returncode)
