#!/usr/bin/env python3
"""
MediaPipe Gesture Controller using gesture_recognizer.task file
This provides more accurate gesture recognition than the custom TensorFlow model.
"""

import cv2
import mediapipe as mp
import requests
import time
import os
from collections import deque

class MediaPipeGestureController:
    def __init__(self, task_path=None, api_url="http://localhost:8081"):
        """Initialize MediaPipe gesture recognizer with task file"""
        self.api_url = api_url
        self.task_path = task_path or "/Users/jethrohermawan/310/Project/models/gesture_recognizer.task"
        
        # Check if task file exists
        if not os.path.exists(self.task_path):
            raise FileNotFoundError(f"Task file not found: {self.task_path}")
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize gesture recognizer
        try:
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            
            base_options = python.BaseOptions(model_asset_path=self.task_path)
            options = vision.GestureRecognizerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.LIVE_STREAM,
                result_callback=self._gesture_callback,
                num_hands=1  # Detect one hand for better performance
            )
            self.recognizer = vision.GestureRecognizer.create_from_options(options)
            self.use_mediapipe_task = True
            print("✅ Using MediaPipe Task file for gesture recognition")
            
        except ImportError:
            print("⚠️ MediaPipe Tasks not available, falling back to basic hand tracking")
            self.use_mediapipe_task = False
            self._init_fallback_hands()
        except Exception as e:
            print(f"⚠️ MediaPipe Task file error: {e}")
            print("⚠️ Falling back to basic hand tracking with enhanced palm detection")
            self.use_mediapipe_task = False
            self._init_fallback_hands()
        
        # Gesture detection variables
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 2.0  # 2 seconds between gestures
        self.gesture_buffer = deque(maxlen=5)  # Buffer for smoothing
        
        # Video capture
        self.cap = None
        self.frame_count = 0
    
    def _init_fallback_hands(self):
        """Initialize basic MediaPipe hands as fallback"""
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        print("✅ Basic hand tracking initialized")
        
    def _gesture_callback(self, result, output_image, timestamp_ms):
        """Callback for MediaPipe gesture recognition"""
        if result.gestures:
            # Get the top gesture
            top_gesture = result.gestures[0][0]
            gesture_name = top_gesture.category_name
            confidence = top_gesture.score
            
            print(f"🎯 Detected: {gesture_name} (confidence: {confidence:.2f})")
            
            # Add to buffer for smoothing
            self.gesture_buffer.append((gesture_name, confidence))
            
            # Check if we have enough confident detections
            if len(self.gesture_buffer) >= 3:
                recent_gestures = list(self.gesture_buffer)[-3:]
                # Check if majority are the same gesture with good confidence
                palm_count = sum(1 for g, c in recent_gestures if 'palm' in g.lower() and c > 0.7)
                
                if palm_count >= 2:  # Majority vote
                    self._handle_palm_gesture(confidence)
    
    def _handle_palm_gesture(self, confidence):
        """Handle detected palm gesture"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return
        
        # Send gesture to API
        if self._send_gesture("palm", confidence):
            self.last_gesture = "palm"
            self.last_gesture_time = current_time
            print(f"🖐️ Palm gesture sent! (confidence: {confidence:.2f})")
    
    def _detect_palm_enhanced(self, hand_landmarks):
        """Enhanced palm detection with confidence scoring"""
        # Extract landmark positions
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append([lm.x, lm.y])
        
        # Key landmark indices
        wrist = landmarks[0]
        thumb_tip, thumb_pip = landmarks[4], landmarks[3]
        index_tip, index_pip = landmarks[8], landmarks[6]
        middle_tip, middle_pip = landmarks[12], landmarks[10]
        ring_tip, ring_pip = landmarks[16], landmarks[14]
        pinky_tip, pinky_pip = landmarks[20], landmarks[18]
        
        extended_count = 0
        confidence_factors = []
        
        # Check thumb extension (horizontal)
        thumb_extended = abs(thumb_tip[0] - wrist[0]) > abs(thumb_pip[0] - wrist[0]) + 0.05
        if thumb_extended:
            extended_count += 1
            confidence_factors.append(0.8)
        
        # Check other fingers (vertical)
        fingers = [(index_tip, index_pip), (middle_tip, middle_pip), 
                  (ring_tip, ring_pip), (pinky_tip, pinky_pip)]
        
        for tip, pip in fingers:
            # Finger is extended if tip is significantly above pip
            extension_amount = pip[1] - tip[1]  # Positive if tip is above pip
            if extension_amount > 0.05:  # Threshold for extension
                extended_count += 1
                confidence_factors.append(min(1.0, extension_amount * 10))  # Scale confidence
        
        # Calculate overall confidence
        base_confidence = extended_count / 5.0  # Base on finger count
        if confidence_factors:
            avg_quality = sum(confidence_factors) / len(confidence_factors)
            confidence = (base_confidence + avg_quality) / 2.0
        else:
            confidence = base_confidence
        
        # Palm detected if 4+ fingers extended with good confidence
        is_palm = extended_count >= 4 and confidence > 0.6
        
        return is_palm, confidence
        
    def _detect_palm_simple(self, hand_landmarks):
        """Simple fallback palm detection"""
        is_palm, confidence = self._detect_palm_enhanced(hand_landmarks)
        return is_palm
    
    def _send_gesture(self, gesture, confidence):
        """Send gesture to API server"""
        try:
            response = requests.post(
                f"{self.api_url}/gesture",
                json={
                    "gesture": gesture,
                    "confidence": float(confidence),
                    "timestamp": time.time()
                },
                timeout=1
            )
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"❌ Failed to send gesture: {e}")
            return False
    
    def test_api_connection(self):
        """Test if API server is accessible"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=2)
            if response.status_code == 200:
                print("✅ API server connection successful")
                return True
        except requests.RequestException:
            pass
        
        print("❌ Cannot connect to API server. Make sure gesture_api_server.py is running")
        return False
    
    def start_detection(self):
        """Start gesture detection with webcam"""
        if not self.test_api_connection():
            return False
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Cannot access camera")
            return False
        
        print("🎬 MediaPipe Gesture Detection Started!")
        print("📋 Instructions:")
        print("   🖐️  Show palm to pause/play media")
        print("   ⌨️  Press 'q' or ESC to quit")
        print("   🔄 Gesture cooldown: 2 seconds")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to grab camera frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                self.frame_count += 1
                
                if self.use_mediapipe_task:
                    # Use MediaPipe Task for gesture recognition
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                    timestamp_ms = int(time.time() * 1000)
                    self.recognizer.recognize_async(mp_image, timestamp_ms)
                    
                else:
                    # Fallback to basic hand tracking
                    results = self.hands.process(rgb_frame)
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Draw hand landmarks
                            self.mp_drawing.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                            )
                            
                            # Enhanced palm detection for fallback mode
                            is_palm, confidence = self._detect_palm_enhanced(hand_landmarks)
                            
                            # Add to buffer for smoothing
                            self.gesture_buffer.append(("palm" if is_palm else "other", confidence))
                            
                            # Check buffer for consistent palm detection
                            if len(self.gesture_buffer) >= 3:
                                recent = list(self.gesture_buffer)[-3:]
                                palm_count = sum(1 for g, c in recent if g == "palm" and c > 0.6)
                                if palm_count >= 2:
                                    self._handle_palm_gesture(confidence)
                            
                            # Visual feedback
                            if is_palm:
                                cv2.putText(frame, f"PALM DETECTED! ({confidence:.2f})", 
                                          (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display status
                status_text = f"Gesture Controller (Frame: {self.frame_count})"
                if self.last_gesture:
                    time_since = time.time() - self.last_gesture_time
                    status_text += f" | Last: {self.last_gesture} ({time_since:.1f}s ago)"
                
                cv2.putText(frame, status_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Show recent buffer status
                if self.gesture_buffer:
                    recent = list(self.gesture_buffer)[-3:]
                    buffer_text = f"Buffer: {[g for g, c in recent]}"
                    cv2.putText(frame, buffer_text, (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                
                cv2.imshow('MediaPipe Gesture Control', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    break
                elif key == ord('t'):  # Test gesture
                    print("🧪 Manual test gesture")
                    self._send_gesture("palm", 0.9)
        
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
        
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        if hasattr(self, 'hands') and not self.use_mediapipe_task:
            self.hands.close()
        
        print("🧹 Cleanup completed")

def main():
    """Main function to run the MediaPipe gesture controller"""
    print("🎬 MediaPipe Gesture Controller")
    print("=" * 50)
    
    # Initialize controller
    try:
        controller = MediaPipeGestureController()
        controller.start_detection()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the gesture_recognizer.task file is in the models folder")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
