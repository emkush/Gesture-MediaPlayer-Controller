import cv2
import mediapipe as mp
import csv
import time
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

GESTURES = ["swipe_left", "swipe_right", "swipe_up", "swipe_down"]
DATA_DIR = "dataset"
os.makedirs(DATA_DIR, exist_ok=True)

SEQUENCE_LENGTH = 20  # number of frames per gesture sample

def record_gesture(gesture_name):
    cap = cv2.VideoCapture(0)
    sequence = []
    print(f"Recording {gesture_name}. Press 'r' to start recording each sample, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Recording", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # record one sample
            print("Recording sequence...")
            sequence = []
            for _ in range(SEQUENCE_LENGTH):
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    frame_data = []
                    for lm in hand_landmarks.landmark:
                        frame_data += [lm.x, lm.y, lm.z]
                    sequence.append(frame_data)
                time.sleep(0.05)  # 20 fps roughly
            # Save
            csv_path = os.path.join(DATA_DIR, f"{gesture_name}_{int(time.time())}.csv")
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(sequence)
            print(f"Saved {csv_path}")
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

for gesture in GESTURES:
    record_gesture(gesture)