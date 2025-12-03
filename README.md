# Gesture Recognition & Control
**CMPT 310 - Fall 2025 - Simon Fraser University**

A hybrid AI system that blends motion detection and gesture recognition for touch-free video player control.

---

## Demo Video
**Watch the system in action:**
[https://drive.google.com/file/d/1pD-rEtYHZJViCPVyhJh_qDc6BmKe7lJT/view?usp=sharing](https://drive.google.com/file/d/1pD-rEtYHZJViCPVyhJh_qDc6BmKe7lJT/view?usp=sharing)

---

## Overview
This project is a **hybrid hand gesture recognition system** designed for real-time media control. It moves beyond simple classification by merging two distinct approaches:

1. **Static Gesture Recognition:** Uses a custom-trained **MediaPipe Model Maker** (`.task` model) to identify fixed hand shapes (e.g., Thumbs Up, Fist).
2. **Dynamic Logic:** Uses temporal smoothing and logic buffers to stabilize inputs and prevent "flickering," ensuring that a gesture is only triggered when it is intentional.

The architecture is built on a modular **Model-View-Controller (MVC)** pattern, separating hardware abstraction, AI processing, and action execution.

---

## Features

| Type | Examples | Description |
| :--- | :--- | :--- |
| **Static Gestures** | Play, Pause, Volume Control | Trained specific hand shapes recognized via the `.task` model. Includes confidence thresholding (>60%). |
| **Dynamic Stabilization** | Debouncing / Smoothing | Implements logic to track gesture consistency over time (6 frames) to prevent accidental triggers. |
| **Cross-Platform** | Camera Selection | Custom hardware manager that auto-detects inputs on macOS, Windows, and Linux. |
| **Media Control** | System-Level Shortcuts | Controls global system volume and media playback via keyboard simulation. |

---

## Project Structure

```text
Gesture_Project/
├── models/
│   ├── gesture_recognizer.task   # Custom trained classification model
│   ├── hand_landmarker.task      # Standard MediaPipe landmark detection
│   └── Main/
│       ├── main.py               # Application Entry Point (View)
│       ├── camera_manager.py     # Hardware Abstraction Layer
│       ├── gesture_engine.py     # AI Processing & Smoothing Logic (Model)
│       └── action_controller.py  # Keyboard/Action Execution (Controller)
├── requirements.txt              # Dependency list
└── README.md                     # Documentation

```
## Installation & Setup

### 1. Prerequisites
* Python version between 3.9 and 3.11
* Webcam (Built-in or USB (Bluetooth)

### 2. Dependencies
Install the required Python libraries:

```bash
pip install opencv-python mediapipe pynput
(Optional for Windows users to see device names):Bashpip install pygrabber
```
### 3. How to Run 
Navigate to the source folder and execute the main script: 
```bash
cd models/Main
python main.py
```
Follow the on-screen prompts to select your camera input.


> ** Note:** Ensure your file paths in the code point correctly to the `.task` models (e.g., `../gesture_recognizer.task`) since the scripts are inside a subfolder.

---

## Instructions
### **Step 1: Install Extension**
   ```
   1. Open Chrome → chrome://extensions/
   2. Enable "Developer mode" (top right toggle)
   3. Click "Load unpacked"
   4. Select the web extension folder
   ```

### **Step 2: Verify Installation**
   - Look for "Gestured-Controlled Media Player" in extensions list
   - Should have a 🎬 icon in toolbar

### **Step 3: Start the Backend**
```bash
./start.sh                    # Automatic (camera required)
```

### **Step 4: Prepare Browser**
1. Open YouTube: https://youtube.com/watch?v=dQw4w9WgXcQ
2. Or Netflix: https://netflix.com (any video)

### **Step 5: Activate Extension**
1. Click the 🎬 extension icon in Chrome toolbar
2. Click "Start Detection" button
3. Status indicator should turn green

### **Step 6: Use Gestures**
- **With Camera:** Show palm to webcam → pause/play
- **Demo Mode:** Automatic gestures every 5 seconds

## Controls Reference

The system maps the following gestures to system actions:

| Gesture | Action | Key Mapping |
| :--- | :--- | :--- |
| **Thumbs Up** | Play / Pause | Spacebar |
| **Fist** | Volume Down | Media Volume Down |
| **Victory (V)** | Volume Up | Media Volume Up |
| **Swipe Left** | Rewind | 30 sec rewind |
| **Swipe Right** | Forward | 30sec fast forward |
| **Open Palm** | pause | spacebar |

---

## Troubleshooting

### 1. Camera Selection Issues
If the camera list does not display names correctly, or if the selected index fails, try selecting index **0** or **1** manually. The `camera_manager.py` includes specific fallback logic for macOS permissions.

### 2. "Ghost" Inputs
If volume changes uncontrollably, increase the `CONFIRMATION_FRAMES` or `MIN_CONFIDENCE` variables in `gesture_engine.py` to require stricter gesture adherence.

### 3. Permissions (macOS)
To control the keyboard, the terminal (VS Code, Terminal.app, or iTerm) must be granted **Accessibility** permissions:
* Go to: **System Settings > Privacy & Security > Accessibility**
* Ensure your terminal application is checked.
