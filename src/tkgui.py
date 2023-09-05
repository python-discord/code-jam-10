import tkinter as tk  # noqa: F401
import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as  # noqa: F401
from PIL import Image, ImageTk  # noqa: F401
from tkinter import Frame, Button, Label, Menu, Tk  # noqa: F401

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"


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
        # self.popup_window = self.create_decrypt_encrypt_window()
        # self.main_window.hide()

        self.ask_key()

    def ask_key(self):
        """Asks For encryption key from the user"""
        pass

    # function to create the place to write text to create image

    def loading_screen(self):
        """The starting page for the application"""
        self.root.title("Pixel Studios")
        self.root.geometry(f"{WIN_W}x{WIN_H}")
        title = Frame(self.root)
        word = "Pixel Studios"
        for w in word:
            temp = Label(title, text=w, bg=DARK_GRAY, fg=WHITE,
                         borderwidth=0, relief="solid", font=("Consolas", 50))
            # temp.pack(side="left")
            self.show(temp)
            # self.root.after(1, self.add_loop, temp)
        title.place(relx=0.5, rely=0.5, anchor="center")
        self.root.configure(background=DARK_GRAY)
        self.root.mainloop()

    def show(self, label: Label, y=-50):
        """Animated a label from top to bottom"""
        if y < 200:
            label.place(x=200, y=y)
            self.root.after(30, self.show, label, y+10)

    def create_main_window(self):
        """Creates Window for the application"""
        file_layout = {'New': {'command': '', 'image': 'assets\\menubar\\demo.png', 'accelerator': 'Ctrl+N'},
                       'Open': {'command': '', 'image': 'assets\\menubar\\demo.png', 'accelerator': 'Ctrl+O'},
                       'Save': {'command': '', 'image': 'assets\\menubar\\demo.png', 'accelerator': 'Ctrl+S'},
                       'Save As': {'command': '', 'image': 'assets\\menubar\\demo.png', 'accelerator': 'Ctrl+Shift+S'},
                       '---': '',
                       'Exit': {'command': self.root.destroy, 'image': 'assets\\menubar\\demo.png', 'accelerator': 'Alt+F4'}
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
                icon = ImageTk.PhotoImage(img)
                fileMenu.add_command(label=name,
                                     command=data['command'],
                                     accelerator=data['accelerator'],
                                     image=icon,
                                    #  compound="left",
                                     activeforeground=WHITE,
                                     activebackground=AQUA,
                                     )

        configMenu = Menu(self.root, tearoff=0)
        menubar.add_cascade(label="Config", menu=configMenu)
        for item in config_layout:
            configMenu.add_command(label=item)
        self.root.configure(background=DARK_GRAY, menu=menubar)
        self.root.mainloop()

# Testing


if __name__ == "__main__":
    gui = GUI(backend.TypingColors())
    # gui.create_main_window()
