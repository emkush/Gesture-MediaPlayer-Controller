# 🎬 CMPT 310 Gesture-Controlled Media Player

**Advanced AI System: Hand Gesture Recognition & Browser Media Control**

<p align="center">
  <b>CMPT 310 · Fall 2025 · SFU</b><br>
  <i>Hybrid AI system that blends motion detection and gesture recognition for video players.</i>
</p>

---

## 📋 Overview

This project i## 🙏 Acknowledgments

- **CMPT 310 Course Team** for project guidance
- **Google MediaPipe** for hand tracking technology
- **TensorFlow** for machine learning framework
- **Chrome Extensions API** for web integration
- **SFU Computer Science** for educational support

---

**Ready to control your media with gestures? Run `python run.py` to get started!** 🎬✋

### 🎯 Project Goals Achieved

This combined system demonstrates:
- ✅ **Multi-modal AI**: Static + Dynamic gesture recognition
- ✅ **Real-world Application**: Browser media control
- ✅ **Scalable Architecture**: Extensible to new gestures/sites
- ✅ **User-friendly Interface**: Simple installation and usage
- ✅ **Educational Value**: Comprehensive AI/ML implementation

**CMPT 310 Fall 2025 - Advanced AI Techniques in Action!** 🚀prehensive hand gesture recognition system** that combines:
- 🤚 **Static gesture recognition** via **MediaPipe Model Maker** (`.task` model)
- 👋 **Dynamic motion detection** using real-time hand landmark tracking
- 🌐 **Browser integration** through Chrome extension
- 🎥 **Real-time media control** for YouTube & Netflix

The system merges two powerful approaches:
1. **Gesture-MediaPlayer-Controller-main**: Core gesture recognition models and training
2. **Project**: Web extension implementation and MediaPipe integration

## ✨ Features

|  Type | Example |  Description |
|----------|-------------|----------------|
| 🖐 **Static Gestures** | 👍 Play · ✋ Pause · 👊 Stop | Trained using **MediaPipe Model Maker** (`.task` model) |
| 👋 **Dynamic Gestures** | Wave Left → ⏮️ Previous · Wave Right → ⏭️ Next | Real-time **motion tracking** of wrist x-direction |
| 🔊 **Custom Gestures** | Swipe Up/Down for Volume · Double Swipe Left = Skip 30s | Hand motion logic with temporal tracking |
| 🤟 **ASL Mode** | A, B, C... | Recognize ASL letters via **ASL Alphabet Dataset** |
| 🌐 **Browser Control** | YouTube & Netflix integration | Chrome extension with seamless media control |

## 🚀 Quick Start

```bash
# Single command to get started
python run.py
```

Choose **Option 1** for MediaPipe gesture control using your `.task` file!

## ✨ Features

- **🤖 MediaPipe Task Recognition**: Uses your custom `gesture_recognizer.task` for high accuracy
- **🎯 AI-Powered Detection**: Custom trained model for palm gesture recognition  
- **📹 Real-time Processing**: Fast MediaPipe-based hand tracking
- **🌐 Browser Integration**: Chrome extension for seamless control
- **🎥 Multi-platform**: Works with YouTube & Netflix

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- Webcam
- macOS/Linux/Windows

## 🛠️ Installation

### 1. Set up Python Environment

```bash
# Navigate to project directory
for example:
cd /Users/jethrohermawan/310/Project

# Activate virtual environment (already created)
source myvenv/bin/activate

# Install required packages (already done)
pip install opencv-python mediapipe tensorflow numpy scikit-learn requests
```

### 2. Install Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `web-extension/` folder from this project
5. The extension should now appear in your extensions list

### 3. MediaPipe Task File
Your `gesture_recognizer.task` file is already in the `models/` folder and ready to use!

## 🎮 Usage Options

| Option | Description | Best For |
|--------|-------------|----------|
| **1. MediaPipe Control** | 🤖 Uses your `.task` file | **Recommended** - Most accurate |
| **2. AI Recognition** | 🎯 Custom TensorFlow model | Alternative method |
| **3. Manual Camera** | 📹 Press 'p' to trigger | Testing setup |
| **4. Extension Test** | 🧪 No camera needed | Debugging browser integration |

