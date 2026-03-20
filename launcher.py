import os
import sys

# Execute the setup
os.chdir(r"c:\Users\KIIT0001\OneDrive\Desktop\tryingit")
exit_code = os.system('python execute_now.py')
sys.exit(exit_code >> 8)
