@echo off
cd /d "c:\Users\KIIT0001\OneDrive\Desktop\tryingit"

echo ============================================
echo Current Directory:
echo ============================================
cd
echo.

echo ============================================
echo Step 1: Creating data directory (if not exists)
echo ============================================
if not exist "data" (
    mkdir data
    echo Data directory created
) else (
    echo Data directory already exists
)
echo.

echo ============================================
echo Step 2: Running python data_fetcher.py
echo ============================================
python data_fetcher.py
if errorlevel 1 (
    echo Error occurred during data_fetcher.py
) else (
    echo data_fetcher.py completed successfully
)
echo.

echo ============================================
echo Step 3: Running python ml_model.py
echo ============================================
python ml_model.py
if errorlevel 1 (
    echo Error occurred during ml_model.py
) else (
    echo ml_model.py completed successfully
)
echo.

echo ============================================
echo Step 4: List contents of data/ directory
echo ============================================
dir data /s
echo.

echo ============================================
echo All commands completed
echo ============================================
