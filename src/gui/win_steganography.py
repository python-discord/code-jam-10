from tkinter import *

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class SteganographyWin(Tk):
    """Window for steganography"""

    def __init__(self):
        """Creates the layout"""
        super().__init__()