## 📋 How It Works

1. **Start launcher**: `python run.py`
2. **Choose MediaPipe option**: Option 1
3. **Open YouTube/Netflix**: Navigate to a video page
4. **Click extension**: Click the � icon → "Start Detection"  
5. **Show palm**: 🖐️ Palm gesture pauses/plays video!

### 🚀 **EASIEST WAY - Use the Launcher:**

```bash
# Start here - interactive menu with all options
python run.py
```

### 📋 **Manual Steps:**

#### **Step 1: Start Backend** (always required)
```bash
python gesture_api_server.py  # Keep this running
```

#### **Step 2: Choose Testing Method:**

**Option A: Test Extension (no camera)**
```bash
python tests/quick_test.py
```

**Option B: Manual Camera Control**  
```bash
python scripts/simple_test.py  # Press 'p' to trigger gestures
```

**Option C: Full AI Recognition**
```bash
python scripts/improved_gesture_controller.py  # Automatic palm detection
```

### 🔧 **Browser Setup:**
1. Install extension: `chrome://extensions/` → Load unpacked → `web-extension/` folder
2. Open YouTube/Netflix VIDEO page (not homepage!)
3. Click 🎬 extension → "Start Detection" → GREEN status

## 🖐️ Supported Gestures

| Gesture | Action | Status |
|---------|--------|--------|
| 🖐️ Palm | Play/Pause | ✅ Working |
| 👍 Thumbs Up | Volume Up | 🚧 Coming Soon |
| 👎 Thumbs Down | Volume Down | 🚧 Coming Soon |
| ✌️ Peace Sign | Skip Forward | 🚧 Coming Soon |

## 🏗️ Project Structure

```
📦 CMPT310-Project/
├── 🚀 run.py                          # Main launcher (START HERE)
├── 📂 models/                         # AI Models & Training
│   ├── gesture_recognizer.task        # MediaPipe trained model
│   ├── gesture_recognizer.ipynb       # Training notebook
│   └── display_test.py               # Model testing utilities
├── 📂 src/                           # Core Application
│   ├── mediapipe_gesture_controller.py # MediaPipe controller
│   ├── gesture_recognition.py         # AI-based recognition  
│   └── gesture_api_server.py         # Backend server
├── 📂 scripts/                       # Scripts & Controllers
│   ├── improved_gesture_controller.py # Enhanced gesture control
│   └── test.py                       # Basic testing
├── 📂 set_data/                      # Training Datasets
│   ├── asl_alphabet/                 # ASL training data
│   └── Hagrid_data/                  # HaGRID gesture dataset
├── 📂 tests/                         # Testing Suite
│   ├── test_mediapipe_task.py        # Test .task file
│   ├── test_gestures.py              # Camera testing
│   └── test_extension.py             # Extension testing
├── 📂 web-extension/                 # Chrome Extension
│   ├── manifest.json                 # Extension configuration
│   ├── background.js                 # Background service worker
│   ├── content.js                    # Content script for media sites
│   └── popup.html/.js                # Extension interface
├── 📂 docs/                          # Documentation
│   ├── SETUP.md                      # Setup instructions
│   ├── USAGE.md                      # Usage guidelines
│   └── TROUBLESHOOTING.md           # Troubleshooting guide
├── 📂 datasets/                      # Additional Training Data
│   ├── ann_subsample/                # Annotated samples
│   ├── ann_test/                     # Test annotations
│   └── ann_train_val/                # Training/validation data
└── 📂 mediapipe/                     # MediaPipe Integration
    └── [MediaPipe source files]      # MediaPipe implementation
```

## 🔧 System Architecture

1. **Gesture Recognition**: Uses MediaPipe to detect hand landmarks from webcam
2. **AI Classification**: TensorFlow model classifies gestures (palm vs others)
3. **Communication**: HTTP API server facilitates Python ↔ Extension communication
4. **Media Control**: Content scripts inject media controls into web pages

