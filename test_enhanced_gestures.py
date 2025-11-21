#!/usr/bin/env python3
"""
Enhanced Gesture Test Script
Tests all supported gestures from the Gesture-MediaPlayer-Controller-main model
"""

import requests
import json
import time

def test_enhanced_gestures():
    """Test all enhanced gestures by sending them to the API server"""
    
    print("🎬 Enhanced Gesture Test")
    print("=" * 50)
    
    # Check if API server is running
    api_url = "http://localhost:8081"
    try:
        response = requests.get(f"{api_url}/status", timeout=2)
        if response.status_code != 200:
            print("❌ API server not responding properly")
            return False
    except Exception as e:
        print(f"❌ API server not running: {e}")
        print("💡 Please start the API server first: python gesture_api_server.py")
        return False
    
    print("✅ API server is running")
    print("\n🧪 Testing enhanced gestures...")
    
    # Define all enhanced gestures to test
    enhanced_gestures = [
        {
            "name": "palm_pause_play",
            "description": "Play/Pause video",
            "emoji": "🖐️"
        },
        {
            "name": "fist_mute", 
            "description": "Mute/Unmute",
            "emoji": "✊"
        },
        {
            "name": "thumbs_up_like",
            "description": "Volume Up / Like",
            "emoji": "👍"
        },
        {
            "name": "thumbs_down_dislike",
            "description": "Volume Down / Dislike", 
            "emoji": "👎"
        },
        {
            "name": "fingers_up_volume_up",
            "description": "Volume Up",
            "emoji": "🖖"
        },
        {
            "name": "fingers_down_volume_down",
            "description": "Volume Down",
            "emoji": "👇"
        }
    ]
    
    print(f"\n📋 Will test {len(enhanced_gestures)} gestures:")
    for i, gesture in enumerate(enhanced_gestures, 1):
        print(f"   {i}. {gesture['emoji']} {gesture['name']} - {gesture['description']}")
    
    input("\n🚀 Press Enter to start testing (make sure you have a YouTube/Netflix video open)...")
    
    # Test each gesture
    for i, gesture in enumerate(enhanced_gestures, 1):
        print(f"\n{i}/{len(enhanced_gestures)} Testing: {gesture['emoji']} {gesture['name']}")
        print(f"   Action: {gesture['description']}")
        
        # Send gesture to API
        command = {
            "gesture": gesture['name'],
            "action": get_action_for_gesture(gesture['name']),
            "timestamp": time.time(),
            "test": True
        }
        
        try:
            response = requests.post(f"{api_url}/gesture", json=command, timeout=2)
            if response.status_code == 200:
                print(f"   ✅ Sent successfully")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Wait between tests
        if i < len(enhanced_gestures):
            print("   ⏳ Waiting 3 seconds...")
            time.sleep(3)
    
    print(f"\n✅ Enhanced gesture testing complete!")
    print("💡 Check your browser to see if the gestures worked")
    
    return True

def get_action_for_gesture(gesture_name):
    """Map gesture names to actions"""
    action_map = {
        "palm_pause_play": "pause_play",
        "fist_mute": "mute",
        "thumbs_up_like": "volume_up",
        "thumbs_down_dislike": "volume_down", 
        "fingers_up_volume_up": "volume_up",
        "fingers_down_volume_down": "volume_down"
    }
    return action_map.get(gesture_name, "unknown")

def test_api_connection():
    """Test basic API server connection"""
    print("\n🔌 Testing API Connection")
    print("-" * 30)
    
    api_url = "http://localhost:8081"
    
    try:
        # Test status endpoint
        response = requests.get(f"{api_url}/status", timeout=2)
        print(f"Status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Server status: {data.get('status', 'unknown')}")
            
        # Test gesture endpoint  
        response = requests.get(f"{api_url}/gesture", timeout=2)
        print(f"Gesture endpoint: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    print("🎬 CMPT310 Enhanced Gesture Test Suite")
    print("=" * 60)
    print("Tests the full multi-gesture system with web extension")
    
    # Test API connection first
    if not test_api_connection():
        print("\n💡 Make sure to:")
        print("1. Start API server: python gesture_api_server.py")
        print("2. Install Chrome extension from web-extension/ folder")
        print("3. Open YouTube/Netflix video page")
        return
    
    # Test enhanced gestures
    if not test_enhanced_gestures():
        return
        
    print("\n🎯 Test Results:")
    print("- If gestures worked: Your system is fully functional! 🎉")
    print("- If gestures didn't work:")
    print("  1. Check browser console (F12)")
    print("  2. Verify extension is installed and enabled") 
    print("  3. Make sure you're on a video page (not homepage)")
    print("  4. Try refreshing the page")
    
    print("\n🚀 Next Steps:")
    print("- Run 'python enhanced_gesture_controller.py' for live gesture recognition")
    print("- Use 'python run.py' for interactive menu")
    
if __name__ == "__main__":
    main()
