@echo off
setlocal enabledelayedexpansion

echo ========================================
echo STEP 1: Display current directory
echo ========================================
cd /d c:\Users\KIIT0001\OneDrive\Desktop\tryingit
echo Current Directory: %cd%
echo.
echo Files in current directory:
dir
echo.

echo ========================================
echo STEP 2: Create data directory if needed
echo ========================================
if not exist "data" (
    mkdir data
    echo Created 'data' directory
) else (
    echo 'data' directory already exists
)
echo.

echo ========================================
echo STEP 3: Run data_fetcher.py
echo ========================================
python data_fetcher.py
echo.

echo ========================================
echo STEP 4: Run ml_model.py
echo ========================================
python ml_model.py
echo.

echo ========================================
echo STEP 5: List contents of data directory
echo ========================================
echo Contents of data/ directory:
dir data
echo.

echo ========================================
echo ALL STEPS COMPLETED
echo ========================================
