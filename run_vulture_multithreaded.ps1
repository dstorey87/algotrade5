#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Runs the multithreaded vulture cleanup process for AlgoTradePro5
.DESCRIPTION
    This script runs the vulture_cleanup.py script with multithreading enabled
    to efficiently scan the codebase for unused code.
.NOTES
    File Name: run_vulture_multithreaded.ps1
    Author: GitHub Copilot
    Date: March 23, 2025
#>

# Set thread count to 14 as requested to reduce load
$cpuCores = 14

Write-Host "Starting multithreaded Vulture code cleanup using $cpuCores threads..."

# Run the vulture cleanup script with multithreading
python vulture_cleanup.py --threads $cpuCores --min-confidence 60 --comment-only

Write-Host "Vulture cleanup process complete."

# Removed the recursive call that was here