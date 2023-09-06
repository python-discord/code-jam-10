import tkinter as tk
from tkinter import Button, Entry, Label, Menu, Text, Tk

from backend import TypingColors
from modules import ImageLabel

WIN_W, WIN_H = (640, 480)
DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"


class GUI:
    """Main GUI class to interact with the backend"""

    def __init__(self):
        """Initializes variables and window"""
        # Creates the window
        self.root = Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.loading_screen()
        # self.popup_window = self.create_decrypt_encrypt_window()
        # self.main_window.hide()

    def ask_key(self):
        """Asks For encryption key from the user"""
        win = tk.Toplevel()
        win.wm_title("Enter Secret Key")
        win.geometry("250x100")
        win.grid_rowconfigure(0, weight=1)
        win.grid_rowconfigure(1, weight=1)
        win.grid_columnconfigure(0, weight=1)
        win.grid_columnconfigure(1, weight=1, uniform=1)

        Label(win, text="Secret Key: ").grid(row=0, column=0, sticky="e")
        self.keylabel = Entry(win)
        self.keylabel.grid(row=0, column=1, sticky="w")

        b = Button(win, text="Start Empty", command=lambda: self.main_typingcolors() or win.destroy())
        b.grid(row=1, column=0)
        b1 = Button(win, text="Use Mask Image", command=lambda: self.main_encodeimg() or win.destroy())
        b1.grid(row=1, column=1)

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
        gif.place(relx=0.5, rely=0.45, anchor="center")

        def loading_animation(root):
            """Loading animation circle for the application"""
            loading = ImageLabel(root)
            loading.configure(bd=0, highlightbackground=None)
            loading.place(relx=0.5, rely=0.55, anchor="center")
            loading.load("assets\\imgs\\loading.gif", False, lambda: gif.destroy() or self.ask_key())
        gif.load("assets\\imgs\\title.gif", False, lambda: loading_animation(self.root))
        self.root.configure(background=DARK_GRAY)

    def _typingcolors_update(self, prev_txt):
        """Update loop for typingcolours"""
        txt = self.text.get('1.0', 'end')
        if txt != prev_txt:
            self.typingColors.update(txt)
            img = self.typingColors.img_tk()
            self.canvas.configure(image=img)
            self.canvas.image = img
        self.root.after(50, lambda: self._typingcolors_update(txt))

    def main_typingcolors(self):
        """Main function for typingcolours layout"""
        self.typingColors = TypingColors()
        self.typingColors.set_encryption(self.keylabel.get())
        self.text = Text(self.root, width=30, height=20)
        self.text.grid(row=0, column=0)
        self.canvas = tk.Label(self.root, image=self.typingColors.img_tk())
        self.canvas.grid(row=0, column=1)
        self._typingcolors_update('')

    def main_encodeimg(self):
        """Encode image method."""
        pass

    def run(self):
        """Creates The Main Window Page for the application"""
        file_layout = {'New': {'command': '',
                               'accelerator': 'Ctrl+N'},
                       'Open': {'command': '',
                                'accelerator': 'Ctrl+O'},
                       'Save': {'command': '',
                                'accelerator': 'Ctrl+S'},
                       'Save As': {'command': '',
                                   'accelerator': 'Ctrl+Shift+S'},
                       '---': '',
                       'Exit': {'command': self.root.destroy,
                                'accelerator': 'Alt+F4'}
                       }
        config_layout = {'Set Key': {'command': self.ask_key}}

        # Main Menu Bar
        menubar = Menu(self.root, tearoff=0, font=("Consolas", 12))

        # File Menu Bar
        fileMenu = Menu(self.root, tearoff=0, cursor="hand1", font=("Consolas", 10))
        menubar.add_cascade(label="File", menu=fileMenu)
        for name, data in file_layout.items():
            if name == "---":
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=name,
                                     command=data['command'],
                                     accelerator=data['accelerator'],
                                     compound="left",
                                     activeforeground=WHITE,
                                     activebackground=AQUA,
                                     )

        configMenu = Menu(self.root, tearoff=0)
        menubar.add_cascade(label="Config", menu=configMenu)
        for item, data in config_layout.items():
            configMenu.add_command(label=item, command=data['command'])
        self.root.configure(background=DARK_GRAY, menu=menubar)
        self.root.mainloop()
