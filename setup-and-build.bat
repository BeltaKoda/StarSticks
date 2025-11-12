@echo off
REM StarSticks - Setup and Build Script
REM This script clones/updates the repo and builds the .exe

echo ============================================================
echo StarSticks - Setup and Build Script
echo ============================================================
echo.

REM Set the target directory
set TARGET_DIR=C:\StarSticks
set REPO_URL=https://github.com/joeydee1986/StarSticks.git

REM Check if directory exists
if exist "%TARGET_DIR%" (
    echo Directory exists. Checking for git repository...

    if exist "%TARGET_DIR%\.git" (
        echo Found git repository. Pulling latest changes...
        cd /d "%TARGET_DIR%"
        git pull
        if errorlevel 1 (
            echo ERROR: Failed to pull latest changes!
            pause
            exit /b 1
        )
        echo Successfully updated repository!
    ) else (
        echo Directory exists but is not a git repository.
        echo Please delete C:\StarSticks manually and run this script again.
        pause
        exit /b 1
    )
) else (
    echo Cloning repository to %TARGET_DIR%...
    git clone %REPO_URL% "%TARGET_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to clone repository!
        echo Make sure git is installed and you have internet connection.
        pause
        exit /b 1
    )
    echo Successfully cloned repository!
    cd /d "%TARGET_DIR%"
)

echo.
echo ============================================================
echo Installing/Updating Dependencies
echo ============================================================
echo.

REM Create virtual environment if it doesn't exist
if not exist "%TARGET_DIR%\venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Building StarSticks.exe
echo ============================================================
echo.

python build.py
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS!
echo ============================================================
echo.
echo StarSticks.exe has been built successfully!
echo Location: %TARGET_DIR%\dist\StarSticks.exe
echo.
echo You can now run StarSticks.exe
echo.
pause
