# PowerShell script for Poetry-based installation
[CmdletBinding()]
param(
    [switch]$force = $false,
    [switch]$dev = $false,
    [switch]$withJupyter = $false
)

# Ensure we're in the correct directory
Set-Location $PSScriptRoot

function Find-Python {
    try {
        # Try common Python installation locations
        $pythonPaths = @(
            "C:\Python310\python.exe",
            "C:\Program Files\Python310\python.exe",
            "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python310\python.exe",
            "C:\Python311\python.exe",
            "C:\Program Files\Python311\python.exe",
            "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe"
        )

        foreach ($path in $pythonPaths) {
            if (Test-Path $path) {
                # Verify it's a real Python installation
                try {
                    $version = & $path -c "import sys; print(sys.version_info[0:2])" 2>$null
                    if ($version -match "(3, 1[01])") {
                        Write-Host "Found Python at: $path"
                        return $path
                    }
                } catch {
                    continue
                }
            }
        }

        # Try py launcher as a last resort
        $pyLauncher = Get-Command "py" -ErrorAction SilentlyContinue
        if ($pyLauncher) {
            $pythonPath = & py -3.10 -c "import sys; print(sys.executable)" 2>$null
            if ($pythonPath -and (Test-Path $pythonPath)) {
                Write-Host "Found Python via py launcher: $pythonPath"
                return $pythonPath
            }
        }

        throw "Could not find a suitable Python 3.10+ installation"
    } catch {
        Write-Error "Failed to find Python: $_"
        return $null
    }
}

function Install-FreqTrade {
    try {
        Write-Host "Installing FreqTrade from source..."
        
        # Check if freqtrade directory exists
        if (-not (Test-Path "freqtrade")) {
            Write-Host "Cloning FreqTrade repository..."
            git clone --single-branch --branch develop https://github.com/freqtrade/freqtrade.git
            if (-not $?) {
                throw "Failed to clone FreqTrade repository"
            }
        }
        
        Push-Location freqtrade
        
        # Ensure FreqTrade directory is clean
        Write-Host "Updating FreqTrade source..."
        git reset --hard
        git clean -fdx
        git pull
        
        # Install in development mode using Poetry's venv Python
        Write-Host "Installing FreqTrade in development mode..."
        $pythonPath = poetry env info --path
        if ($pythonPath) {
            $pythonExe = Join-Path $pythonPath "Scripts\python.exe"
            & $pythonExe -m pip install -e . --no-deps
            if (-not $?) {
                throw "Failed to install FreqTrade in development mode"
            }
        } else {
            throw "Poetry environment not found"
        }
        
        Pop-Location
        Write-Host "[OK] FreqTrade installed successfully"
        return $true
        
    } catch {
        Write-Error "Failed to install FreqTrade: $_"
        if ($PSItem.ScriptStackTrace) {
            Write-Error $PSItem.ScriptStackTrace
        }
        return $false
    }
}

function Install-Poetry {
    param (
        [string]$pythonPath
    )

    try {
        $poetry = Get-Command "poetry" -ErrorAction SilentlyContinue
        if (-not $poetry) {
            Write-Host "Installing Poetry..."

            if (-not $pythonPath) {
                throw "Python path not provided"
            }

            # Set Python path for Poetry installer
            $env:POETRY_PYTHON = $pythonPath
            
            # Install Poetry using the specific Python
            Write-Host "Installing Poetry using Python at: $pythonPath"
            (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | & $pythonPath -
            if (-not $?) {
                throw "Poetry installation failed"
            }

            # Add Poetry to PATH
            $poetryPath = "$env:APPDATA\Python\Scripts"
            $env:Path += ";$poetryPath"
            [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
            
            # Verify installation
            $poetry = Get-Command "poetry" -ErrorAction Stop
            Write-Host "[OK] Poetry installed successfully"
        } else {
            Write-Host "[OK] Poetry already installed"
        }

        # Force Poetry to use the specific Python version
        Write-Host "Configuring Poetry to use Python at: $pythonPath"
        poetry env use $pythonPath
        if (-not $?) {
            throw "Failed to configure Poetry to use Python at: $pythonPath"
        }

        return $true
    } catch {
        Write-Error "Failed to install/configure Poetry: $_"
        if ($PSItem.ScriptStackTrace) {
            Write-Error $PSItem.ScriptStackTrace
        }
        return $false
    }
}

# Verify Python installation first
Write-Host "Looking for Python 3.10 or later..."
$pythonPath = Find-Python
if (-not $pythonPath) {
    Write-Error "No suitable Python installation found. Please install Python 3.10 or later."
    exit 1
}

Write-Host "Using Python installation at: $pythonPath"

# Install and configure Poetry with the found Python
if (-not (Install-Poetry -pythonPath $pythonPath)) {
    exit 1
}

# Configure Poetry
Write-Host "Configuring Poetry..."
poetry config virtualenvs.in-project true
poetry config installer.max-workers 4

# Clean installation if force flag is used
if ($force) {
    Write-Host "Force flag detected - cleaning existing environment..."
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force ".venv"
    }
    if (Test-Path "poetry.lock") {
        Remove-Item -Force "poetry.lock"
    }
}

# Install dependencies with Poetry
Write-Host "Installing dependencies..."
$installArgs = @()
if ($dev) {
    $installArgs += "--with"
    $installArgs += "dev"
}
if ($withJupyter) {
    $installArgs += "--with"
    $installArgs += "jupyter"
}
$installArgs += "--no-interaction"

Write-Host "Running poetry install $($installArgs -join ' ')"

# Force Poetry to use the correct Python for dependency installation
$env:POETRY_PYTHON = $pythonPath
poetry install @installArgs

if (-not $?) {
    Write-Error "Failed to install dependencies"
    exit 1
}

# Install FreqTrade from source
if (-not (Install-FreqTrade)) {
    Write-Error "Failed to install FreqTrade"
    exit 1
}

Write-Host "`nInstallation complete!"
Write-Host "To activate the environment: poetry shell"
Write-Host "To run the trading bot: poetry run python run_algotradpro5.py"
if (-not $withJupyter) {
    Write-Host "To install Jupyter support: poetry install --with jupyter"
}