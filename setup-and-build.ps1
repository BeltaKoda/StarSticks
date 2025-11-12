# StarSticks - Setup and Build Script (PowerShell)
# This script clones/updates the repo and builds the .exe

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "StarSticks - Setup and Build Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$TARGET_DIR = "C:\StarSticks"
$REPO_URL = "https://github.com/BeltaKoda/StarSticks.git"

# Check if directory exists
if (Test-Path $TARGET_DIR) {
    Write-Host "Directory exists. Checking for git repository..." -ForegroundColor Yellow

    if (Test-Path "$TARGET_DIR\.git") {
        Write-Host "Found git repository. Pulling latest changes..." -ForegroundColor Green
        Set-Location $TARGET_DIR
        git pull
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to pull latest changes!" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
        Write-Host "Successfully updated repository!" -ForegroundColor Green
    } else {
        Write-Host "Directory exists but is not a git repository." -ForegroundColor Red
        Write-Host "Please delete C:\StarSticks manually and run this script again." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "Cloning repository to $TARGET_DIR..." -ForegroundColor Green
    git clone $REPO_URL $TARGET_DIR
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to clone repository!" -ForegroundColor Red
        Write-Host "Make sure git is installed and you have internet connection." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Successfully cloned repository!" -ForegroundColor Green
    Set-Location $TARGET_DIR
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Installing/Updating Dependencies" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "$TARGET_DIR\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment and install dependencies
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$TARGET_DIR\venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Building StarSticks.exe" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python build.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "StarSticks.exe has been built successfully!" -ForegroundColor Green
Write-Host "Location: $TARGET_DIR\dist\StarSticks.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now run StarSticks.exe" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
