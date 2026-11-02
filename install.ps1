# DevSetup Windows One-Line Installer
# Usage: irm https://raw.githubusercontent.com/DEMOCODE675/CloneCode/v2/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host "🐾 Installing DevSetup CLI..." -ForegroundColor Cyan

$RepoUrl = "git+https://github.com/DEMOCODE675/CloneCode.git@v2"
$InstallBase = "$HOME\.devsetup"
$BinDir = "$InstallBase\bin"

# 1. Try pipx if available
if (Get-Command pipx -ErrorAction SilentlyContinue) {
    Write-Host "Found pipx, installing globally in isolated environment..." -ForegroundColor Green
    pipx install --force $RepoUrl
    Write-Host "DevSetup installed successfully via pipx!" -ForegroundColor Green
    devsetup cat
    exit 0
}

# 2. Try uv if available
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "Found uv, installing tool..." -ForegroundColor Green
    uv tool install --force $RepoUrl
    Write-Host "DevSetup installed successfully via uv!" -ForegroundColor Green
    devsetup cat
    exit 0
}

# 3. Use standard Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if (-not $pythonCmd) {
    Write-Host "Error: Python 3.12+ was not found on your system." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/ or via Microsoft Store." -ForegroundColor Yellow
    exit 1
}

Write-Host "Setting up isolated DevSetup environment in $InstallBase..." -ForegroundColor Cyan
if (-not (Test-Path $InstallBase)) {
    New-Item -ItemType Directory -Path $InstallBase -Force | Out-Null
}

$VenvDir = "$InstallBase\venv"
& $pythonCmd -m venv $VenvDir

$VenvPython = "$VenvDir\Scripts\python.exe"
$VenvDevSetup = "$VenvDir\Scripts\devsetup.exe"

Write-Host "Installing latest DevSetup CLI from repository..." -ForegroundColor Cyan
& $VenvPython -m pip install --quiet --upgrade pip
& $VenvPython -m pip install --quiet --upgrade $RepoUrl

if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

# Create wrapper script in bin dir
$ShimCmd = "$BinDir\devsetup.cmd"
"@echo off`r`n`"$VenvDevSetup`" %*" | Set-Content -Path $ShimCmd -Encoding Ascii

# Ensure BinDir is in User PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if ($UserPath -notlike "*$BinDir*") {
    Write-Host "Adding $BinDir to User PATH..." -ForegroundColor Cyan
    $NewPath = "$BinDir;$UserPath"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, [EnvironmentVariableTarget]::User)
    $env:Path = "$BinDir;$env:Path"
}

Write-Host "`n DevSetup is installed and ready to use!`n" -ForegroundColor Green
& $VenvDevSetup cat

