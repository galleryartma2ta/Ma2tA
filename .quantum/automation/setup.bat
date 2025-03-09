@echo off
chcp 65001 > nul
echo [*] Setting up Quantum Auto-Save System...

set QUANTUM_PATH=C:\Users\Ma2tA\Documents\GitHub\Ma2tA\.quantum
set AUTOMATION_PATH=%QUANTUM_PATH%\automation

echo [*] Creating directories...
if not exist "%AUTOMATION_PATH%" mkdir "%AUTOMATION_PATH%"
if not exist "%QUANTUM_PATH%\test" mkdir "%QUANTUM_PATH%\test"
if not exist "%QUANTUM_PATH%\emotions" mkdir "%QUANTUM_PATH%\emotions"
if not exist "%QUANTUM_PATH%\reality" mkdir "%QUANTUM_PATH%\reality"
if not exist "%QUANTUM_PATH%\resonance" mkdir "%QUANTUM_PATH%\resonance"
if not exist "%QUANTUM_PATH%\activation" mkdir "%QUANTUM_PATH%\activation"
if not exist "%QUANTUM_PATH%\logs" mkdir "%QUANTUM_PATH%\logs"

echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed. Please install Python 3.x
    exit /b 1
)

echo [*] Testing configuration...
if exist "%AUTOMATION_PATH%\config.json" (
    echo [+] Configuration file found
) else (
    echo [X] Configuration file missing
    exit /b 1
)

echo %date% %time% > "%QUANTUM_PATH%\logs\setup.log"
echo User: artgalleryma2ta >> "%QUANTUM_PATH%\logs\setup.log"
echo Status: ACTIVE >> "%QUANTUM_PATH%\logs\setup.log"

echo [+] Setup complete! System is ready.
echo [*] You can now run: python %AUTOMATION_PATH%\run.py
pause