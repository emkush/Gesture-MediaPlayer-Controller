# 🎬 QUICK START GUIDE

## 🚀 **EASIEST WAY TO TEST MANUAL CAMERA:**

### **Step 1: Install Extension** (One-time setup)
```bash
1. Open Chrome → chrome://extensions/
2. Enable "Developer mode" (top right)
3. Click "Load unpacked" 
4. Select: /Users/jethrohermawan/310/Project/web-extension/
```

### **Step 2: Start Backend**
```bash
# Terminal 1: API Server (keep this running)
cd /Users/jethrohermawan/310/Project
python gesture_api_server.py
```

### **Step 3: Test Manual Camera**
```bash
# Terminal 2: Manual Camera Test
cd /Users/jethrohermawan/310/Project  
python scripts/simple_test.py
```

**Or use the launcher:**
```bash
python run.py
# Choose option 2
```

---

## 📂 **ORGANIZED FILE STRUCTURE:**

```
/Users/jethrohermawan/310/Project/
├── run.py                     # 🚀 MAIN LAUNCHER - START HERE
├── gesture_api_server.py      # 🔧 Backend server (always needed)
│
├── scripts/
│   ├── simple_test.py         # 📹 Manual camera (press 'p' for gesture)
│   └── improved_gesture_controller.py  # 🤖 Full AI recognition
│
├── tests/
│   ├── quick_test.py          # 🧪 Test extension without camera
│   └── debug_extension.py     # 🔍 Diagnose problems
│
├── models/
│   ├── palm_model.py          # 🧠 Train AI model
│   └── model.py               # 📊 Original model
│
└── web-extension/             # 🌐 Chrome extension files
```

---

## 🎯 **WHAT TO RUN FIRST:**

### **For Manual Camera Testing:**
```bash
# 1. Start this (keep running):
python gesture_api_server.py

# 2. Then run this:
python scripts/simple_test.py
```

### **For Extension Testing (no camera):**
```bash  
# 1. Start this (keep running):
python gesture_api_server.py

# 2. Then run this:
python tests/quick_test.py
```

### **For Full AI Recognition:**
```bash
# 1. Start this (keep running):
python gesture_api_server.py

# 2. Then run this:
python scripts/improved_gesture_controller.py
```

---

## 🔧 **TROUBLESHOOTING:**

**If confused:** Run `python run.py` - it has a menu!

**If not working:** Run `python tests/debug_extension.py`

**If camera issues:** Check System Preferences → Privacy → Camera

---

## 🎉 **SUCCESS CRITERIA:**

✅ **Extension test works:** Video pauses/plays when you run `quick_test.py`

✅ **Camera test works:** Camera opens, you press 'p', video pauses/plays

✅ **Full AI works:** Show palm to camera, video pauses/plays automatically

**Start with the extension test, then camera test, then full AI!**
