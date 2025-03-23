# Run this script as Administrator
$pythonPath = "C:\Users\darre\AppData\Local\Programs\Python\Python311"
$pythonScripts = "C:\Users\darre\AppData\Local\Programs\Python\Python311\Scripts"

# Get the current PATH for the system
$currentSystemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

# Add Python paths if they're not already there
if (-not $currentSystemPath.Contains($pythonPath)) {
    $newSystemPath = $currentSystemPath + ";" + $pythonPath
    [Environment]::SetEnvironmentVariable("Path", $newSystemPath, "Machine")
}

if (-not $currentSystemPath.Contains($pythonScripts)) {
    $newSystemPath = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + $pythonScripts
    [Environment]::SetEnvironmentVariable("Path", $newSystemPath, "Machine")
}

# Set PYTHONHOME
[Environment]::SetEnvironmentVariable("PYTHONHOME", $pythonPath, "Machine")

# Disable Python Launcher to prevent Microsoft Store redirects
$appExecPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\python.exe"
if (Test-Path $appExecPath) {
    Remove-Item $appExecPath -Force
}

Write-Host "Python paths have been set up. Please restart your terminal for changes to take effect."
Write-Host "Python executable path: $pythonPath\python.exe"
Write-Host "Python Scripts path: $pythonScripts"