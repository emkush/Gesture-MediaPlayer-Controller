#!/usr/bin/env python3
"""
Test script to verify MediaPipe gesture_recognizer.task file works correctly
"""

import os
import sys

def test_task_file():
    """Test if the MediaPipe task file exists and is valid"""
    print("🧪 Testing MediaPipe Task File")
    print("=" * 40)
    
    task_path = "/Users/jethrohermawan/310/Project/models/gesture_recognizer.task"
    
    # Check if file exists
    if not os.path.exists(task_path):
        print(f"❌ Task file not found: {task_path}")
        return False
    
    # Check file size
    file_size = os.path.getsize(task_path)
    print(f"✅ Task file found: {task_path}")
    print(f"📏 File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    # Try to load with MediaPipe
    try:
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        
        print("✅ MediaPipe Tasks library available")
        
        # Try to create gesture recognizer
        base_options = python.BaseOptions(model_asset_path=task_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        recognizer = vision.GestureRecognizer.create_from_options(options)
        
        print("✅ Gesture recognizer created successfully!")
        print("🎯 Your MediaPipe task file is valid and ready to use!")
        
        # Show available gestures (if possible)
        print("\n📋 Task file is compatible with MediaPipe gesture recognition")
        print("💡 You can now use Option 1 in the main launcher for MediaPipe control")
        
        return True
        
    except ImportError:
        print("❌ MediaPipe Tasks library not available")
        print("💡 Install with: pip install mediapipe")
        return False
        
    except Exception as e:
        print(f"❌ Error loading task file: {e}")
        print("💡 The task file might be corrupted or incompatible")
        return False

def main():
    """Main test function"""
    success = test_task_file()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 SUCCESS: Your MediaPipe task file is ready!")
        print("\n🚀 Next steps:")
        print("1. Run: python run.py")
        print("2. Choose option 1 (MediaPipe Gesture Control)")
        print("3. Show your palm to control media!")
    else:
        print("❌ Issues found with MediaPipe task file")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the file is a valid MediaPipe .task file")
        print("2. Install MediaPipe: pip install mediapipe")
        print("3. Use option 2 (AI Gesture Recognition) as fallback")

if __name__ == "__main__":
    main()
