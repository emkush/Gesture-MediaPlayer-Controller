#!/usr/bin/env python3
"""
🎬 Gesture-Controlled Media Player - Main Launcher
Interactive menu to run different components of the system
"""

import subprocess
import sys
import os
import time

def print_header():
    print("\n" + "="*70)
    print("🎬 GESTURE-CONTROLLED MEDIA PLAYER")
    print("="*70)
    print("🖐️  Control YouTube & Netflix with palm gestures!")
    print("📹 Show your palm to pause/play videos")
    print("="*70)

def check_api_server():
    """Check if API server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8081/status", timeout=1)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Start the API server in background"""
    print("🚀 Starting API server...")
    try:
        # Use the virtual environment Python
        python_path = "/Users/jethrohermawan/310/Project/myvenv/bin/python"
        subprocess.Popen([python_path, "src/gesture_api_server.py"])
        time.sleep(2)  # Give it time to start
        return check_api_server()
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False

def run_script(script_path, description):
    """Run a Python script with proper error handling"""
    print(f"\n🚀 Starting: {description}")
    print("-" * 50)
    
    # Use the virtual environment Python
    python_path = "/Users/jethrohermawan/310/Project/myvenv/bin/python"
    
    try:
        subprocess.run([python_path, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}: {e}")
    except KeyboardInterrupt:
        print(f"\n⚠️ {description} interrupted by user")
    except FileNotFoundError:
        print(f"❌ File not found: {script_path}")

def main_menu():
    """Show main menu with most important options"""
    while True:
        print_header()
        
        print("\n📋 CHOOSE AN OPTION:")
        print("1. 🚀 Enhanced Multi-Gesture Control (RECOMMENDED)")
        print("2. 🤖 MediaPipe Gesture Control (Uses your .task file)")
        print("3. 🎯 AI Gesture Recognition (Advanced)")
        print("4. 📹 Manual Camera Test (Press 'p' to trigger)")
        print("5. 🧪 Test Extension (No camera needed)")
        print("6. 🔧 Debug & Troubleshoot")
        print("7. 📄 View Documentation")
        print("0. ❌ Exit")
        
        # Show API server status
        api_status = "🟢 Running" if check_api_server() else "🔴 Not Running"
        print(f"\n📡 API Server Status: {api_status}")
        print()
        
        choice = input("👉 Enter your choice (0-7): ").strip()
        
        if choice == "1":
            # Enhanced Multi-Gesture Control (NEW)
            if not check_api_server():
                print("⚠️ API server not running. Starting it first...")
                if not start_api_server():
                    print("❌ Failed to start API server. Please start it manually.")
                    input("Press Enter to continue...")
                    continue
            
            print("\n🚀 Starting Enhanced Multi-Gesture Control...")
            print("💡 Full gesture support: Palm, Thumbs, Fist, and more!")
            print("📋 Gestures supported:")
            print("   🖐️ Palm - Play/Pause")
            print("   👍 Thumbs Up - Volume Up")  
            print("   👎 Thumbs Down - Volume Down")
            print("   ✊ Fist - Mute/Unmute")
            print("   🖖 Fingers Up/Down - Volume Control")
            run_script("enhanced_gesture_controller.py", "Enhanced Multi-Gesture Controller")
            
        elif choice == "2":
            # MediaPipe Gesture Control
            if not check_api_server():
                print("⚠️ API server not running. Starting it first...")
                if not start_api_server():
                    print("❌ Failed to start API server. Please start it manually.")
                    input("Press Enter to continue...")
                    continue
            
            print("\n🤖 Starting MediaPipe Gesture Control...")
            print("💡 This uses your gesture_recognizer.task file for better accuracy!")
            run_script("src/mediapipe_gesture_controller.py", "MediaPipe Gesture Controller")
            
        elif choice == "3":
            # AI Gesture Recognition
            if not check_api_server():
                print("⚠️ API server not running. Starting it first...")
                if not start_api_server():
                    print("❌ Failed to start API server. Please start it manually.")
                    input("Press Enter to continue...")
                    continue
            
            run_script("src/gesture_recognition.py", "AI Gesture Recognition")
            
        elif choice == "4":
            # Manual Camera Test
            if not check_api_server():
                print("⚠️ API server not running. Starting it first...")
                if not start_api_server():
                    print("❌ Failed to start API server. Please start it manually.")
                    input("Press Enter to continue...")
                    continue
            
            run_script("tests/test_gestures.py", "Manual Camera Test")
            
        elif choice == "5":
            # Test Extension
            if not check_api_server():
                print("⚠️ API server not running. Starting it first...")
                if not start_api_server():
                    print("❌ Failed to start API server. Please start it manually.")
                    input("Press Enter to continue...")
                    continue
            
            run_script("tests/test_extension.py", "Extension Test")
            
        elif choice == "6":
            # Debug & Troubleshoot
            print("\n🔧 Available Debug Tools:")
            print("1. Test MediaPipe task file")
            print("2. System diagnostics")
            print("3. Debug gesture detection")
            debug_choice = input("Choose (1-3): ").strip()
            if debug_choice == "1":
                run_script("tests/test_mediapipe_task.py", "MediaPipe Task Test")
            elif debug_choice == "2":
                run_script("tests/debug_detection.py", "System Diagnostics")
            elif debug_choice == "3":
                run_script("tests/debug_detection.py", "Debug Gesture Detection")
            
        elif choice == "7":
            # Documentation
            print("\n📚 DOCUMENTATION:")
            print("- README.md - Main project documentation")
            print("- docs/SETUP.md - Setup instructions")
            print("- docs/TROUBLESHOOTING.md - Common issues")
            print("- INTEGRATION_SUMMARY.md - Project integration details")
            print("\n💡 Check the web-extension folder for Chrome extension files")
            input("Press Enter to continue...")
            
        elif choice == "0":
            print("\n👋 Thanks for using the Enhanced Gesture-Controlled Media Player!")
            print("🎬 Happy gesture controlling!")
            break
            
        else:
            print("⚠️ Invalid choice. Please enter a number from 0-7.")
            input("Press Enter to continue...")

def main():
    """Main function to run the launcher"""
    main_menu()

def show_setup_instructions():
    """Show setup instructions"""
    print("\n" + "="*60)
    print("📋 SETUP INSTRUCTIONS")
    print("="*60)
    
    print("""
🔧 CHROME EXTENSION SETUP:
1. Open Chrome → chrome://extensions/
2. Enable 'Developer mode' (top right toggle)
3. Click 'Load unpacked' 
4. Select: /Users/jethrohermawan/310/Project/web-extension/

📺 BROWSER SETUP:
1. Open YouTube or Netflix
2. Start playing a video (not on homepage!)
3. Click the 🎬 extension icon
4. Click 'Start Detection' → should turn GREEN

🖥️ SYSTEM SETUP:
Terminal 1: python gesture_api_server.py  (keep running)
Terminal 2: Choose one of the options from main menu

🎯 TESTING ORDER:
1. Test Extension (option 1) - verify browser communication
2. Test Camera (option 2) - verify camera works  
3. Full AI (option 3) - complete gesture recognition

💡 TROUBLESHOOTING:
- Option 4 in main menu runs diagnostics
- Check camera permissions in System Preferences
- Make sure you're on a VIDEO page, not homepage
""")
    
    input("Press Enter to return to menu...")

if __name__ == "__main__":
    main()
