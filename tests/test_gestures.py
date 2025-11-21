#!/usr/bin/env python3
"""
Simple Camera Test and Gesture Demo
Tests camera access and provides manual gesture simulation
"""

import cv2
import time
import requests
import json
import sys

def test_camera():
    """Test camera access with detailed diagnostics"""
    print("🔍 Testing Camera Access...")
    
    for camera_id in range(3):
        print(f"   Testing camera {camera_id}...")
        try:
            cap = cv2.VideoCapture(camera_id)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"   ✅ Camera {camera_id} works! ({frame.shape})")
                    cap.release()
                    return camera_id
                else:
                    print(f"   ❌ Camera {camera_id} opened but can't read frames")
            else:
                print(f"   ❌ Camera {camera_id} failed to open")
            
            cap.release()
        except Exception as e:
            print(f"   ❌ Camera {camera_id} error: {e}")
    
    print("❌ No working cameras found")
    return None

def test_api_server():
    """Test if API server is running"""
    try:
        response = requests.get("http://localhost:8081/status", timeout=2)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
    except:
        pass
    
    print("❌ API server not running")
    print("   Start it with: python gesture_api_server.py")
    return False

def manual_gesture_demo():
    """Manual gesture control demo"""
    print("\n🎮 Manual Gesture Control Demo")
    print("================================")
    print("Commands:")
    print("  p = Send palm gesture (pause/play)")
    print("  s = Check server status") 
    print("  q = Quit")
    print()
    
    while True:
        try:
            command = input("Enter command (p/s/q): ").strip().lower()
            
            if command == 'q':
                break
            elif command == 'p':
                # Send palm gesture
                gesture_data = {
                    "gesture": "palm",
                    "timestamp": time.time(),
                    "action": "pause_play"
                }
                
                try:
                    response = requests.post("http://localhost:8081/gesture", 
                                           json=gesture_data, timeout=2)
                    if response.status_code == 200:
                        print("✅ Palm gesture sent! Check your browser.")
                    else:
                        print(f"❌ Failed to send gesture: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif command == 's':
                test_api_server()
            else:
                print("Unknown command. Use p/s/q")
                
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("👋 Demo ended")

def simple_camera_demo(camera_id):
    """Simple camera display without MediaPipe"""
    print(f"\n📹 Simple Camera Demo (Camera {camera_id})")
    print("Press 'p' to simulate palm gesture, 'q' to quit")
    
    cap = cv2.VideoCapture(camera_id)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Lost camera connection")
                break
            
            # Flip frame for natural interaction
            frame = cv2.flip(frame, 1)
            
            # Add instructions
            cv2.putText(frame, "Press 'p' for palm gesture, 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Show your palm here (simulation only)", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("Simple Camera Test", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                # Send palm gesture
                gesture_data = {
                    "gesture": "palm", 
                    "timestamp": time.time(),
                    "action": "pause_play"
                }
                
                try:
                    response = requests.post("http://localhost:8081/gesture", 
                                           json=gesture_data, timeout=1)
                    if response.status_code == 200:
                        print("✅ Palm gesture sent!")
                        # Show visual feedback
                        cv2.putText(frame, "PALM GESTURE SENT!", (10, 70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        cv2.imshow("Simple Camera Test", frame)
                        cv2.waitKey(500)  # Show message for 500ms
                except Exception as e:
                    print(f"❌ Error sending gesture: {e}")
                    
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    print("🎬 Simple Gesture System Test")
    print("=============================")
    print()
    
    # Test API server
    api_works = test_api_server()
    
    # Test camera
    camera_id = test_camera()
    
    print("\n📋 Available Options:")
    
    if camera_id is not None:
        print("1. Simple camera demo (press 'p' for gesture)")
        print("2. Manual control demo (no camera)")
    else:
        print("1. Manual control demo (no camera needed)")
    
    print("3. Exit")
    
    try:
        if camera_id is not None:
            choice = input("\nChoose option (1/2/3): ").strip()
        else:
            choice = input("\nChoose option (1/3): ").strip()
        
        if choice == "1" and camera_id is not None:
            if api_works:
                simple_camera_demo(camera_id)
            else:
                print("❌ API server needed for camera demo")
        elif choice == "2" or (choice == "1" and camera_id is None):
            if api_works:
                manual_gesture_demo()
            else:
                print("❌ API server needed for gesture demo")
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("Invalid choice")
            
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
