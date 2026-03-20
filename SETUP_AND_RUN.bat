@echo off
SETLOCAL EnableDelayedExpansion

echo ========================================================================
echo   INDIA CARBON EMISSIONS TRACKER - AUTOMATED SETUP
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Step 1: Checking Python version...
python --version
echo.

REM Create data directory
if not exist "data" (
    mkdir data
    echo [OK] Created data directory
) else (
    echo [OK] Data directory already exists
)
echo.

echo ========================================================================
echo   STEP 2: Installing Required Packages
echo ========================================================================
echo.

echo Installing dependencies from requirements.txt...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install
    echo Attempting individual installs...
    pip install pandas numpy requests scikit-learn anthropic streamlit plotly streamlit-folium folium
)
echo [OK] Dependencies installed
echo.

echo ========================================================================
echo   STEP 3: Running Data Fetcher (data_fetcher.py)
echo ========================================================================
echo.

python data_fetcher.py
if errorlevel 1 (
    echo [ERROR] Data fetcher failed!
    pause
    exit /b 1
)
echo.
echo [OK] Data fetcher completed successfully
echo.

echo ========================================================================
echo   STEP 4: Running ML Model (ml_model.py)
echo ========================================================================
echo.

python ml_model.py
if errorlevel 1 (
    echo [ERROR] ML model failed!
    pause
    exit /b 1
)
echo.
echo [OK] ML model completed successfully
echo.

echo ========================================================================
echo   STEP 5: Verifying Generated Files
echo ========================================================================
echo.

echo Contents of data directory:
dir data /b
echo.

if exist "data\state_emissions.csv" (
    echo [OK] state_emissions.csv created
) else (
    echo [ERROR] state_emissions.csv NOT FOUND
)

if exist "data\emissions_forecast.csv" (
    echo [OK] emissions_forecast.csv created
) else (
    echo [ERROR] emissions_forecast.csv NOT FOUND
)

if exist "data\state_tiers.csv" (
    echo [OK] state_tiers.csv created
) else (
    echo [ERROR] state_tiers.csv NOT FOUND
)

if exist "data\net_zero_gaps.csv" (
    echo [OK] net_zero_gaps.csv created
) else (
    echo [ERROR] net_zero_gaps.csv NOT FOUND
)

echo.
echo ========================================================================
echo   SETUP COMPLETE!
echo ========================================================================
echo.
echo Your India Carbon Emissions Tracker is ready!
echo.
echo To start the dashboard, run:
echo   streamlit run app.py
echo.
echo The dashboard will open in your browser at http://localhost:8501
echo.
echo Press any key to start the dashboard now, or Ctrl+C to exit...
pause >nul

echo.
echo Starting Streamlit dashboard...
echo.

streamlit run app.py

ENDLOCAL
