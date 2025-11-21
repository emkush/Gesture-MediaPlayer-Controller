"""
Enhanced Multi-Gesture Media Controller for CMPT310-Project

This controller uses the full MediaPipe gesture recognition model from 
Gesture-MediaPlayer-Controller-main with comprehensive gesture support:
- palm_pause_play: Play/Pause videos
- fist_mute: Mute/Unmute
- thumbs_up_like: Volume up / Like video
- thumbs_down_dislike: Volume down / Dislike video  
- fingers_up_volume_up: Volume up
- fingers_down_volume_down: Volume down

Integrates with the web extension for YouTube/Netflix control.
"""

import cv2
import time
import numpy as np
import requests
import json
from collections import deque
import threading
import sys
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat


class EnhancedGestureController:
    def __init__(self, gesture_model_path="models/gesture_recognizer.task"):
        """Initialize the enhanced gesture controller with full MediaPipe model"""
        print("🎬 Initializing Enhanced Gesture-Controlled Media Player...")
        
        # Gesture model path
        self.gesture_model_path = self.find_model_file(gesture_model_path)
        if not self.gesture_model_path:
            raise FileNotFoundError("gesture_recognizer.task not found!")
        
        # Initialize MediaPipe gesture recognition
        self.setup_mediapipe()
        
        # Gesture mapping for media control
        self.gesture_actions = {
            "palm_pause_play": "pause_play",
            "fist_mute": "mute",
            "thumbs_up_like": "volume_up",
            "thumbs_down_dislike": "volume_down",
            "fingers_up_volume_up": "volume_up",
            "fingers_down_volume_down": "volume_down",
            "none": None
        }
        
        # Enhanced gesture descriptions for UI
        self.gesture_descriptions = {
            "palm_pause_play": "Play/Pause",
            "fist_mute": "Mute/Unmute", 
            "thumbs_up_like": "Volume Up / Like",
            "thumbs_down_dislike": "Volume Down / Dislike",
            "fingers_up_volume_up": "Volume Up",
            "fingers_down_volume_down": "Volume Down",
            "none": "No gesture"
        }
        
        # Gesture colors for visual feedback
        self.gesture_colors = {
            "palm_pause_play": (0, 255, 0),      # Green
            "fist_mute": (0, 0, 255),            # Red
            "thumbs_up_like": (255, 165, 0),     # Orange
            "thumbs_down_dislike": (128, 0, 128), # Purple
            "fingers_up_volume_up": (0, 255, 255), # Cyan
            "fingers_down_volume_down": (255, 0, 255), # Magenta
            "none": (100, 100, 100)              # Gray
        }
        
        # Gesture stabilization
        self.last_gesture = "none"
        self.stable_gesture = "none"
        self.gesture_frames = 0
        self.confirmation_frames = 8  # Require more frames for stability
        
        # Cooldown management
        self.last_action_time = 0
        self.action_cooldown = 2.0  # 2 seconds between actions
        
        # API communication
        self.api_url = "http://localhost:8081"
        
        print(f"✅ Enhanced gesture controller initialized with model: {self.gesture_model_path}")
        print("📋 Supported gestures:")
        for gesture, desc in self.gesture_descriptions.items():
            if gesture != "none":
                print(f"   🖐️ {gesture}: {desc}")
    
    def find_model_file(self, model_path):
        """Find the gesture recognizer model file"""
        possible_paths = [
            model_path,
            "models/gesture_recognizer.task",
            "../models/gesture_recognizer.task",
            "gesture_recognizer.task",
            "/Users/jethrohermawan/310/CMPT310-Project/models/gesture_recognizer.task"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Found gesture model at: {path}")
                return path
        
        print("❌ Gesture model not found in any of these locations:")
        for path in possible_paths:
            print(f"   - {path}")
        return None
    
    def setup_mediapipe(self):
        """Setup MediaPipe gesture recognition"""
        try:
            # Create gesture recognizer
            gesture_options = vision.GestureRecognizerOptions(
                base_options=python.BaseOptions(model_asset_path=self.gesture_model_path),
                running_mode=vision.RunningMode.IMAGE,
                num_hands=1,
                min_hand_detection_confidence=0.6,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.gesture_recognizer = vision.GestureRecognizer.create_from_options(gesture_options)
            
            print("✅ MediaPipe gesture recognizer initialized")
        except Exception as e:
            print(f"❌ MediaPipe initialization failed: {e}")
            raise
    
    def test_api_connection(self):
        """Test connection to the API server"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=2)
            if response.status_code == 200:
                print("✅ API server connection successful")
                return True
            else:
                print(f"⚠️ API server responded with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API server connection failed: {e}")
            return False
    
    def find_working_camera(self):
        """Find the first working camera"""
        print("🔍 Searching for available cameras...")
        
        for camera_id in range(5):  # Try cameras 0-4
            try:
                cap = cv2.VideoCapture(camera_id)
                if cap.isOpened():
                    # Test if we can actually read a frame
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"✅ Found working camera at index {camera_id}")
                        return cap, camera_id
                    cap.release()
            except Exception as e:
                print(f"   Camera {camera_id}: {str(e)}")
                continue
        
        print("❌ No working camera found")
        return None, -1
    
    def recognize_gesture(self, frame):
        """Recognize gesture from frame using MediaPipe model"""
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = Image(image_format=ImageFormat.SRGB, data=rgb_frame)
            
            # Recognize gesture
            result = self.gesture_recognizer.recognize(mp_image)
            
            gesture_name = "none"
            confidence = 0.0
            
            # Extract the top gesture prediction
            if result.gestures:
                top_gesture = result.gestures[0][0]  # First hand, top prediction
                gesture_name = top_gesture.category_name
                confidence = top_gesture.score
            
            return gesture_name, confidence
            
        except Exception as e:
            print(f"Error in gesture recognition: {e}")
            return "none", 0.0
    
    def stabilize_gesture(self, raw_gesture):
        """Apply gesture stabilization to reduce flickering"""
        if raw_gesture == self.last_gesture:
            self.gesture_frames += 1
        else:
            self.gesture_frames = 0
        
        # Only update stable gesture if we've seen it consistently
        if self.gesture_frames >= self.confirmation_frames:
            self.stable_gesture = raw_gesture
        
        self.last_gesture = raw_gesture
        return self.stable_gesture
    
    def send_gesture_command(self, gesture, action):
        """Send gesture command to the web extension API"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_action_time < self.action_cooldown:
            return False
        
        if action is None:
            return False
        
        self.last_action_time = current_time
        
        # Prepare command
        command = {
            "gesture": gesture,
            "action": action,
            "timestamp": current_time,
            "description": self.gesture_descriptions.get(gesture, "Unknown")
        }
        
        print(f"🖐️ Gesture: {gesture} -> Action: {action}")
        
        # Send to API server
        try:
            response = requests.post(f"{self.api_url}/gesture", json=command, timeout=1)
            if response.status_code == 200:
                print(f"   ✅ Command sent successfully: {action}")
                return True
            else:
                print(f"   ❌ Failed to send command: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ⚠️ API server not responding: {e}")
            return False
    
    def draw_gesture_info(self, frame, gesture, confidence):
        """Draw gesture information on frame"""
        h, w = frame.shape[:2]
        
        # Get color for current gesture
        color = self.gesture_colors.get(gesture, (255, 255, 255))
        description = self.gesture_descriptions.get(gesture, gesture)
        
        # Draw main gesture info
        gesture_text = f"Gesture: {description}"
        confidence_text = f"Confidence: {confidence:.2f}"
        
        # Background rectangle for text
        cv2.rectangle(frame, (10, 10), (400, 80), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (400, 80), color, 2)
        
        # Draw text
        cv2.putText(frame, gesture_text, (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, confidence_text, (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw stabilization info
        stability_text = f"Stability: {self.gesture_frames}/{self.confirmation_frames}"
        cv2.putText(frame, stability_text, (20, h - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Draw gesture legend
        legend_y = 100
        cv2.putText(frame, "Gesture Guide:", (20, legend_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        for i, (gest, desc) in enumerate(self.gesture_descriptions.items()):
            if gest != "none":
                y_pos = legend_y + 20 + (i * 20)
                gest_color = self.gesture_colors.get(gest, (255, 255, 255))
                cv2.putText(frame, f"• {desc}", (25, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, gest_color, 1)
    
    def run_camera(self):
        """Main camera loop with enhanced gesture recognition"""
        # Check API connection
        api_connected = self.test_api_connection()
        if not api_connected:
            print("⚠️ API server not running. Starting in demo mode...")
            print("💡 To enable full functionality, run: python gesture_api_server.py")
        
        # Find working camera
        cap, camera_id = self.find_working_camera()
        if cap is None:
            print("\n❌ Camera Error Solutions:")
            print("1. Check camera permissions in System Preferences")
            print("2. Close other apps using camera (Zoom, Skype, etc.)")
            print("3. Try demo mode instead")
            return False
        
        print(f"\n🎥 Starting enhanced gesture recognition with camera {camera_id}")
        print("📋 Instructions:")
        print("   • Show gestures clearly to the camera")
        print("   • Maintain good lighting")
        print("   • Keep hand 1-2 feet from camera")
        print("   • Gestures need to be stable for 8 frames")
        print("   • Press 'ESC' or 'q' to exit")
        
        frame_count = 0
        fps_tracker = deque(maxlen=30)
        
        try:
            while True:
                start_time = time.time()
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Failed to read frame - camera disconnected?")
                    break
                
                frame_count += 1
                
                # Flip frame for natural interaction
                frame = cv2.flip(frame, 1)
                
                # Process every frame for responsive gesture recognition
                raw_gesture, confidence = self.recognize_gesture(frame)
                
                # Apply gesture stabilization
                stable_gesture = self.stabilize_gesture(raw_gesture)
                
                # Send command if gesture is stable and confident
                if (stable_gesture != "none" and 
                    confidence > 0.7 and 
                    stable_gesture in self.gesture_actions):
                    
                    action = self.gesture_actions[stable_gesture]
                    if action and api_connected:
                        self.send_gesture_command(stable_gesture, action)
                
                # Draw gesture information
                self.draw_gesture_info(frame, stable_gesture, confidence)
                
                # Calculate and display FPS
                frame_time = time.time() - start_time
                fps_tracker.append(1.0 / frame_time if frame_time > 0 else 0)
                avg_fps = sum(fps_tracker) / len(fps_tracker)
                
                cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, frame.shape[0] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Display instructions
                cv2.putText(frame, "ESC/Q: Quit | Show gestures for media control", 
                           (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                cv2.imshow("Enhanced Gesture-Controlled Media Player", frame)
                
                # Exit conditions
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord('q'):  # ESC or 'q'
                    break
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("✅ Camera released and windows closed")
        
        return True


def main():
    print("🎬 Enhanced Gesture-Controlled Media Player")
    print("==========================================")
    print("Using full MediaPipe model with comprehensive gesture support!")
    
    try:
        controller = EnhancedGestureController()
        success = controller.run_camera()
        
        if not success:
            print("\n💡 Troubleshooting tips:")
            print("1. Check camera permissions")
            print("2. Close other camera applications")
            print("3. Ensure gesture_recognizer.task is in models/ folder")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\n💡 Make sure:")
        print("1. gesture_recognizer.task is in models/ folder")
        print("2. MediaPipe is installed: pip install mediapipe")
        print("3. Camera is available and not in use")


if __name__ == "__main__":
    main()
