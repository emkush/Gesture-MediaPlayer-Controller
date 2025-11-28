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
