@echo off
cd /d c:\Users\KIIT0001\OneDrive\Desktop\tryingit
echo Starting India Carbon Emissions Tracker...
echo.
python -c "import subprocess, sys, os; os.chdir(r'c:\Users\KIIT0001\OneDrive\Desktop\tryingit'); os.makedirs('data', exist_ok=True); print('Running data_fetcher...'); subprocess.run([sys.executable, 'data_fetcher.py']); print('\nRunning ml_model...'); subprocess.run([sys.executable, 'ml_model.py']); print('\nDone! Starting dashboard...'); subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])"
