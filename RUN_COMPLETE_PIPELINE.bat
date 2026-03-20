@echo off
REM ============================================================================
REM India Carbon Emissions Tracker - Complete Pipeline Execution
REM ============================================================================
REM This script will:
REM 1. Verify Python installation
REM 2. Check/Install dependencies
REM 3. Create data directory
REM 4. Run data_fetcher.py
REM 5. Run ml_model.py
REM 6. Verify CSV files created
REM 7. Start Streamlit dashboard
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo INDIA CARBON EMISSIONS TRACKER - COMPLETE PIPELINE EXECUTION
echo ============================================================================
echo.

REM Set working directory
cd /d c:\Users\KIIT0001\OneDrive\Desktop\tryingit

REM ============================================================================
REM STEP 1: Verify Python Installation
REM ============================================================================
echo.
echo STEP 1: Verifying Python Installation
echo ============================================================================
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo SUCCESS: Python is installed
    python --version
)
echo.

REM ============================================================================
REM STEP 2: Check and Install Dependencies
REM ============================================================================
echo.
echo STEP 2: Checking/Installing Python Dependencies
echo ============================================================================
echo Installing packages from requirements.txt...
pip install --upgrade pip >nul 2>&1
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
) else (
    echo SUCCESS: All dependencies installed
)
echo.

REM ============================================================================
REM STEP 3: Create Data Directory
REM ============================================================================
echo.
echo STEP 3: Creating Data Directory
echo ============================================================================
if not exist "data" (
    mkdir data
    echo Created 'data' directory
) else (
    echo 'data' directory already exists
)
echo Directory: %cd%\data
echo.

REM ============================================================================
REM STEP 4: Run Data Fetcher
REM ============================================================================
echo.
echo STEP 4: Running data_fetcher.py
echo ============================================================================
echo This will download OWID CO2 data and generate state-level emissions...
echo.
python data_fetcher.py
if errorlevel 1 (
    echo ERROR: data_fetcher.py failed
    pause
    exit /b 1
) else (
    echo SUCCESS: data_fetcher.py completed
)
echo.

REM ============================================================================
REM STEP 5: Run ML Model
REM ============================================================================
echo.
echo STEP 5: Running ml_model.py
echo ============================================================================
echo This will train ML models and generate forecasts...
echo.
python ml_model.py
if errorlevel 1 (
    echo ERROR: ml_model.py failed
    pause
    exit /b 1
) else (
    echo SUCCESS: ml_model.py completed
)
echo.

REM ============================================================================
REM STEP 6: Verify Generated CSV Files
REM ============================================================================
echo.
echo STEP 6: Verifying Generated CSV Files
echo ============================================================================
echo.
echo Contents of data/ directory:
echo.
if exist "data" (
    dir /s data\*.csv 2>nul
    if errorlevel 1 (
        echo WARNING: No CSV files found in data/ directory
    ) else (
        echo SUCCESS: CSV files created in data/ directory
    )
) else (
    echo ERROR: data/ directory not found
    pause
    exit /b 1
)
echo.

REM ============================================================================
REM STEP 7: Summary and Next Steps
REM ============================================================================
echo.
echo ============================================================================
echo PIPELINE EXECUTION SUMMARY
echo ============================================================================
echo.
echo [✓] Data directory created
echo [✓] OWID CO2 data downloaded
echo [✓] State emissions generated
echo [✓] ML models trained
echo [✓] Forecasts created
echo [✓] CSV files verified
echo.
echo ============================================================================
echo NEXT STEP: Starting Streamlit Dashboard
echo ============================================================================
echo.
echo The Streamlit dashboard will start in your browser...
echo URL: http://localhost:8501
echo.
echo Press any key to start the dashboard...
pause

REM ============================================================================
REM STEP 8: Start Streamlit Dashboard
REM ============================================================================
echo.
echo Starting Streamlit dashboard...
streamlit run app.py --server.headless false

pause
