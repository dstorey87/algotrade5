$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting AlgoTradePro5 System Validation" -ForegroundColor Cyan

# 1. Check Python environment
try {
    python --version
    pip --version
} catch {
    Write-Host "❌ Python environment not properly configured" -ForegroundColor Red
    exit 1
}

# 2. Check Docker
try {
    docker --version
    docker ps
} catch {
    Write-Host "❌ Docker not running or not installed" -ForegroundColor Red
    exit 1
}

# 3. Run system validation tests
Write-Host "📋 Running system validation tests..." -ForegroundColor Yellow
python src/tests/system_validation.py

# 4. Check test results
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All tests passed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Some tests failed. Please check the output above." -ForegroundColor Red
}
