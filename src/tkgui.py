import tkinter as tk  # noqa: F401
import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as  # noqa: F401
from PIL import Image, ImageTk  # noqa: F401
from tkinter import PhotoImage, Frame, Button, Label, Menu, Tk, Text  # noqa: F401
from modules import ImageLabel  # noqa: F401

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class GUI:
    """Main GUI class to interact with the backend"""

    def __init__(self, typingColors: backend.TypingColors):
        """Initializes variables and window"""
        # stores the backend class
        self.typingColors = typingColors

        # To delay invoking image updation when the user is continuously typing
        self.last_time = 0
        self.interval = 0.6
        self.UPDATE_FLAG = False

        self.file = None  # Opened files

        # Creates the window
        self.root = Tk()
        self.loading_screen()
        # self.create_main_window([])
        self.ask_key()

    def ask_key(self):
        """Asks For encryption key from the user"""
        pass

    # function to create the place to write text to create image

    def loading_screen(self):
        """The starting page for the application"""
        self.root.title("Pixel Studios")
        self.root.geometry(f"{WIN_W}x{WIN_H}")
        # title = Label(self.root, bg=DARK_GRAY, width=WIN_W, height=WIN_H, image="")
        # canvas = tk.Canvas(self.root, width=WIN_W, height=WIN_H, bg=DARK_GRAY, bd=0, highlightthickness=0)
        # canvas.place(relx=0.5, rely=0.5, anchor="center")

        gif = ImageLabel(self.root)
        gif.configure(bd=0, highlightbackground=None)
        gif.place(relx=0.5, rely=0.43, anchor="center")

        def loading_animation(root):
            """Loading animation circle for the application"""
            loading = ImageLabel(root)
            loading.configure(bd=0, highlightbackground=None)
            loading.place(relx=0.5, rely=0.57, anchor="center")
            loading.load("assets\\imgs\\loading.gif", False, lambda: self.create_main_window([loading, gif]))
        gif.load("assets\\imgs\\title.gif", False, lambda: loading_animation(self.root))
        self.root.configure(background=DARK_GRAY)
        self.root.mainloop()

    def create_menu_bar(self):
        """Packs the menu bar for the application"""
        file_layout = {'New': {'command': '', 'image': 'assets\\imgs\\new.png',
                               'accelerator': 'Ctrl+N'},
                       'Open': {'command': '', 'image': 'assets\\imgs\\open.png',
                                'accelerator': 'Ctrl+O'},
                       'Save': {'command': '', 'image': 'assets\\imgs\\save.png',
                                'accelerator': 'Ctrl+S'},
                       'Save As  ': {'command': '', 'image': 'assets\\imgs\\save_as.png',
                                     'accelerator': 'Ctrl+Shift+S'},
                       '---': '',
                       'Exit': {'command': tk.Frame.destroy, 'image': 'assets\\imgs\\exit.png',
                                'accelerator': 'Alt+F4'}
                       }
        config_layout = ['Set Key']

        # Main Menu Bar
        menubar = Menu(self.root, tearoff=0, font=("Consolas", 12))
        # File Menu Bar
        fileMenu = Menu(self.root, tearoff=0, cursor="hand1", font=("Consolas", 10))
        menubar.add_cascade(label="File", menu=fileMenu)
        for name, data in file_layout.items():
            if name == "---":
                fileMenu.add_separator()
            else:
                img = Image.open(data['image'])
                icon = ImageTk.PhotoImage(file=img)
                # Icon not reflecting as of now, causing the "menu" to not be visible
                # This is a known error
                fileMenu.add_command(label=name,
                                     command=data['command'],
                                     accelerator=data['accelerator'],
                                     image=icon,
                                     compound="left",
                                     activeforeground=WHITE,
                                     activebackground=GRAY,
                                     )

        configMenu = Menu(self.root, tearoff=0)
        menubar.add_cascade(label="Config", menu=configMenu)
        for item in config_layout:
            configMenu.add_command(label=item,
                                   activeforeground=WHITE,
                                   activebackground=GRAY,
                                   )
        self.root.configure(background=DARK_GRAY, menu=menubar)

    def create_main_window(self, destroy: list[ImageLabel]):
        """Creates The Main Window Page for the application"""
        if len(destroy) > 0:  # Destroy the previous image labels for a fresh home screen application.
            for i in destroy:
                i.destroy()
        self.create_menu_bar()

        # The Main Input Frame:
        main = Frame(self.root, bg=DARK_GRAY)
        main.place(relx=0.5, rely=0.5, anchor="center")
        input = Frame(main, bg=DARK_GRAY)
        input.pack()

        label = Label(input, text="Enter Secret Key:", font=("Consolas", 12), bg=DARK_GRAY, fg=WHITE, pady=5)
        label.pack()

        self.key = Text(input, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0)
        self.key.pack()

        random = Label(input, text="Note: You can keep it empty for a random key", font=("Consolas", 10, "italic"),
                       bg=DARK_GRAY, fg=WHITE, pady=2)
        random.pack()

        self.error = Label(input, text="", font=("Consolas", 10, "bold"), bg=DARK_GRAY, fg=BRIGHT_RED, pady=2)
        self.error.pack()

        # Encrypt / Decrypt Buttons Frame:
        buttons = Frame(main, background=DARK_GRAY, pady=50)
        encrypt = Button(buttons, text="Encrypt", font=("Consolas", 12, "bold"), bg=RED, fg=WHITE,
                         padx=5, pady=5, cursor="hand2", bd=0, command=lambda: self.check_key(True))
        encrypt.grid(row=0, column=0, padx=10, pady=10)
        decrypt = Button(buttons, text="Decrypt", font=("Consolas", 12, "bold"), bg=GREEN, fg=WHITE,
                         padx=5, pady=5, cursor="hand2", bd=0, command=lambda: self.check_key(False))
        decrypt.grid(row=0, column=10, padx=10, pady=10)
        buttons.pack()
        # buttons.place(relx=0.5, rely=0.5, anchor="center")
        self.root.mainloop()

    def check_key(self, encrypt: bool):
        """Checks if key length is between 4 and 24, and then opens the encrypt/decrypt page"""
        key = self.key.get(1.0, "end-1c")
        if 4 <= len(key) <= 24 or len(key) == 0:
            if encrypt:
                self.encrypt(key)
            else:
                self.decrypt(key)
        else:
            self.key.configure(bg=RED, fg=WHITE)
            self.error.configure(text="Key must be between 4 and 24 characters long (or empty)")

    def encrypt(self, key: str = None):
        """Opens the encryption page with the secret key"""
        self.typingColors.set_encryption(key)
        # self.typingColors.save("test.png")
        # self.create_image_window("test.png")

    def decrypt(self, key: str = None):
        """Opens the decryption page with the secret key"""
        print(key)
        self.typingColors.set_encryption(key)


if __name__ == "__main__":
    gui = GUI(backend.TypingColors())
    # gui.create_main_window()
