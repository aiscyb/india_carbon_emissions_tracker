@echo off
echo ========================================================================
echo   PYTHON INSTALLATION CHECK
echo ========================================================================
echo.

REM Check for python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python is installed!
    python --version
    echo.
    echo You can now run the project.
    echo Double-click: SETUP_AND_RUN.bat
    echo.
    pause
    exit /b 0
)

REM Check for py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python is installed via py launcher!
    py --version
    echo.
    echo NOTE: Use 'py' instead of 'python' on your system.
    echo.
    echo Creating a special launcher for you...
    (
        echo @echo off
        echo cd /d "%%~dp0"
        echo py EXECUTE_ALL.py
        echo pause
    ) > RUN_WITH_PY.bat
    echo.
    echo [CREATED] RUN_WITH_PY.bat
    echo.
    echo Now double-click: RUN_WITH_PY.bat to run the project
    echo.
    pause
    exit /b 0
)

REM Python not found
echo [ERROR] Python is NOT installed on your system!
echo.
echo ========================================================================
echo   PLEASE INSTALL PYTHON
echo ========================================================================
echo.
echo 1. Go to: https://www.python.org/downloads/
echo.
echo 2. Click the big yellow "Download Python" button
echo.
echo 3. Run the installer
echo.
echo 4. IMPORTANT: Check the box "Add Python to PATH"
echo.
echo 5. Click "Install Now"
echo.
echo 6. After installation, restart this script
echo.
echo ========================================================================
echo.
echo Opening Python download page in your browser...
echo.
start https://www.python.org/downloads/
echo.
pause
