import time
from collections import deque
# If you are using a MediaPipe .task file for dynamics, import this:
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class DynamicGestureProcessor:
    """
    PURPOSE:
    This class handles "Motion-Based" gestures (e.g., Waving, Double Swipe).
    Unlike static gestures (shapes), these require analyzing a history of 
    movements over time.
    """

    def __init__(self, model_path=None):
        """
        Setup the processor.
        
        Args:
            model_path (str): Path to a .task file trained on video data (optional).
        """
        # 1. Configuration
        self.model_path = model_path
        
        # 2. History Buffer
        # We store the last 30 frames of hand positions to analyze movement.
        # 'deque' is a list that automatically deletes old items when full.
        self.history_length = 30 
        self.landmark_history = deque(maxlen=self.history_length)

        # 3. Load Model (Placeholder)
        self.model = self._load_dynamic_model()

    def _load_dynamic_model(self):
        """
        INTERNAL: Loads the MediaPipe task file specifically for 
        continuous video recognition, if you have one.
        """
        if not self.model_path:
            return None
        
        print(f"Loading Dynamic Model from: {self.model_path}")
        
        # TODO:  IMPLEMENTATION
        # Create the MediaPipe GestureRecognizer in VIDEO mode here.
        # Example logic:
        # base_options = python.BaseOptions(model_asset_path=self.model_path)
        # options = vision.GestureRecognizerOptions(
        #     base_options=base_options,
        #     running_mode=vision.RunningMode.VIDEO # <--- Note: VIDEO mode
        # )
        # return vision.GestureRecognizer.create_from_options(options)
        
        return None 

    def process_frame(self, landmarks, timestamp_ms):
        """
        PURPOSE:
        Feeds new data into the processor and returns a dynamic gesture name.

        Args:
            landmarks: The hand landmarks list from the main engine.
            timestamp_ms: The current video timestamp (needed for .task video mode).
            
        Returns:
            str: The detected dynamic gesture (e.g., "Wave_Left" or "None").
        """
        
        # Step 1: Add current data to history
        if landmarks:
            self.landmark_history.append(landmarks)
        else:
            # If hand is lost, we might want to clear history or keep waiting
            pass

        # Step 2: Option A - Use the .task Model (AI Approach)
        if self.model:
            # TODO: Feed the image/timestamp to self.model.recognize_for_video()
            # result = self.model.recognize_for_video(mp_image, timestamp_ms)
            # return result
            pass

        # Step 3: Option B - Manual Logic (Code Approach)
        # If we don't have a model, we calculate movement manually.
        gesture = self._calculate_manual_dynamics()
        
        return gesture

    def _calculate_manual_dynamics(self):
        """
        INTERNAL: Checks the history buffer for specific movement patterns.
        Example: Is the hand moving consistently to the left?
        """
        if len(self.landmark_history) < 5:
            return "None"

        # TODO: IMPLEMENTATION
        # Example Logic:
        # 1. Get X coordinate of the wrist (point 0) from 5 frames ago.
        # 2. Get X coordinate of the wrist NOW.
        # 3. If (old_x - new_x) > 0.5: Return "Swipe Left"
        
        return "None"
    

    """
    TO DO after completing dynamic gestures. 
    
    FOR gesture_engine:

        # 1. Import it
        from dynamic_engine import DynamicGestureProcessor

        # 2. Initialize it
        dynamic_engine = DynamicGestureProcessor(model_path="./models/dynamic.task") 

        # 3. Inside the While Loop
        # ... after getting landmarks ...
        dynamic_gesture = dynamic_engine.process_frame(landmarks, int(time.time() * 1000))

        if dynamic_gesture != "None":
            print(f"DYNAMIC GESTURE DETECTED: {dynamic_gesture}")
            # Trigger action...
            
    """