# Quantum System Setup Script
Write-Host "💫 Setting up Quantum Auto-Save System..." -ForegroundColor Cyan

# Define paths
$QUANTUM_PATH = "C:\Users\Ma2tA\Documents\GitHub\Ma2tA\.quantum"
$AUTOMATION_PATH = "$QUANTUM_PATH\automation"

# Create necessary directories
Write-Host "🌊 Creating directories..." -ForegroundColor Blue
$directories = @(
    "$AUTOMATION_PATH",
    "$QUANTUM_PATH\test",
    "$QUANTUM_PATH\emotions",
    "$QUANTUM_PATH\reality",
    "$QUANTUM_PATH\resonance",
    "$QUANTUM_PATH\activation",
    "$QUANTUM_PATH\logs"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Verify Python installation
Write-Host "🌊 Checking Python installation..." -ForegroundColor Blue
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python is not installed. Please install Python 3.x" -ForegroundColor Red
    exit 1
}

# Check configuration file
Write-Host "🌊 Testing configuration..." -ForegroundColor Blue
$configPath = "$AUTOMATION_PATH\config.json"
if (Test-Path $configPath) {
    Write-Host "✨ Configuration file found" -ForegroundColor Green
}
else {
    Write-Host "❌ Configuration file missing" -ForegroundColor Red
    exit 1
}

# Create timestamp file
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
@"
Last Setup: $timestamp
User: artgalleryma2ta
Status: ACTIVE
"@ | Out-File -FilePath "$QUANTUM_PATH\logs\setup.log" -Encoding UTF8

Write-Host "✨ Setup complete! System is ready." -ForegroundColor Green
Write-Host "💫 You can now run: python $AUTOMATION_PATH\run.py" -ForegroundColor Cyan