### Model Training & Development

The project includes comprehensive training capabilities:
- **MediaPipe Model Maker**: For static gesture recognition
- **Custom TensorFlow Models**: For specialized gesture detection
- **ASL Integration**: For sign language recognition
- **Dynamic Gesture Detection**: Using temporal motion analysis

## 🎯 Supported Websites

- ✅ **YouTube** (`youtube.com`) - Full support
- ✅ **Netflix** (`netflix.com`) - Full support
- 🚧 **Other sites** - Can be added by modifying `content.js`

## 🐛 Troubleshooting

### Extension Not Responding (Most Common Issue)

**Problem:** Extension shows green status but nothing happens when showing palm

**Solution - Step by Step:**
```bash
# 1. Use the launcher for easy diagnosis
python run.py  # Choose option 4 for debugging

# 2. Or run manually:
python tests/debug_extension.py

# 3. Test extension manually:
python tests/quick_test.py
```

**Follow this checklist:**
1. ✅ API server running (`curl http://localhost:8081/status`)
2. ✅ Extension installed and enabled in `chrome://extensions/`
3. ✅ On YouTube/Netflix VIDEO page (not homepage)
4. ✅ Clicked "Start Detection" → status indicator GREEN
5. ✅ Test manual gesture: `python quick_test.py`

### Camera/Gesture Recognition Issues
```bash
# Use simple camera test first
python scripts/simple_test.py

# Or use the launcher
python run.py  # Choose option 2

# Check camera permissions: System Preferences → Privacy → Camera
# Close other camera apps (Zoom, Teams, etc.)
```

### Extension Debug Steps
1. **Check Extension Console:**
   - Right-click extension icon → "Inspect popup"
   - Look for error messages in Console tab

2. **Check Content Script:**
   - F12 on YouTube/Netflix page
   - Console should show: "Gesture-controlled media player loaded!"

3. **Manual Test:**
   - Run `python tests/quick_test.py`
   - Video should pause/play when gestures are sent

### Common Fixes
- **Refresh** the YouTube/Netflix page after starting detection
- **Restart** Chrome extension (disable/enable)
- **Check** you're on a video page with actual video content
- **Verify** extension permissions in Chrome settings

## 🔧 Configuration

### Gesture Sensitivity
Edit `gesture_controller.py`:
```python
self.palm_threshold = 0.7  # Lower = more sensitive
self.gesture_cooldown = 2.0  # Seconds between gestures
```

### API Server Port
Edit `gesture_api_server.py` and `gesture_controller.py`:
```python
port = 8081  # Change if port conflicts
```

## 🚀 Development

### Adding New Gestures

1. **Collect Training Data**: Add gesture annotations to `datasets/`
2. **Update Model**: Modify `palm_model.py` to include new gestures
3. **Update Recognition**: Add detection logic in `gesture_controller.py`
4. **Update Extension**: Add new actions in `content.js`

### Adding New Websites

1. **Update Manifest**: Add site permissions to `manifest.json`
2. **Update Content Script**: Add selectors for new site in `content.js`
3. **Test Integration**: Verify media controls work on new site

## 📊 Performance

- **Latency**: ~200-500ms from gesture to action
- **Accuracy**: Depends on lighting and hand positioning
- **Resource Usage**: Moderate CPU usage for video processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

## 📄 License

This project is for educational purposes. MediaPipe and TensorFlow are used under their respective licenses.

## � Tips

- **Best results**: Good lighting, clear palm gesture
- **Gesture cooldown**: 2 seconds between detections  
- **Troubleshooting**: Run `python tests/test_mediapipe_task.py`
- **Multiple options**: Try different recognition methods if one doesn't work

The system now supports your MediaPipe task file for superior gesture recognition accuracy! 🎯

## �🙏 Acknowledgments

- Google MediaPipe for hand tracking
- TensorFlow for machine learning
- Chrome Extensions API for web integration

---

**Ready to control your media with gestures? Run `python run.py` to get started!** 🎬✋
