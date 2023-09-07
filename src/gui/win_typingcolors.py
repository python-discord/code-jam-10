from tkinter import *
from tkinter import filedialog as fd
from backend.typingcolors import TypingColors
from gui.main_gui import GUI
# import gui

# from gui.main_gui import GUI

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class TypingColorsWin(GUI):
    """Window for typingcolors"""

    def __init__(self):
        """Creates the layout"""
        # super().__init__()
        # self = root
        self.create_menu_bar()
        self.typingColors = TypingColors()  # the main backend
        self.file = None  # open files
        self.title("New File - Typing Colors")
        # split layout
        self.text = Text(
            self,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(self, image=self.typingColors.img_scaled(), bg=DARK_GRAY)
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.canvas.grid(row=0, column=1, sticky="ne")
        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        # start the loop
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt):
        """Update loop for typingcolours"""
        txt = self.text.get("1.0", "end")
        if txt != prev_txt:  # only update if text changed
            self.typingColors.update(txt)
            img = self.typingColors.img_scaled()
            self.canvas.configure(image=img)
            self.canvas.image = img
            self.info.set(
                f"{len(txt) - 1} characters   |   {self.typingColors.width}px x {self.typingColors.height}px"
            )
        self.after(50, lambda: self._typingcolors_update(txt))

    def new(self):
        """Resets the canvas and text"""
        self.file = None
        self.title("New File - Typing Colors")
        self.text.delete(1.0, "end")
        self.typingColors.update("")

    def open(self):
        """Opens and loads a selected text file"""
        filename = fd.askopenfilename(title="Open", filetypes=[("All", "*.*")])
        if filename:
            content = open(filename, "r").read()
            self.file = filename
            self.title(f"{filename} - Typing Colors")
            self.text.delete(1.0, "end")
            self.text.insert("end", content)
            self.typingColors.update(content)

    def save(self):
        """Saves the current text"""
        if not self.file:  # no file to save to yet
            self.saveas()  # open a file selector then save
        else:
            open(self.file, "w").write(self.text.get(1.0, "end"))

    def saveas(self):
        """Opens a file dialog and saves text to selected file"""
        filename = fd.asksaveasfilename(title="Save As", filetypes=[("All", "*.*")])
        if filename:
            self.file = filename
            self.title(f"{filename} - Typing Colors")
            open(self.file, "w").write(self.text.get(1.0, "end"))

    def export(self):
        """Exports the canvas to a PNG"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("PNG", "*.png")])
        if filename:
            self.typingColors.canvas.save(filename, format="PNG")

    def create_menu_bar(self):
        """Packs the menu bar for the application"""
        layouts = {
            "File": {
                "New": {
                    "command": self.new,
                    "image": "assets\\imgs\\new.png",
                    "accelerator": "Ctrl+N",
                },
                "Open": {
                    "command": self.open,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+O",
                },
                "Save": {
                    "command": self.save,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+S",
                },
                "Save As": {
                    "command": self.saveas,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+Shift+S",
                },
                "Export": {
                    "command": self.export,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+I",
                },
                "---": "",
                "Exit": {
                    "command": self.destroy,
                    "image": "assets\\imgs\\exit.png",
                    "accelerator": "Alt+F4",
                },
            },
            # "Config": {
            #     "Set Key": {
            #         "command": self.edit_key,
            #         "image": "",
            #         "accelerator": "Ctrl+K",
            #     }
            # }
        }

        # Main Menu Bar
        menubar = Menu(self, tearoff=0, font=("Consolas", 12))

        # Add to menu bars
        for label, layout in layouts.items():
            menu = Menu(self, tearoff=0, cursor="hand1", font=("Consolas", 10))
            menubar.add_cascade(label=label, menu=menu)
            for name, data in layout.items():
                if "-" in name:
                    menu.add_separator()
                else:
                    menu.add_command(
                        label=name,
                        compound="left",
                        command=data["command"],
                        accelerator=data["accelerator"],
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )
        self.configure(background=DARK_GRAY, menu=menubar)
