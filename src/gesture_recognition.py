import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import json
import time
import requests
from collections import deque
import threading
import sys
import os

class ImprovedGestureRecognizer:
    def __init__(self, model_path="palm_gesture_model.h5"):
        """Initialize the improved gesture recognizer with better error handling"""
        print("🎬 Initializing Gesture-Controlled Media Player...")
        
        # Suppress TensorFlow warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel('ERROR')
        
        # Load or create model and scaler
        self.model = self.load_or_create_model(model_path)
        self.scaler = self.load_scaler()
        
        # MediaPipe setup with error handling
        self.setup_mediapipe()
        
        # Gesture detection parameters
        self.palm_threshold = 0.7  # Higher threshold since model seems biased toward palm
        self.gesture_buffer = deque(maxlen=5)  # Shorter buffer for responsiveness
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # Shorter cooldown
        
        # API communication
        self.api_url = "http://localhost:8081"
        
        print("✅ Gesture recognizer initialized successfully")
    
    def load_scaler(self):
        """Load feature scaler for AI model"""
        try:
            import joblib
            scaler = joblib.load("palm_scaler.pkl")
            print("✅ Loaded feature scaler")
            return scaler
        except Exception as e:
            print(f"⚠️ Could not load scaler: {e}")
            return None
    
    def test_api_connection(self):
        """Test connection to the API server"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def load_or_create_model(self, model_path):
        """Load model with better error handling"""
        try:
            # Suppress specific TensorFlow warnings
            with tf.keras.utils.custom_object_scope({}):
                model = tf.keras.models.load_model(model_path, compile=False)
            
            # Recompile to avoid metric warnings
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            print(f"✅ Loaded trained model from {model_path}")
            return model
        except Exception as e:
            print(f"⚠️  Could not load model ({e}). Creating basic structure...")
            return self.create_basic_model()
    
    def load_scaler(self):
        """Load the feature scaler if available"""
        try:
            import joblib
            scaler = joblib.load("palm_scaler.pkl")
            print("✅ Loaded feature scaler")
            return scaler
        except Exception as e:
            print(f"⚠️ Could not load scaler ({e}). Will use raw features.")
            return None
    
    def create_basic_model(self):
        """Create a basic model structure"""
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(63,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def setup_mediapipe(self):
        """Setup MediaPipe with better error handling"""
        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.6,  # Lower for better detection
                min_tracking_confidence=0.4
            )
            self.mp_drawing = mp.solutions.drawing_utils
            print("✅ MediaPipe initialized")
        except Exception as e:
            print(f"❌ MediaPipe initialization failed: {e}")
            raise
    
    def find_working_camera(self):
        """Find the first working camera"""
        print("🔍 Searching for available cameras...")
        
        # Try different camera indices
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
    
    def extract_landmarks(self, hand_landmarks):
        """Extract hand landmarks as a feature vector"""
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
        return np.array(landmarks)
    
    def detect_palm_simple(self, landmarks):
        """Simple palm detection based on hand geometry (fallback)"""
        try:
            # Reshape landmarks to 21 points x 3 coordinates
            points = landmarks.reshape(21, 3)
            
            # MediaPipe hand landmarks: 0=wrist, 4=thumb_tip, 8=index_tip, 12=middle_tip, 16=ring_tip, 20=pinky_tip
            fingertips = [8, 12, 16, 20]  # Four main fingers (excluding thumb for now)
            wrist = points[0]
            
            extended_fingers = 0
            finger_threshold = 0.08  # Stricter threshold - fingers must be clearly extended
            
            # Check each of the four main fingers
            for tip_idx in fingertips:
                tip = points[tip_idx]
                # If fingertip is significantly above wrist, finger is extended
                if tip[1] < wrist[1] - finger_threshold:
                    extended_fingers += 1
            
            # Check thumb separately (different geometry)
            thumb_tip = points[4]
            thumb_base = points[1]  # Thumb base for better comparison
            # Thumb is extended if it's far from the palm center OR spread out
            thumb_extended = (abs(thumb_tip[0] - wrist[0]) > 0.10) or (abs(thumb_tip[0] - thumb_base[0]) > 0.08)
            if thumb_extended:
                extended_fingers += 1
            
            # VERY STRICT palm detection: Nearly ALL fingers must be extended for a true palm
            # This prevents peace signs, OK signs, pointing, etc. from being detected as palm
            confidence = extended_fingers / 5.0
            is_palm = extended_fingers >= 4.5  # At least 4.5 out of 5 fingers must be extended (almost all)
            
            return is_palm, confidence
            
        except Exception as e:
            print(f"Error in simple palm detection: {e}")
            return False, 0.0
    
    def detect_palm(self, landmarks):
        """Detect if current hand pose is a palm gesture"""
        try:
            # Get simple detection first (more reliable)
            is_palm_simple, confidence_simple = self.detect_palm_simple(landmarks)
            
            # Try AI model as secondary validation
            try:
                landmarks_reshaped = landmarks.reshape(1, -1)
                
                # Apply scaling if available
                if self.scaler is not None:
                    landmarks_scaled = self.scaler.transform(landmarks_reshaped)
                    ai_prediction = self.model.predict(landmarks_scaled, verbose=0)[0][0]
                else:
                    ai_prediction = self.model.predict(landmarks_reshaped, verbose=0)[0][0]
                
                # If AI model seems reasonable, use it as primary with simple detection as backup
                if 0.0 <= ai_prediction <= 1.0:
                    # Use AI model as primary since it's now well-trained
                    ai_is_palm = ai_prediction > 0.5  # Use 0.5 threshold for well-trained model
                    
                    # Require BOTH AI and simple detection to agree for final decision
                    is_palm_combined = ai_is_palm and is_palm_simple
                    combined_confidence = (0.6 * ai_prediction) + (0.4 * confidence_simple)
                    
                    return is_palm_combined, combined_confidence
                else:
                    # AI model unreliable, use simple detection only
                    return is_palm_simple, confidence_simple
                    
            except Exception as e:
                # AI model failed, use simple detection
                return is_palm_simple, confidence_simple
                
        except Exception as e:
            # Complete fallback
            print(f"Error in palm detection: {e}")
            return False, 0.0
    
    def send_gesture_command(self, gesture):
        """Send gesture command to API server"""
        current_time = time.time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return
        
        self.last_gesture_time = current_time
        
        command = {
            "gesture": gesture,
            "timestamp": current_time,
            "action": "pause_play" if gesture == "palm" else "unknown"
        }
        
        print(f"🖐️ Gesture detected: {gesture} -> {command['action']}")
        
        # Send to API server
        try:
            response = requests.post(f"{self.api_url}/gesture", json=command, timeout=1)
            if response.status_code == 200:
                print("   ✅ Gesture sent successfully")
            else:
                print(f"   ❌ Failed to send gesture: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️ API server not responding: {e}")
    
    def run_camera(self):
        """Main camera loop with improved error handling"""
        # Find working camera
        cap, camera_id = self.find_working_camera()
        if cap is None:
            print("\n❌ Camera Error Solutions:")
            print("1. Check camera permissions in System Preferences")
            print("2. Close other apps using camera (Zoom, Skype, etc.)")
            print("3. Try demo mode instead: python test_demo.py")
            return False
        
        print(f"\n🎥 Starting gesture recognition with camera {camera_id}")
        print("📋 Instructions:")
        print("   • Show your palm clearly to the camera")
        print("   • Ensure good lighting")
        print("   • Keep hand 1-2 feet from camera")
        print("   • Press 'ESC' to exit")
        print("   • Press 'q' to quit")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Failed to read frame - camera disconnected?")
                    break
                
                frame_count += 1
                
                # Flip frame for natural interaction
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process every 3rd frame for performance
                if frame_count % 3 == 0:
                    results = self.hands.process(frame_rgb)
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Draw landmarks
                            self.mp_drawing.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                            )
                            
                            # Extract landmarks and detect palm
                            landmarks = self.extract_landmarks(hand_landmarks)
                            is_palm, confidence = self.detect_palm(landmarks)
                            
                            # Add to buffer for smoothing
                            self.gesture_buffer.append(is_palm)
                            
                            # Check if majority of recent detections are palm
                            if len(self.gesture_buffer) >= 3:  # Smaller buffer requirement
                                palm_count = sum(self.gesture_buffer)
                                if palm_count >= 2:  # More lenient majority vote
                                    print(f"🖐️ Sending palm gesture (buffer: {palm_count}/{len(self.gesture_buffer)})")
                                    self.send_gesture_command("palm")
                            
                            # Display prediction
                            gesture_text = f"Palm Detection: {confidence:.2f}"
                            color = (0, 255, 0) if is_palm else (0, 100, 255)
                            cv2.putText(frame, gesture_text, (10, 30), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            
                            # Debug: Show buffer status
                            buffer_text = f"Buffer: {sum(self.gesture_buffer)}/{len(self.gesture_buffer)}"
                            cv2.putText(frame, buffer_text, (10, 60), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
                            if is_palm:
                                cv2.putText(frame, "PALM DETECTED!", (10, 90), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                # Also print to console for debugging
                                print(f"Palm detected: confidence={confidence:.2f}, buffer={list(self.gesture_buffer)}")
                    else:
                        # Clear buffer if no hands detected
                        self.gesture_buffer.clear()
                        cv2.putText(frame, "Show your palm to the camera", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Display instructions
                cv2.putText(frame, "ESC/Q: Quit | Palm: Pause/Play", 
                           (10, frame.shape[0] - 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                cv2.imshow("Gesture-Controlled Media Player", frame)
                
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
    print("🎬 Gesture-Controlled Media Player")
    print("==================================")
    
    try:
        recognizer = ImprovedGestureRecognizer()
        success = recognizer.run_camera()
        
        if not success:
            print("\n💡 Try the demo mode instead:")
            print("   python test_demo.py")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\n💡 Try the demo mode instead:")
        print("   python test_demo.py")

if __name__ == "__main__":
    main()
