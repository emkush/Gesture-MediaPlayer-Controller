import cv2
import time
import sys

# Import our custom classes
from camera_manager import CameraManager
from gesture_engine import GestureEngine
from controller import ActionController

#  SETTINGS
# Make sure these paths are correct!
GESTURE_MODEL_PATH = "./models/gesture_recognizer.task"
HAND_MODEL_PATH = "./models/hand_landmarker.task"

def main():
    """
    PURPOSE:
    This is the main loop of the program.
    1. Select Camera
    2. Load AI
    3. Loop: Capture -> Process -> Action -> Draw
    """

    # --- STEP 1: SETUP CAMERA ---
    print("Initializing Camera Manager...")
    cam_manager = CameraManager()
    selected_camera_index = cam_manager.select_camera()

    # --- STEP 2: LOAD AI ENGINE ---
    print("Loading AI Models... (This might take a second)")
    try:
        engine = GestureEngine(GESTURE_MODEL_PATH, HAND_MODEL_PATH)
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not load models.\n{e}")
        print("Check if the .task files are in the 'models' folder!")
        sys.exit()

    #  STEP 3: SETUP CONTROLLER 
    controller = ActionController()

    #  STEP 4: START VIDEO LOOP 
    cap = cv2.VideoCapture(selected_camera_index)
    
    # Used for FPS calculation
    prev_time = time.time()
    
    print("\nSystem Ready! Press 'q' to quit.")

    while True:
        # A. Read a frame from the camera
        success, frame = cap.read()
        if not success:
            print("Error: Camera disconnected.")
            break

        # B. Ask the Engine to process the frame
        # It returns the stable gesture, the score, and the hand dots
        gesture_name, confidence_score, landmarks = engine.process_frame(frame)

        # C. Perform Action (Keyboard Press)
        result = controller.execute_action(gesture_name)
        if result == "EXIT":
            print("Exit gesture detected. Goodbye!")
            break

        # D. Draw User Interface (Skeleton and Text)
        height, width, _ = frame.shape
        
        # Only draw if we see a hand
        if landmarks:
            # 1. Convert normalized points (0.0 to 1.0) to pixels
            x_coordinates = [int(p.x * width) for p in landmarks]
            y_coordinates = [int(p.y * height) for p in landmarks]
            
            # 2. Draw Bounding Box (Green Box)
            min_x, max_x = min(x_coordinates), max(x_coordinates)
            min_y, max_y = min(y_coordinates), max(y_coordinates)
            cv2.rectangle(frame, (min_x-20, min_y-20), (max_x+20, max_y+20), (0, 255, 0), 2)

            # 3. Draw Gesture Text Label
            # Show the gesture name and the confidence score (e.g., 0.95)
            label_text = f"{gesture_name} ({confidence_score:.2f})"
            cv2.putText(frame, label_text, (min_x, min_y - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 4. Draw the Skeleton Dots
            for point in landmarks:
                pixel_x = int(point.x * width)
                pixel_y = int(point.y * height)
                cv2.circle(frame, (pixel_x, pixel_y), 4, (0, 255, 255), -1)

        # E. Calculate and Draw FPS (Frames Per Second)
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

        # F. Show the window
        cv2.imshow("Gesture Control - Student Edition", frame)

        # G. Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup when the loop finishes
    cap.release()
    cv2.destroyAllWindows()

# This line runs the main function
if __name__ == "__main__":
    main()