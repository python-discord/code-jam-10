from random import choices
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

from backend import utils
from backend.typingcolors import TypingColors
from gui.modules import *
from gui.win_decrypt import DecryptWin
from gui.win_steganography import SteganographyWin
from gui.win_typingcolors import TypingColorsWin

WIN_W, WIN_H = (800, 500)


class GUI(Tk):
    """Main GUI class to interact with the backend"""

    def __init__(self):
        """Initializes variables and window"""
        # Creates the window
        super().__init__()
        self.title("The Neverending Loops")
        self.sw, self.sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.minsize(width=int(self.sw * 0.45), height=int(self.sh * 0.45))

        self.geometry(f"{WIN_W}x{WIN_H}")
        center(self, WIN_W, WIN_H)
        loading_animation(self)
        self.configure(background=DARK_GRAY)

    def callback(self, callback: callable, *args):
        """Callback a function while destroying existing widgets"""
        for widget in self.winfo_children():
            widget.destroy()
        callback(*args)

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

        self.key_method_text = StringVar(input, "")
        self.key_method = Entry(
            input,
            width=25,
            font=("Consolas", 12),
            bd=0,
            textvariable=self.key_method_text,
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
        opts = ["Typing Colors", "Image Masking"]
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
        encrypt.bind(
            "<Enter>",
            lambda event: encrypt["menu"].tk_popup(
                encrypt.winfo_rootx(), encrypt.winfo_rooty() + encrypt.winfo_height()
            ),
        )
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
        self.mainloop()

    def _valid_key(self, empty_key=True):
        """Checks if key is valid"""
        self.key = self.key_method_text.get()
        if len(self.key) == 0:
            if empty_key:
                self.key = "".join(choices(PRINTABLE.replace("\t", ""), k=16))
                return True
            else:
                self.key_method.configure(bg=RED, fg=WHITE)
                self.error.configure(text="Key cannot be empty")
                return False
        elif not (4 <= len(self.key) <= 24):
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
        if self._valid_key(encrypt):
            self.key_method.configure(bg=DARK_GRAY, fg=WHITE)
            self.error.configure(text="")
            if encrypt:
                self.encrypt(mode)
            elif len(self.key) > 0:  # checks if key is not empty for decryption
                self.decrypt()
            else:
                self.key_method.configure(bg=RED, fg=WHITE)
                self.error.configure(text="Invalid secret key")

    def encrypt(self, mode: int = 0):
        """Opens the encryption page with the secret key"""
        # Mode 0 is for Typing Colors
        # Mode 1 is for Masked Image
        if len(self.key) == 0:
            self.key = "".join(choices(PRINTABLE.replace("\t", ""), k=16))
        if mode == 0:

            def create_win():
                self.currentwin = TypingColorsWin(self)
                self.currentwin.pack(expand=True, fill="both")

            self.callback(create_win)
        else:
            self.switch_steganography()

    def decrypt(self):
        """Opens the decryption page with the secret key"""
        filename = fd.askopenfilename(title="Select Image", filetypes=[("PNG", "*.png")])
        if not filename:
            return
        try:
            object, decoded_text = utils.decrypt(filename, self.key)
        except Exception:  # invalid decryption key
            self.key_method.configure(bg=RED, fg=WHITE)
            messagebox.showinfo("Decryption Failed", "Invalid secret key!")
            return

        def create_win():
            self.currentwin = DecryptWin(self, object, decoded_text)
            self.currentwin.pack(expand=True, fill="both")

        self.callback(create_win)

    def switch_typingcolors(self):
        """Switches to typing colors mode"""
        self.typingColors = TypingColors()
        self.typingColors.set_key(self.key)

        def create_win():
            self.currentwin = TypingColorsWin(self)
            self.currentwin.pack(expand=True, fill="both")

        self.callback(create_win)

    def switch_steganography(self):
        """Switches to encrypt steganography"""
        filename = fd.askopenfilename(title="Select Image to use as Mask", filetypes=[("PNG", "*.png")])
        if not filename:
            return

        def create_win():
            self.currentwin = SteganographyWin(self, filename)
            self.currentwin.pack(expand=True, fill="both")

        self.callback(create_win)

    def switch_decrypt(self):
        """Switches to decrypt mode"""
        key_popup(self, after_exec=self.decrypt, empty_key=False)
