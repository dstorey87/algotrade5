$processName = "code_cleaner"

# Check if already running
$running = Get-Process -Name $processName -ErrorAction SilentlyContinue
if ($running) {
    Write-Host "Code cleaner is already running"
    exit
}

# Start the code cleaner in watch mode
$pythonPath = "python"
$scriptPath = Join-Path $PSScriptRoot "code_cleaner.py"
$logPath = Join-Path $PSScriptRoot "code_cleaner.log"

Start-Process -FilePath $pythonPath -ArgumentList "$scriptPath --watch --clean" -RedirectStandardOutput $logPath -WindowStyle Hidden

Write-Host "Code cleaner started in watch mode. Check code_cleaner.log for output."