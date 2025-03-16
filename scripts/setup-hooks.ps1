# Setup Git hooks and dependencies
Write-Host "Setting up Git hooks and dependencies..." -ForegroundColor Green

# Ensure the hooks directory exists
$hooksDir = Join-Path (Get-Location) ".git\hooks"
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install pylint mypy

# Install Node.js dependencies for frontend checks
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
if (Test-Path (Join-Path (Get-Location) "frontend\package.json")) {
    Push-Location frontend
    npm install --save-dev eslint typescript @typescript-eslint/parser @typescript-eslint/eslint-plugin
    Pop-Location
}

# Make pre-commit hook executable
Write-Host "Setting up pre-commit hook..." -ForegroundColor Yellow
$preCommitPath = Join-Path $hooksDir "pre-commit"
$preCommitContent = @"
#!/usr/bin/env pwsh
python `"`$PSScriptRoot/pre-commit`" `$args
"@
$preCommitContent | Out-File -FilePath "$preCommitPath.ps1" -Encoding utf8 -Force

# Create a .bat wrapper for Windows compatibility
$batWrapper = @"
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0\pre-commit.ps1" %*
"@
$batWrapper | Out-File -FilePath $preCommitPath -Encoding ascii -Force

Write-Host "`nGit hooks setup complete!" -ForegroundColor Green
Write-Host "The pre-commit hook will now:"
Write-Host "1. Check code quality using pylint and mypy"
Write-Host "2. Use GitHub Copilot to suggest fixes for any issues"
Write-Host "3. Automatically update relevant documentation"