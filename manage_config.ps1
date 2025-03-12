# PowerShell script to manage AlgoTradPro5 configuration
param(
    [string]$action = "check",
    [string]$strategy = "QuantumHybridStrategy"
)

# Ensure we're in the correct directory
Set-Location $PSScriptRoot

function Backup-Config {
    if (Test-Path "freqtrade/config.json") {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Copy-Item "freqtrade/config.json" "freqtrade/config_backup_$timestamp.json"
        Write-Host "Configuration backed up to config_backup_$timestamp.json"
    }
}

function Restore-LastConfig {
    $backups = Get-ChildItem "freqtrade/config_backup_*.json" | Sort-Object LastWriteTime -Descending
    if ($backups.Count -gt 0) {
        Copy-Item $backups[0].FullName "freqtrade/config.json"
        Write-Host "Configuration restored from $($backups[0].Name)"
    } else {
        Write-Host "No configuration backups found"
    }
}

function Reset-Config {
    Backup-Config
    python setup_config.py
    Write-Host "Configuration reset to defaults"
}

switch ($action) {
    "backup" {
        Backup-Config
    }
    "restore" {
        Restore-LastConfig
    }
    "reset" {
        Reset-Config
    }
    "check" {
        if (Test-Path "freqtrade/config.json") {
            Write-Host "Configuration exists and will be validated..."
            python initialize_system.py
        } else {
            Write-Host "Configuration not found, generating new one..."
            Reset-Config
        }
    }
    default {
        Write-Host "Invalid action. Use: check, backup, restore, or reset"
    }
}