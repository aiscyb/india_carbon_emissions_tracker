@echo off
REM India Carbon Emissions Tracker - Full Setup Runner
setlocal enabledelayedexpansion
cd /d "c:\Users\KIIT0001\OneDrive\Desktop\tryingit"

echo.
echo ============================================================
echo India Carbon Emissions Tracker - Full Setup
echo ============================================================
echo.
echo Current Directory: %cd%
echo.

REM Step 1: Create data directory
echo ============================================================
echo STEP 1: Create data directory
echo ============================================================
if not exist "data" (
    mkdir data
    echo Data directory created
) else (
    echo Data directory already exists
)
echo.

REM Step 2: Run data_fetcher.py
echo ============================================================
echo STEP 2: Run data_fetcher.py - Download emissions data
echo ============================================================
python data_fetcher.py
if errorlevel 1 (
    echo Warning: data_fetcher.py encountered issues, but continuing...
) else (
    echo data_fetcher.py completed successfully
)
echo.

REM Step 3: Run ml_model.py
echo ============================================================
echo STEP 3: Run ml_model.py - Train ML models
echo ============================================================
python ml_model.py
if errorlevel 1 (
    echo Warning: ml_model.py encountered issues
) else (
    echo ml_model.py completed successfully
)
echo.

REM Step 4: List data directory
echo ============================================================
echo STEP 4: Data directory contents
echo ============================================================
if exist "data" (
    echo Files in data directory:
    dir /b data
    echo.
    echo Detailed listing:
    dir data
) else (
    echo Data directory does not exist
)
echo.

REM Step 5: Show setup complete
echo ============================================================
echo SETUP COMPLETE - Ready to start Streamlit app
echo ============================================================
echo.
echo To start the Streamlit dashboard, run:
echo   streamlit run app.py
echo.
pause
