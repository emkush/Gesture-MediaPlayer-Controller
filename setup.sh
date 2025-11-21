#!/bin/bash

# CMPT310-Project Setup Script
# Automated setup for the Gesture-Controlled Media Player

echo "🎬 CMPT 310 Gesture-Controlled Media Player Setup"
echo "=================================================="
echo

# Check Python installation
echo "✅ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version found"

# Create virtual environment if it doesn't exist
if [ ! -d "myvenv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv myvenv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source myvenv/bin/activate

# Install required packages
echo "📦 Installing required packages..."
pip install --upgrade pip
pip install opencv-python mediapipe tensorflow numpy scikit-learn requests

echo
echo "🎯 Setup Complete!"
echo "=================="
echo
echo "Next steps:"
echo "1. Install Chrome extension:"
echo "   - Open chrome://extensions/"
echo "   - Enable Developer mode"
echo "   - Click 'Load unpacked'"
echo "   - Select the 'web-extension/' folder"
echo
echo "2. Run the application:"
echo "   python run.py"
echo
echo "3. Choose Option 1 for Enhanced Multi-Gesture control!"
echo "   Supports: Palm, Thumbs Up/Down, Fist, and more!"
echo
echo "🖐️ Gesture Support:"
echo "   🖐️ Palm - Play/Pause"
echo "   👍 Thumbs Up - Volume Up"  
echo "   👎 Thumbs Down - Volume Down"
echo "   ✊ Fist - Mute/Unmute"
echo
echo "🎬 Ready to control media with enhanced gestures!"
