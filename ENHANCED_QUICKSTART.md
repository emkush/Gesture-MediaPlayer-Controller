# 🚀 Enhanced CMPT310 Gesture Controller - Quick Start Guide

## 🎯 What's New?

This enhanced version combines the full gesture recognition capabilities from `Gesture-MediaPlayer-Controller-main` with the web extension from `Project`, providing:

### 🖐️ **Complete Gesture Support:**
- **🖐️ Palm** → Play/Pause videos
- **👍 Thumbs Up** → Volume Up / Like video  
- **👎 Thumbs Down** → Volume Down / Dislike video
- **✊ Fist** → Mute/Unmute
- **🖖 Fingers Up** → Volume Up
- **👇 Fingers Down** → Volume Down

### 🌐 **Browser Integration:**
- Works with YouTube & Netflix
- Real-time gesture recognition
- Visual feedback in browser
- Chrome extension control

## 🛠️ Installation (3 Steps)

### Step 1: Setup Python Environment
```bash
# Navigate to project folder
cd /path/to/CMPT310-Project

# Run automated setup
./setup.sh

# Or manual setup:
python -m venv myvenv
source myvenv/bin/activate  # macOS/Linux
pip install opencv-python mediapipe tensorflow numpy scikit-learn requests
```

### Step 2: Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (toggle top-right)
3. Click "Load unpacked"
4. Select `web-extension/` folder from this project
5. Extension should appear in your toolbar

### Step 3: Verify Setup
```bash
# Test if everything works
python test_enhanced_gestures.py
```

## 🚀 Usage (2 Commands)

### Quick Start:
```bash
# Start the complete system
python run.py
# Choose Option 1: Enhanced Multi-Gesture Control
```

### Manual Start:
```bash
# Terminal 1: Start API server (keep running)
python gesture_api_server.py

# Terminal 2: Start gesture recognition  
python enhanced_gesture_controller.py
```

## 📺 Browser Setup

1. **Open YouTube or Netflix**
2. **Start playing a video** (not on homepage!)
3. **Click the 🎬 extension icon**
4. **Click "Start Detection"** → should turn GREEN
5. **Show gestures to camera** → controls should work!

## 🖐️ How to Use Gestures

### **Palm Gesture (Play/Pause)**
- Show open palm to camera
- Keep all 5 fingers extended
- Hold steady for 1-2 seconds
- Video should pause/play

### **Thumbs Up (Volume Up)**
- Make thumbs up gesture
- Point thumb upward clearly
- Hold steady for 1-2 seconds

### **Thumbs Down (Volume Down)**  
- Make thumbs down gesture
- Point thumb downward clearly
- Hold steady for 1-2 seconds

### **Fist (Mute/Unmute)**
- Make closed fist
- Keep all fingers closed
- Hold steady for 1-2 seconds

## 🔧 Troubleshooting

### ❌ **Gestures Not Working?**
1. **Check API Server:**
   ```bash
   curl http://localhost:8081/status
   ```
   Should return: `{"status": "running"}`

2. **Check Extension:**
   - Right-click extension icon → "Inspect popup"
   - Look for errors in console
   - Try disable/enable extension

3. **Check Browser Page:**
   - Must be on VIDEO page (not homepage)
   - Press F12 → Console should show: "Gesture-controlled media player loaded!"

### 📷 **Camera Issues?**
- Check camera permissions in System Preferences
- Close other apps using camera (Zoom, Teams, etc.)
- Try different camera if multiple available

### 🔌 **Extension Not Loading?**
- Verify you selected correct `web-extension/` folder
- Check Chrome extensions page for errors
- Try refreshing browser page

## 📋 File Structure

```
CMPT310-Project/
├── enhanced_gesture_controller.py    # Main enhanced controller
├── gesture_api_server.py            # API server for browser communication
├── run.py                          # Interactive launcher
├── test_enhanced_gestures.py       # Test all gestures
├── models/
│   └── gesture_recognizer.task     # Trained MediaPipe model
├── web-extension/                  # Chrome extension files
│   ├── manifest.json
│   ├── background.js              # Enhanced gesture handling
│   └── content.js                 # Multi-gesture support
└── setup.sh                       # Automated setup script
```

## 🎯 Testing Your Setup

### Test 1: API Server
```bash
python gesture_api_server.py
# Should show: "Gesture API server starting on http://localhost:8081"
```

### Test 2: Enhanced Gestures
```bash  
python test_enhanced_gestures.py
# Should send all 6 gesture types to browser
```

### Test 3: Live Recognition
```bash
python enhanced_gesture_controller.py  
# Should open camera with gesture recognition
```

### Test 4: Browser Integration
1. Open YouTube video
2. Start gesture controller 
3. Click extension → "Start Detection"
4. Show palm → video should pause/play

## 💡 Pro Tips

- **Good Lighting**: Ensure your hand is well-lit
- **Clear Background**: Avoid busy backgrounds behind your hand
- **Proper Distance**: Keep hand 1-2 feet from camera
- **Hold Steady**: Gestures need to be stable for 1-2 seconds
- **One Hand**: Use one hand at a time for best results

## 🚀 Next Steps

### For Development:
- Modify `enhanced_gesture_controller.py` to add new gestures
- Update `web-extension/content.js` for new websites
- Train new models using `models/gesture_recognizer.ipynb`

### For Usage:
- Practice gestures in good lighting
- Try different websites (add support in content.js)
- Use gesture cooldown (2 seconds between gestures)

## 🎬 Success!

You now have a complete multi-gesture media control system that demonstrates:
- ✅ **Advanced AI/ML**: MediaPipe + TensorFlow integration
- ✅ **Real-world Application**: Browser media control  
- ✅ **Full-stack Development**: Python + JavaScript + Chrome APIs
- ✅ **User Experience**: Intuitive gesture interface

**Perfect for CMPT 310 - Advanced AI Techniques in Action!** 🚀

---

**Need help?** Check:
- `README.md` - Complete project documentation
- `INTEGRATION_SUMMARY.md` - Technical details
- `run.py` - Interactive troubleshooting menu
