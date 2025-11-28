import cv2
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat

class GestureEngine:
    """
    PURPOSE:
    This class loads the AI models and processes the video frames.
    It determines WHICH gesture is being shown and draws the skeleton.
    """

    def __init__(self, gesture_model_path, hand_model_path):
        """
        Setup the AI models (Gesture Recognizer and Hand Landmarker).
        """
        # Configuration Variables
        self.min_confidence = 0.60    # Must be 60% sure to count
        self.confirmation_frames = 6  # Must hold gesture for 6 frames
        
        # Smoothing Variables (To prevent flickering)
        self.last_seen_gesture = "none"
        self.consecutive_frame_count = 0
        self.stable_gesture = "none"

        # 1. Load the Gesture Recognizer
        base_options_g = python.BaseOptions(model_asset_path=gesture_model_path)
        self.recognizer = vision.GestureRecognizer.create_from_options(
            vision.GestureRecognizerOptions(base_options=base_options_g, running_mode=vision.RunningMode.IMAGE)
        )

        # 2. Load the Hand Landmarker (for drawing the dots)
        base_options_h = python.BaseOptions(model_asset_path=hand_model_path)
        self.detector = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(base_options=base_options_h, num_hands=1, running_mode=vision.RunningMode.IMAGE)
        )

    def process_frame(self, frame):
        """
        PURPOSE:
        Takes a raw image from the camera, runs it through the AI, 
        and returns the results.
        
        RETURNS:
        - gesture_name: The cleaned-up, stable gesture (e.g., "Victory")
        - confidence: How sure the AI is (0.0 to 1.0)
        - landmarks: The list of hand points (for drawing)
        """
        
        # Convert OpenCV BGR format to MediaPipe RGB format
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb_image)

        # --- Step 1: Detect Hand Skeleton ---
        hand_result = self.detector.detect(mp_image)
        landmarks = None
        if hand_result.hand_landmarks:
            landmarks = hand_result.hand_landmarks[0] # Get the first hand

        # --- Step 2: Recognize Gesture ---
        gesture_result = self.recognizer.recognize(mp_image)
        
        current_gesture = "none"
        current_score = 0.0

        # Did we find any gestures?
        if gesture_result.gestures:
            top_prediction = gesture_result.gestures[0][0]
            current_score = top_prediction.score
            
            # FILTER: Is the score high enough?
            if current_score > self.min_confidence:
                current_gesture = top_prediction.category_name

        # --- Step 3: Smoothing (Debouncing) ---
        # This logic prevents the volume from jumping if the hand twitches.
        
        if current_gesture == self.last_seen_gesture:
            # If the gesture is the same as the last frame, add 1 to counter
            self.consecutive_frame_count += 1
        else:
            # If the hand moved/changed, reset the counter
            self.consecutive_frame_count = 0

        # If we have seen the same gesture for 6 frames, accept it as "Stable"
        if self.consecutive_frame_count >= self.confirmation_frames:
            self.stable_gesture = current_gesture

        # Remember this gesture for the next loop
        self.last_seen_gesture = current_gesture
        
        return self.stable_gesture, current_score, landmarks