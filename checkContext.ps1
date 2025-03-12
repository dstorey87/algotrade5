# Pre-commit hook for AlgoTradPro5
# Validates documentation and integration requirements

$ErrorActionPreference = "Stop"

function Test-MDFileContent {
    param (
        [string]$FilePath,
        [string[]]$RequiredSections
    )
    
    $content = Get-Content $FilePath -Raw
    $missingCount = 0
    $missingSections = @()
    
    foreach ($section in $RequiredSections) {
        if ($content -notmatch $section) {
            $missingCount++
            $missingSections += $section
        }
    }
    
    return @{
        IsValid = $missingCount -eq 0
        MissingSections = $missingSections
    }
}

function Test-FileInteractions {
    param (
        [string]$FilePath
    )
    
    $content = Get-Content $FilePath -Raw
    $hasInteractions = $content -match "## Interactions"
    $hasMissingIntegrations = $content -match "## Missing Integrations"
    $hasRedundantCode = $content -match "## Redundant Code"
    
    return @{
        IsValid = $hasInteractions -and $hasMissingIntegrations -and $hasRedundantCode
        MissingDocs = @(
            if (-not $hasInteractions) { "Interactions" }
            if (-not $hasMissingIntegrations) { "Missing Integrations" }
            if (-not $hasRedundantCode) { "Redundant Code" }
        )
    }
}

# Get changed files
$changedFiles = git diff --cached --name-only

# Core documentation files that must always be updated
$coreDocFiles = @(
    "ARCHITECTURE_ANALYSIS.md",
    "SYSTEM_JOURNAL.md",
    "TRADING_STRATEGY.md",
    "readme.md"
)

# Required sections in documentation
$requiredSections = @(
    "## Interactions",
    "## Missing Integrations",
    "## Redundant Code",
    "## Component Relationships",
    "## Data Flow",
    "## Error Handling"
)

$errors = @()

# Check each changed file
foreach ($file in $changedFiles) {
    $ext = [System.IO.Path]::GetExtension($file)
    
    # Python file changes must be documented
    if ($ext -eq ".py") {
        $docUpdated = $false
        foreach ($docFile in $coreDocFiles) {
            if ($changedFiles -contains $docFile) {
                $docUpdated = $true
                break
            }
        }
        
        if (-not $docUpdated) {
            $errors += "Python file '$file' was modified but no documentation files were updated"
        }
        
        # Check ARCHITECTURE_ANALYSIS.md for interaction documentation
        $archResult = Test-FileInteractions "ARCHITECTURE_ANALYSIS.md"
        if (-not $archResult.IsValid) {
            $errors += "ARCHITECTURE_ANALYSIS.md missing sections for '$file': $($archResult.MissingDocs -join ', ')"
        }
    }
}

# Validate core documentation files
foreach ($docFile in $coreDocFiles) {
    if (Test-Path $docFile) {
        $result = Test-MDFileContent -FilePath $docFile -RequiredSections $requiredSections
        if (-not $result.IsValid) {
            $errors += "$docFile is missing required sections: $($result.MissingSections -join ', ')"
        }
    }
}

# Check specific integration requirements
if ($changedFiles -match "ai_model_manager.py|strategy_engine.py|quantum_optimizer.py") {
    if (-not ($changedFiles -contains "system_integration.py")) {
        $errors += "Changes to AI/Quantum components require updates to system_integration.py"
    }
}

# Report errors and exit
if ($errors.Count -gt 0) {
    Write-Host "`nPre-commit validation failed:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "- $error" -ForegroundColor Red
    }
    Write-Host "`nPlease fix the above issues and try committing again" -ForegroundColor Yellow
    exit 1
}

Write-Host "Pre-commit validation passed" -ForegroundColor Green
exit 0
