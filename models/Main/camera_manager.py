import cv2
import subprocess
import re
import platform
import sys

class CameraManager:
    """
    Handles camera detection and user selection across macOS, Windows, and Linux.
    """
    def __init__(self):
        self.os_name = platform.system()

    def _get_cameras_macos(self):
        """Internal: Uses ffmpeg to list AVFoundation devices."""
        cameras = {}
        try:
            result = subprocess.run(
                ["ffmpeg", "-f", "avfoundation", "-list_devices", "true", "-i", ""],
                stderr=subprocess.PIPE, text=True
            )
            lines = result.stderr.split("\n")
            capture_mode = False
            for line in lines:
                if "AVFoundation video devices" in line:
                    capture_mode = True
                    continue
                if "AVFoundation audio devices" in line:
                    break
                if capture_mode:
                    match = re.search(r"\[(\d+)\]\s+(.*)", line)
                    if match:
                        cameras[int(match.group(1))] = match.group(2)
        except Exception as e:
            print(f"Warning: ffmpeg detection failed ({e})")
        return cameras

    def _get_cameras_windows(self):
        """Internal: Uses pygrabber if available, or generic fallback."""
        cameras = {}
        try:
            from pygrabber.dshow_graph import FilterGraph
            graph = FilterGraph()
            devices = graph.get_input_devices()
            for i, name in enumerate(devices):
                cameras[i] = name
        except ImportError:
            pass  # pygrabber not installed
        except Exception:
            pass
        return cameras

    def _get_cameras_linux(self):
        """Internal: Uses v4l2-ctl to list devices."""
        cameras = {}
        try:
            result = subprocess.run(["v4l2-ctl", "--list-devices"], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            current_name = None
            for line in output.split("\n"):
                if not line.strip(): continue
                if not line.startswith("\t"):
                    current_name = line.strip()
                elif "/dev/video" in line and current_name:
                    index = int(line.strip().replace("/dev/video", ""))
                    cameras[index] = current_name
                    current_name = None
        except Exception:
            pass
        return cameras

    def get_active_cameras(self):
        """
        Returns a list of tuples (index, name) for cameras that are physically accessible.
        """
        # 1. Get names based on OS
        named_cameras = {}
        if self.os_name == "Darwin":
            named_cameras = self._get_cameras_macos()
        elif self.os_name == "Windows":
            named_cameras = self._get_cameras_windows()
        elif self.os_name == "Linux":
            named_cameras = self._get_cameras_linux()

        # 2. Verify availability with OpenCV
        valid_cameras = []
        
        # If detection failed, probe the first 4 indices blindly
        indices_to_check = named_cameras.keys() if named_cameras else range(4)

        for idx in indices_to_check:
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                name = named_cameras.get(idx, f"Camera Index {idx}")
                valid_cameras.append((idx, name))
                cap.release()
        
        return sorted(valid_cameras, key=lambda x: x[0])

    def select_camera(self):
        """
        Interactively asks the user to select a camera via the terminal.
        Returns: int (The selected camera index)
        """
        print("\n--- Scanning for Cameras ---")
        available = self.get_active_cameras()

        if not available:
            print("No cameras found! Please connect a device.")
            sys.exit()

        print(f"Detected System: {self.os_name}")
        print(f"Found {len(available)} device(s):")
        for idx, name in available:
            print(f"  [{idx}] {name}")

        while True:
            try:
                selection = input("\nEnter camera number to use: ")
                choice = int(selection)
                if any(c[0] == choice for c in available):
                    print(f"Selected: {choice}\n")
                    return choice
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number.")