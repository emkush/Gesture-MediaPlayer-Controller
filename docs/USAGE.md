# 🎬 How to Run the Gesture-Controlled Media Player

## 📋 Complete Setup Guide

### **Prerequisites**
- ✅ Chrome browser
- ✅ Python environment (already set up in `myvenv/`)
- ✅ Webcam (for real gesture recognition)

## 🚀 Method 1: Quick Demo (Without Camera)

Perfect for testing if everything works:

```bash
# 1. Start API server (keep this running)
python gesture_api_server.py

# 2. In another terminal, run the demo
python test_demo.py
```

**What this does:**
- Tests the extension communication
- Sends fake palm gestures every 5 seconds
- Great for verifying the system works before using camera

## 🎥 Method 2: Full System with Camera

For real gesture recognition:

```bash
# Option A: Use the automated script
./start.sh

# Option B: Manual setup
# Terminal 1:
python gesture_api_server.py

# Terminal 2:
python gesture_controller.py
```

## 🔧 Chrome Extension Setup

1. **Install Extension:**
   ```
   1. Open Chrome → chrome://extensions/
   2. Enable "Developer mode" (top right toggle)
   3. Click "Load unpacked"
   4. Select: /Users/jethrohermawan/310/Project/web-extension/
   ```

2. **Verify Installation:**
   - Look for "Gestured-Controlled Media Player" in extensions list
   - Should have a 🎬 icon in toolbar

## 🎯 Usage Steps

### **Step 1: Start the Backend**
```bash
# Choose one:
./start.sh                    # Automatic (camera required)
python test_demo.py          # Demo mode (no camera)
```

### **Step 2: Prepare Browser**
1. Open YouTube: https://youtube.com/watch?v=dQw4w9WgXcQ
2. Or Netflix: https://netflix.com (any video)

### **Step 3: Activate Extension**
1. Click the 🎬 extension icon in Chrome toolbar
2. Click "Start Detection" button
3. Status indicator should turn green

### **Step 4: Use Gestures**
- **With Camera:** Show palm to webcam → pause/play
- **Demo Mode:** Automatic gestures every 5 seconds

## 📱 Extension Interface

```
🎬 Gesture Control
Control media with hand gestures

┌─────────────────────────┐
│ Gesture Detection   ● │  ← Green = active
│ Current site: YouTube ✓│
│                         │
│ [Start Detection]       │
│                         │
│ Available Gestures:     │
│ 🖐️ Palm → Play/Pause    │
│ 👍 Thumbs Up → Coming   │
│ ✌️ Peace → Coming       │
└─────────────────────────┘
```

## 🐛 Troubleshooting

### **Camera Issues (Most Common)**

**Problem:** "Failed to grab frame" or camera won't open

**Solutions:**
```bash
# 1. Use improved version with better camera detection
python improved_gesture_controller.py

# 2. Check camera permissions
# System Preferences → Security & Privacy → Camera → Allow Terminal/Python

# 3. Close other camera apps (Zoom, Teams, FaceTime, etc.)

# 4. Test camera manually
python -c "import cv2; cap=cv2.VideoCapture(0); print('Camera works:', cap.read()[0])"

# 5. Use demo mode if camera fails
python test_demo.py
```

### **TensorFlow/MediaPipe Warnings**

**Problem:** AttributeError, MessageFactory errors, or compilation warnings

**Solution:** These are usually harmless warnings. Use the improved version:
```bash
python improved_gesture_controller.py  # Has better error handling
```

### **Extension Not Working**
```bash
# Check API server
curl http://localhost:8081/status

# Should return: {"status": "running", ...}
```

### **Gesture Not Detected**
- Use improved version: `python improved_gesture_controller.py`
- Ensure good lighting (not too dark/bright)
- Keep hand clearly visible and steady
- Try demo mode first: `python test_demo.py`
- Lower detection threshold in code if needed

### **Website Not Responding**
- Refresh the page after starting extension
- Check extension is loaded in chrome://extensions/
- Make sure you're on a video page (not homepage)
- Try different video or website

## 🔍 Debug Mode

Add debug output to see what's happening:

```bash
# Check extension console
# 1. Right-click extension icon → "Inspect popup"
# 2. Check Console tab for errors

# Check content script
# 1. F12 on YouTube/Netflix page  
# 2. Look for "Gesture-controlled media player loaded!"
```

## 📊 System Status Checks

```bash
# 1. API Server Status
curl http://localhost:8081/status

# 2. Send Test Gesture
curl -X POST http://localhost:8081/gesture \
  -H "Content-Type: application/json" \
  -d '{"gesture": "palm", "timestamp": 1234567890}'

# 3. Check Latest Gesture
curl http://localhost:8081/gesture
```

## 🎮 Different Usage Modes

### **Mode 1: Development/Testing**
```bash
python test_demo.py  # No camera needed
```

### **Mode 2: Real Usage**
```bash
python improved_gesture_controller.py  # Camera required (better version)
python gesture_controller.py          # Original version
```

### **Mode 3: Full System**
```bash
./start.sh  # Everything automated
```

## 💡 Tips for Best Results

1. **Lighting:** Use good room lighting
2. **Position:** Keep hand 1-2 feet from camera
3. **Gesture:** Show clear palm for 1-2 seconds
4. **Timing:** Wait 2 seconds between gestures (cooldown)
5. **Sites:** Works best on video player pages

## 🚀 Quick Start Checklist

- [ ] Chrome extension installed
- [ ] API server running (`python gesture_api_server.py`)
- [ ] YouTube or Netflix open
- [ ] Extension "Start Detection" clicked
- [ ] Camera working (for real mode) OR demo running
- [ ] Show palm gesture → media should pause/play

**🎉 Success:** You should see media pause/play when you show your palm!
