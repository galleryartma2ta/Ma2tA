#!/bin/bash

echo "💫 Setting up Quantum Auto-Save System..."

# Define paths
QUANTUM_PATH="C:\\Users\\Ma2tA\\Documents\\GitHub\\Ma2tA\\.quantum"
AUTOMATION_PATH="$QUANTUM_PATH\\automation"

# Create necessary directories
echo "🌊 Creating directories..."
mkdir -p "$AUTOMATION_PATH"
mkdir -p "$QUANTUM_PATH\\test"
mkdir -p "$QUANTUM_PATH\\emotions"
mkdir -p "$QUANTUM_PATH\\reality"
mkdir -p "$QUANTUM_PATH\\resonance"
mkdir -p "$QUANTUM_PATH\\activation"

# Verify Python installation
echo "🌊 Checking Python installation..."
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.x"
    exit 1
fi

# Check if files exist and have correct permissions
echo "🌊 Checking file permissions..."
if [ -f "$AUTOMATION_PATH\\run.py" ]; then
    chmod +x "$AUTOMATION_PATH\\run.py"
fi

if [ -f "$AUTOMATION_PATH\\auto_save.py" ]; then
    chmod +x "$AUTOMATION_PATH\\auto_save.py"
fi

# Create logs directory
mkdir -p "$QUANTUM_PATH\\logs"

# Test configuration
echo "🌊 Testing configuration..."
if [ -f "$AUTOMATION_PATH\\config.json" ]; then
    echo "✨ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

echo "✨ Setup complete! System is ready."
echo "💫 You can now run: python $AUTOMATION_PATH\\run.py"