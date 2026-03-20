@echo off
echo ========================================================================
echo   PUSH TO GITHUB - AUTOMATED SETUP
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    echo After installation, run this script again.
    echo.
    start https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is installed
git --version
echo.

REM Check if already a git repository
if exist ".git" (
    echo [INFO] Git repository already initialized
    echo.
) else (
    echo Initializing Git repository...
    git init
    echo [OK] Git repository initialized
    echo.
)

REM Show current status
echo Current status:
git status
echo.

echo ========================================================================
echo   READY TO COMMIT
echo ========================================================================
echo.
echo Your project is ready to be pushed to GitHub!
echo.
echo NEXT STEPS:
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Repository name: india-carbon-emissions-tracker
echo.
echo 3. Description: AI-powered carbon emissions tracker for MoSPI
echo.
echo 4. Choose Public or Private
echo.
echo 5. DO NOT initialize with README (we already have one)
echo.
echo 6. After creating, come back here and press any key...
echo.
pause

echo.
echo ========================================================================
echo   ADDING FILES
echo ========================================================================
echo.

echo Adding all files to git...
git add .
echo [OK] Files added
echo.

echo Files to be committed:
git status --short
echo.

set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message=Initial commit: India Carbon Emissions Tracker for MoSPI portfolio

echo.
echo Creating commit with message: "%commit_message%"
git commit -m "%commit_message%"
echo [OK] Commit created
echo.

echo ========================================================================
echo   CONNECT TO GITHUB
echo ========================================================================
echo.
echo Now we need your GitHub repository URL.
echo.
echo It should look like:
echo https://github.com/YOUR-USERNAME/india-carbon-emissions-tracker.git
echo.
set /p repo_url="Paste your GitHub repository URL here: "

if "%repo_url%"=="" (
    echo [ERROR] No URL provided!
    echo.
    echo Please run this script again and provide the repository URL.
    pause
    exit /b 1
)

echo.
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin "%repo_url%"
echo [OK] Remote repository added
echo.

echo Verifying remote...
git remote -v
echo.

echo ========================================================================
echo   PUSHING TO GITHUB
echo ========================================================================
echo.
echo Pushing to main branch...
echo.
echo You may be asked for:
echo - Username: Your GitHub username
echo - Password: Use a Personal Access Token (not your actual password)
echo.
echo How to get a token: https://github.com/settings/tokens
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo - Wrong credentials
    echo - Repository doesn't exist
    echo - Permission denied
    echo.
    echo See GITHUB_PUSH_GUIDE.md for troubleshooting.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   SUCCESS!
echo ========================================================================
echo.
echo Your project has been pushed to GitHub! 🎉
echo.
echo View it at: %repo_url:.git=%
echo.
echo NEXT STEPS (Optional):
echo.
echo 1. Add repository topics (tags) on GitHub
echo 2. Star your own repo
echo 3. Deploy to Streamlit Cloud for a live demo
echo 4. Share the link on your resume/LinkedIn
echo.
echo See GITHUB_PUSH_GUIDE.md for deployment instructions.
echo.
pause
