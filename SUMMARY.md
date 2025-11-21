# 🎬 PROJECT - TEAM GUIDE

```
📦 gesture-media-player/
├── 📄 README.md                    # Project overview & instructions
├── 📄 run.py                      # 🚀 MAIN LAUNCHER (START HERE)
├── 📄 start.py                    # Quick start script
├── 📂 src/                        # ⭐ CORE APPLICATION CODE
│   ├── 📄 gesture_api_server.py   # HTTP API server for browser communication
│   ├── 📄 gesture_recognition.py  # Main camera gesture detection
│   └── 📄 model_training.py       # AI model training & retraining
├── 📂 models/                     # 🤖 AI MODELS & TRAINING
│   └── 📄 train_palm_model.py     # Model training utilities
├── 📂 tests/                      # 🧪 TESTING & DEBUGGING
│   ├── 📄 test_gestures.py        # Test camera gesture detection
│   ├── 📄 test_extension.py       # Test browser extension
│   └── 📄 debug_detection.py      # Debug palm detection issues
├── 📂 web-extension/              # 🌐 CHROME EXTENSION
│   ├── 📄 manifest.json          # Extension configuration
│   ├── 📄 background.js           # Background service worker
│   ├── 📄 content.js              # Content script for media control
│   ├── 📄 popup.html             # Extension popup interface
│   └── 📄 popup.js               # Popup functionality
├── 📂 docs/                      # 📚 DOCUMENTATION
│   ├── 📄 SETUP.md               # Setup instructions
│   ├── 📄 USAGE.md               # Usage guide
│   └── 📄 TROUBLESHOOTING.md     # Common issues & solutions
├── 📂 datasets/                  # 📊 TRAINING DATA (unchanged)
├── 📄 palm_gesture_model.h5      # Trained AI model
└── 📄 palm_scaler.pkl            # Feature scaling for AI model
```

## 🚀 HOW TO USE (FOR TEAM MEMBERS)

### Option 1: Interactive Launcher (Recommended)
```bash
python run.py
```
Choose from menu options 1-6 for different functions.

### Option 2: Quick Start
```bash
python start.py
```
Automatically starts API server + gesture recognition.

### Option 3: Manual Components
```bash
# Start API server
python src/gesture_api_server.py

# In another terminal, start gesture recognition
python src/gesture_recognition.py
```

## 🎯 KEY IMPROVEMENTS FOR TEAM

### ✅ **Clear Entry Points**
- **`run.py`** - Main interactive launcher
- **`start.py`** - Quick automatic start
- No confusion about which file to run first

### ✅ **Logical Organization**
- **`src/`** - Core application logic
- **`tests/`** - All testing tools
- **`docs/`** - All documentation
- **`models/`** - AI model files
- **`web-extension/`** - Browser extension

### ✅ **Better File Names**
- `gesture_recognition.py` (was `improved_gesture_controller.py`)
- `test_gestures.py` (was `simple_test.py`)
- `debug_detection.py` (was `debug_palm_detection.py`)

### ✅ **Updated References**
- `run.py` launcher updated to use new paths
- All import paths corrected
- Documentation updated

## 👥 TEAM WORKFLOW

### 🔧 **For Developers**
1. **Core features**: Edit files in `src/`
2. **Testing**: Use tools in `tests/`
3. **Documentation**: Update files in `docs/`

### 🧪 **For Testers**
1. **Quick testing**: `python run.py` → Option 2
2. **Extension testing**: `python run.py` → Option 1
3. **Debug issues**: `python run.py` → Option 4

### 📖 **For New Team Members**
1. **Start here**: Read `README.md`
2. **Setup**: Follow `docs/SETUP.md`
3. **Run**: Use `python run.py`
