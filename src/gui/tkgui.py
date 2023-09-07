import tkinter as tk
from tkinter import *  # noqa: F403

from backend.typingcolors import TypingColors
from backend.typingcolors_utils import load
from gui.layouts import SteganographyWin, TypingColorsWin
from gui.modules import ImageLabel

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class GUI:
    """Main GUI class to interact with the backend"""

    def __init__(self):
        """Initializes variables and window"""
        self.file = None  # Opened files

        # Creates the window
        self.root = Tk()
        self.loading_screen()

    def center(self, root: Tk):
        """Centers a tkinter window"""
        root.update_idletasks()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        x = int((width - WIN_W)/2)
        y = int((height - WIN_H)/3)  # A bit off center to align it well with the taskbar
        root.geometry(f"+{x}+{y}")

    def callback(self, callback: callable, destroy: list[Widget] = None, *args):
        """Callback a function while destroying existing widgets"""
        if len(destroy) > 0:  # Destroy the previous image labels for a fresh home screen application.
            for i in destroy:
                i.destroy()
        callback(*args)

    # function to create the place to write text to create image

    def loading_screen(self):
        """The starting page for the application"""
        self.root.title("Pixel Studios")
        self.root.geometry(f"{WIN_W}x{WIN_H}")
        # self.root.eval('tk::PlaceWindow . center')
        self.center(self.root)

        gif = ImageLabel(self.root)
        gif.configure(bd=0, highlightbackground=None)
        gif.place(relx=0.5, rely=0.43, anchor="center")

        def loading_animation(root):
            """Loading animation circle for the application"""
            loading = ImageLabel(root)
            loading.configure(bd=0, highlightbackground=None)
            loading.place(relx=0.5, rely=0.57, anchor="center")
            loading.load(
                "assets\\imgs\\loading.gif",
                False,
                lambda: self.callback(self.create_main_window, [loading, gif]),
            )

        gif.load("assets\\imgs\\title.gif", False, lambda: loading_animation(self.root))
        self.root.configure(background=DARK_GRAY)
        self.root.mainloop()

    def create_main_window(self):
        """Creates The Main Window Page for the application"""
        # The Main Input Frame:
        main = Frame(self.root, bg=DARK_GRAY)
        main.place(relx=0.5, rely=0.5, anchor="center")
        input = Frame(main, bg=DARK_GRAY)
        input.pack()

        label = Label(
            input,
            text="Enter Secret Key:",
            font=("Consolas", 12),
            bg=DARK_GRAY,
            fg=WHITE,
            pady=5,
        )
        label.pack()

        self.key = Text(
            input, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0
        )
        self.key.pack()

        self.error = Label(
            input,
            text="",
            font=("Consolas", 10, "bold"),
            bg=DARK_GRAY,
            fg=BRIGHT_RED,
            pady=2,
        )
        self.error.pack()

        # Encrypt / Decrypt Buttons Frame:
        buttons = Frame(main, background=DARK_GRAY, pady=15)

        # Encrypt OptionMenu
        method = StringVar()
        method.set("Encrypt ▼")
        opts = ["Typing Colors", "Use Masked Image"]
        encrypt = OptionMenu(
            buttons,
            method,
            *opts,
        )
        encrypt.configure(
            font=("Consolas", 12, "bold"),
            bg=RED,
            fg=WHITE,
            padx=5,
            pady=5,
            cursor="hand2",
            indicatoron=0,
            bd=0,
            highlightbackground=RED,
            activeforeground=WHITE,
            activebackground=RED,
        )
        encrypt["menu"].configure(
            font=("Consolas", 10),
            cursor="hand2",
            activebackground=RED,
            activeforeground=WHITE,
            foreground=DARK_GRAY,
        )
        encrypt.grid(row=0, column=0, padx=10, pady=10)
        method.trace("w", lambda *args: self.check_key(True, opts.index(method.get())))

        # Decrypt Button
        decrypt = Button(
            buttons,
            text="Decrypt",
            font=("Consolas", 12, "bold"),
            bg=GREEN,
            fg=WHITE,
            padx=5,
            pady=3,
            cursor="hand2",
            bd=0,
            command=lambda: self.check_key(False),
        )
        decrypt.grid(row=0, column=10, padx=10, pady=10)
        buttons.pack()
        # buttons.place(relx=0.5, rely=0.5, anchor="center")
        self.root.mainloop()

    def check_key(self, encrypt: bool, mode: int = 0):
        """Checks if key length is between 4 and 24, and then opens the encrypt/decrypt page"""
        key = self.key.get(1.0, "end-1c")
        if 4 <= len(key) <= 24:
            if encrypt:
                self.encrypt(key, mode)
            else:
                self.decrypt(key)
        else:
            self.key.configure(bg=RED, fg=WHITE)
            self.error.configure(
                text="Key must be between 4 and 24 characters long"
            )

    def encrypt(self, key: str = None, mode: int = 0):
        """Opens the encryption page with the secret key"""
        # Mode 0 is for Typing Colors
        # Mode 1 is for Masked Image
        self.typingColors = TypingColors()
        self.typingColors.set_encryption(key)

        self.typingColorsWin = TypingColorsWin(self.typingColors)

    def decrypt(self, key: str = None):
        """Opens the decryption page with the secret key"""
        self.typingColors = TypingColors()
        self.typingColors.set_encryption(key)

        self.typingColorsWin = TypingColorsWin(self.typingColors)
