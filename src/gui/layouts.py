from tkinter import *

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"

def create_menu_bar(app):
    """Packs the menu bar for the application"""
    file_layout = {
        "New": {
            "command": "",
            "image": "assets\\imgs\\new.png",
            "accelerator": "Ctrl+N",
        },
        "Open": {
            "command": "",
            "image": "assets\\imgs\\open.png",
            "accelerator": "Ctrl+O",
        },
        "Save": {
            "command": "",
            "image": "assets\\imgs\\save.png",
            "accelerator": "Ctrl+S",
        },
        "Save As  ": {
            "command": "",
            "image": "assets\\imgs\\save_as.png",
            "accelerator": "Ctrl+Shift+S",
        },
        "---": "",
        "Exit": {
            "command": app.destroy,
            "image": "assets\\imgs\\exit.png",
            "accelerator": "Alt+F4",
        },
    }
    config_layout = ["Set Key"]

    # Main Menu Bar
    menubar = Menu(app, tearoff=0, font=("Consolas", 12))
    # File Menu Bar
    fileMenu = Menu(app, tearoff=0, cursor="hand1", font=("Consolas", 10))
    menubar.add_cascade(label="File", menu=fileMenu)
    for name, data in file_layout.items():
        if name == "---":
            fileMenu.add_separator()
        else:
            # img = Image.open(data['image'])
            # icon = ImageTk.PhotoImage(img)
            # print(icon)
            # Icon not reflecting as of now, causing the "menu" to not be visible
            # This is a known error
            fileMenu.add_command(
                label=name,
                command=data["command"],
                accelerator=data["accelerator"],
                #  image=icon,
                compound="left",
                activeforeground=WHITE,
                activebackground=GRAY,
            )

    configMenu = Menu(app, tearoff=0)
    menubar.add_cascade(label="Config", menu=configMenu)
    for item in config_layout:
        configMenu.add_command(
            label=item,
            activeforeground=WHITE,
            activebackground=GRAY,
        )
    app.configure(background=DARK_GRAY, menu=menubar)

class TypingColorsWin(Toplevel):
    """Window for typingcolors"""

    def __init__(self, typingColors):
        super().__init__()
        create_menu_bar(self)
        self.typingColors = typingColors
        self.text = Text(
            self,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.text.grid(row=0, column=0, sticky='nsew')
        self.canvas = Label(
            self, image=self.typingColors.img_scaled(), bg=DARK_GRAY
        )
        self.canvas.grid(row=0, column=1, sticky="nw")
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt):
        """Update loop for typingcolours"""
        txt = self.text.get("1.0", "end")
        if txt != prev_txt:  # only update if text changed
            self.typingColors.update(txt)
            img = self.typingColors.img_scaled()
            self.canvas.configure(image=img)
            self.canvas.image = img
        self.after(50, lambda: self._typingcolors_update(txt))


class SteganographyWin():
    """Window for steganography layout"""
    pass
