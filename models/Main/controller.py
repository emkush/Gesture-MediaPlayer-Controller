from pynput.keyboard import Controller, Key

class ActionController:
    """
    PURPOSE:
    This class handles the keyboard. It translates a gesture name 
    into an actual computer key press.
    """

    def __init__(self):
        self.keyboard = Controller()

    def execute_action(self, gesture_name):
        """
        PURPOSE:
        Checks the gesture name and triggers the correct function.
        Returns "EXIT" if the user wants to quit.
        """
        if gesture_name == "thumbs_up":
            self.play_pause()
        
        elif gesture_name == "fist":
            self.volume_down()
            
        elif gesture_name == "victory":
            self.volume_up()
            
        elif gesture_name == "swipe_left":
            self.rewind()
            
        elif gesture_name == "swipe_right":
            self.forward()
            
        elif gesture_name == "open_palm":
            return "EXIT" # Tell Main.py to stop
        
        return None # Do nothing

    # --- KEYBOARD SHORTCUTS ---

    def play_pause(self):
        # Press Spacebar
        self.keyboard.press(" ")
        self.keyboard.release(" ")

    def volume_up(self):
        # Press Special Volume Up Key
        self.keyboard.press(Key.media_volume_up)
        self.keyboard.release(Key.media_volume_up)

    def volume_down(self):
        # Press Special Volume Down Key
        self.keyboard.press(Key.media_volume_down)
        self.keyboard.release(Key.media_volume_down)

    def rewind(self):
        # Press Left Arrow
        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)

    def forward(self):
        # Press Right Arrow
        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)