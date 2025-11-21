#!/usr/bin/env python3
"""
🎬 Gesture Media Player - Quick Start Script
This script helps you start the system components easily.
"""

import subprocess
import sys
import time
import os

def start_api_server():
    """Start the API server"""
    print("🚀 Starting API Server...")
    python_path = sys.executable
    try:
        subprocess.Popen([python_path, "src/gesture_api_server.py"])
        print("✅ API Server started on http://localhost:8081")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False

def start_gesture_recognition():
    """Start gesture recognition"""
    print("🚀 Starting Gesture Recognition...")
    python_path = sys.executable
    try:
        subprocess.run([python_path, "src/gesture_recognition.py"])
        return True
    except KeyboardInterrupt:
        print("\n🛑 Gesture recognition stopped")
        return False
    except Exception as e:
        print(f"❌ Failed to start gesture recognition: {e}")
        return False

def main():
    """Main quick start function"""
    print("🎬 Gesture-Controlled Media Player - Quick Start")
    print("=" * 50)
    
    print("\n📋 This will:")
    print("1. Start the API server")
    print("2. Start gesture recognition")
    print("3. You can then use your browser extension")
    
    input("\nPress Enter to continue...")
    
    # Start API server
    if not start_api_server():
        return
    
    # Start gesture recognition
    print("\n📹 Starting camera gesture recognition...")
    print("💡 Show your palm to the camera to pause/play videos")
    print("💡 Press ESC or Ctrl+C to stop")
    
    start_gesture_recognition()

if __name__ == "__main__":
    main()
