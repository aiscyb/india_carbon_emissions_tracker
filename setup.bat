@echo off
echo ================================================
echo India Carbon Emissions Tracker - Quick Setup
echo ================================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Generating data...
python run_tests.py
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To start the dashboard, run:
echo   streamlit run app.py
echo.
pause
