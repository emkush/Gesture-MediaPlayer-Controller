#!/usr/bin/env python3
"""
Debug script to investigate palm detection issues.
This will help identify why all gestures are being detected as "palm".
"""

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import os

class PalmDetectionDebugger:
    def __init__(self):
        """Initialize debugger with model and MediaPipe"""
        # Suppress TensorFlow warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel('ERROR')
        
        # Load model
        try:
            self.model = tf.keras.models.load_model("palm_gesture_model.h5", compile=False)
            self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            self.model = None
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.4
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def extract_landmarks(self, hand_landmarks):
        """Extract hand landmarks as feature vector"""
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
        return np.array(landmarks)
    
    def analyze_hand_geometry(self, landmarks):
        """Analyze hand geometry for debugging"""
        points = landmarks.reshape(21, 3)
        
        # Key landmarks
        wrist = points[0]
        thumb_tip = points[4]
        index_tip = points[8]
        middle_tip = points[12]
        ring_tip = points[16]
        pinky_tip = points[20]
        
        # Finger MCPs (base of fingers)
        thumb_mcp = points[1]
        index_mcp = points[5]
        middle_mcp = points[9]
        ring_mcp = points[13]
        pinky_mcp = points[17]
        
        analysis = {
            'wrist_y': wrist[1],
            'fingertips': {
                'thumb': {'y': thumb_tip[1], 'extended': thumb_tip[1] < thumb_mcp[1]},
                'index': {'y': index_tip[1], 'extended': index_tip[1] < index_mcp[1]},
                'middle': {'y': middle_tip[1], 'extended': middle_tip[1] < middle_mcp[1]},
                'ring': {'y': ring_tip[1], 'extended': ring_tip[1] < ring_mcp[1]},
                'pinky': {'y': pinky_tip[1], 'extended': pinky_tip[1] < pinky_mcp[1]}
            }
        }
        
        # Count extended fingers
        extended_count = sum(1 for finger in analysis['fingertips'].values() if finger['extended'])
        analysis['extended_fingers'] = extended_count
        
        return analysis
    
    def detect_palm_simple(self, landmarks):
        """Original simple detection with debug info"""
        try:
            points = landmarks.reshape(21, 3)
            fingertips = [4, 8, 12, 16, 20]  
            wrist = points[0]
            
            extended_fingers = 0
            finger_analysis = {}
            
            # Check each finger
            for i, tip_idx in enumerate(fingertips[1:], 1):  # Skip thumb
                tip = points[tip_idx]
                is_extended = tip[1] < wrist[1] - 0.05
                if is_extended:
                    extended_fingers += 1
                finger_analysis[f'finger_{i}'] = {
                    'tip_y': tip[1],
                    'wrist_y': wrist[1],
                    'diff': wrist[1] - tip[1],
                    'extended': is_extended
                }
            
            # Check thumb
            thumb_tip = points[4]
            thumb_extended = abs(thumb_tip[0] - wrist[0]) > 0.08
            if thumb_extended:
                extended_fingers += 0.5
            
            finger_analysis['thumb'] = {
                'tip_x': thumb_tip[0],
                'wrist_x': wrist[0],
                'diff': abs(thumb_tip[0] - wrist[0]),
                'extended': thumb_extended
            }
            
            confidence = min(1.0, extended_fingers / 3.0)
            is_palm = extended_fingers >= 2
            
            return is_palm, confidence, finger_analysis, extended_fingers
            
        except Exception as e:
            print(f"Error in simple detection: {e}")
            return False, 0.0, {}, 0
    
    def debug_detection(self, landmarks):
        """Debug both AI and simple detection"""
        debug_info = {}
        
        # AI Model prediction
        if self.model is not None:
            try:
                landmarks_reshaped = landmarks.reshape(1, -1)
                ai_prediction = self.model.predict(landmarks_reshaped, verbose=0)[0][0]
                debug_info['ai_prediction'] = ai_prediction
                debug_info['ai_palm'] = ai_prediction > 0.4
            except Exception as e:
                debug_info['ai_error'] = str(e)
        
        # Simple detection
        is_palm_simple, conf_simple, finger_analysis, extended_count = self.detect_palm_simple(landmarks)
        debug_info['simple_detection'] = {
            'is_palm': is_palm_simple,
            'confidence': conf_simple,
            'extended_fingers': extended_count,
            'finger_details': finger_analysis
        }
        
        # Hand geometry analysis
        debug_info['geometry'] = self.analyze_hand_geometry(landmarks)
        
        return debug_info
    
    def run_debug_camera(self):
        """Run camera with detailed debugging"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot open camera")
            return
        
        print("🔍 Palm Detection Debug Mode")
        print("Show different hand gestures to see detection results")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Extract landmarks and debug
                    landmarks = self.extract_landmarks(hand_landmarks)
                    debug_info = self.debug_detection(landmarks)
                    
                    # Print detailed debug info
                    print("\n" + "="*50)
                    if 'ai_prediction' in debug_info:
                        print(f"AI Prediction: {debug_info['ai_prediction']:.3f} -> {'PALM' if debug_info['ai_palm'] else 'NOT PALM'}")
                    
                    simple = debug_info['simple_detection']
                    print(f"Simple Detection: {simple['confidence']:.3f} -> {'PALM' if simple['is_palm'] else 'NOT PALM'}")
                    print(f"Extended Fingers: {simple['extended_fingers']}")
                    
                    # Show finger details
                    for finger, details in simple['finger_details'].items():
                        if finger == 'thumb':
                            print(f"  {finger}: diff={details['diff']:.3f} -> {'EXTENDED' if details['extended'] else 'folded'}")
                        else:
                            print(f"  {finger}: diff={details['diff']:.3f} -> {'EXTENDED' if details['extended'] else 'folded'}")
                    
                    # Display on screen
                    y_offset = 30
                    if 'ai_prediction' in debug_info:
                        ai_text = f"AI: {debug_info['ai_prediction']:.3f} ({'PALM' if debug_info['ai_palm'] else 'NOT PALM'})"
                        cv2.putText(frame, ai_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if debug_info['ai_palm'] else (0, 0, 255), 2)
                        y_offset += 30
                    
                    simple_text = f"Simple: {simple['confidence']:.3f} ({'PALM' if simple['is_palm'] else 'NOT PALM'})"
                    cv2.putText(frame, simple_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if simple['is_palm'] else (0, 0, 255), 2)
                    y_offset += 30
                    
                    cv2.putText(frame, f"Extended Fingers: {simple['extended_fingers']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            else:
                cv2.putText(frame, "Show your hand to the camera", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Palm Detection Debug", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    debugger = PalmDetectionDebugger()
    debugger.run_debug_camera()

if __name__ == "__main__":
    main()
