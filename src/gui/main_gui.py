from pathlib import Path
from random import choices
from tkinter import *
# from .modules import *
from . import modules
from tkinter import filedialog as fd

from backend.typingcolors import TypingColors
from backend import utils
from gui.modules import *
from gui.win_decrypt import DecryptWin
from gui.win_steganography import SteganographyWin
from gui.win_typingcolors import TypingColorsWin

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
IMGS = Path("assets") / "imgs"


class GUI(Tk):
    """Main GUI class to interact with the backend"""

    def __init__(self):
        """Initializes variables and window"""
        # Creates the window
        super().__init__()

    def callback(self, callback: callable, destroy: list[Widget] = None, *args):
        """Callback a function while destroying existing widgets"""
        # Destroy the previous image labels for a fresh home screen application.
        for i in destroy:
            i.destroy()
        callback(*args)

    # function to create the place to write text to create image

    def loading_screen(self):
        """The starting page for the application"""
        self.title("Pixel Studios")
        self.geometry(f"{WIN_W}x{WIN_H}")
        center(self, WIN_W, WIN_H)

        gif = ImageLabel(self)
        gif.configure(bd=0, highlightbackground=None)
        gif.place(relx=0.5, rely=0.43, anchor="center")

        def loading_animation(root):
            """Loading animation circle for the application"""
            loading = ImageLabel(root)
            loading.configure(bd=0, highlightbackground=None)
            loading.place(relx=0.5, rely=0.57, anchor="center")
            loading.load(
                IMGS / "loading.gif",
                False,
                lambda: callback(self.create_main_window, [loading, gif]),
            )

        # gif.load(IMGS / "title.gif", False, lambda: loading_animation(self))
        gif.load(IMGS / "title.gif", False, lambda: callback(self.create_main_window, [gif]))
        self.configure(background=DARK_GRAY)
        self.mainloop()

    def create_main_window(self):
        """Creates The Main Window Page for the application"""
        # The Main Input Frame:
        self.main = Frame(self, bg=DARK_GRAY)
        self.main.place(relx=0.5, rely=0.5, anchor="center")
        input = Frame(self.main, bg=DARK_GRAY)
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

        self.key_method = Text(
            input, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0
        )
        self.key_method.pack()

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
        buttons = Frame(self.main, background=DARK_GRAY, pady=15)

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
        self.mainloop()

    def _valid_key(self):
        """Checks if key is valid"""
        self.key = self.key_method.get(1.0, "end-1c")
        if not (4 <= len(self.key) <= 24 or len(self.key) == 0):
            self.key_method.configure(bg=RED, fg=WHITE)
            self.error.configure(text="Key must be between 4 and 24 characters long")
            return False
        elif " " in self.key:
            self.key_method.configure(bg=RED, fg=WHITE)
            self.error.configure(text="Key can't contain whitespaces")
            return False
        return True

    def check_key(self, encrypt: bool, mode: int = 0):
        """Opens the encrypt/decrypt page"""
        self.key = self.key_method.get(1.0, "end-1c")
        if modules._valid_key(self, self.key, self.key_method, self.error):
            self.key_method.configure(bg=DARK_GRAY, fg=WHITE)
            self.error.configure(text="")
            if encrypt:
                self.encrypt(self.key, mode)
            elif len(self.key) > 0:  # checks if key is not empty for decryption
                self.decrypt(self.key)
            else:
                self.key_method.configure(bg=RED, fg=WHITE)
                self.error.configure(text="Invalid secret key")

    def encrypt(self, key: str = None, mode: int = 0):
        """Opens the encryption page with the secret key"""
        # Mode 0 is for Typing Colors
        # Mode 1 is for Masked Image
        if mode == 0:
            self.typingColors = TypingColors()
            if len(key) == 0:
                key = "".join(choices(PRINTABLE.replace("\t", ""), k=16))
            self.typingColors.set_key(key)
            callback(
                lambda: TypingColorsWin(self, self.typingColors, key
                                        ).pack(expand=True, fill='both'), [self.main])
        else:
            self.steganographyWin = SteganographyWin()

    def decrypt(self, key: str = None):
        """Opens the decryption page with the secret key"""
        # TODO: find out what method used to encrypt here
        # decrypting typingcolors image
        filename = fd.askopenfilename(
            title="Select Image", filetypes=[("PNG", "*.png")]
        )
        try:
            self.typingColors, decoded_text = utils.decrypt(filename, key)
        except KeyError:  # invalid decryption key
            self.key_method.configure(bg=RED, fg=WHITE)
            self.error.configure(text="Invalid secret key")
            return

        callback(
            lambda: DecryptWin(self, self.typingColors, decoded_text, key).pack(expand=True, fill='both'), [self.main]
        )
