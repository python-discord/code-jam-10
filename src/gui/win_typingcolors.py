from tkinter import *
from tkinter import filedialog as fd
from gui.modules import *


class TypingColorsWin():
    """Window for typingcolors"""

    def __init__(self, root: Tk, typingcolors: classmethod, key: str):
        """Creates the layout"""
        # super().__init__()
        self.root = root
        dynamic_menu_bar(self.root, self)
        # self.create_menu_bar()
        self.typingColors = typingcolors  # the main backend
        self.file = None  # open files
        self.root.title("New File - Typing Colors")
        # split layout
        self.text = Text(
            self.root,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(self.root, image=self.typingColors.img_scaled(), bg=DARK_GRAY)
        self.key = StringVar()
        self.key.set(f"Secret Key: {key}")
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.canvas.grid(row=0, column=1, sticky="ne")
        Label(self.root, textvariable=self.key, bg=DARK_GRAY, fg="white").grid(
            row=0, column=1, sticky="e"
        )
        Label(self.root, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        # start the loop
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt: str):
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
        self.root.after(50, lambda: self._typingcolors_update(txt))

    def open(self):
        """Opens and loads a selected text file"""
        filename = fd.askopenfilename(title="Open", filetypes=[("All", "*.*")])
        if filename:
            content = open(filename, "r").read()
            self.file = filename
            self.root.title(f"{filename} - Typing Colors")
            self.text.delete(1.0, "end")
            self.text.insert("end", content)
            self.typingColors.update(content)

    def export(self):
        """Exports the canvas to a PNG"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("PNG", "*.png")])
        if filename:
            self.typingColors.canvas.save(filename, format="PNG")

    def edit_key(self):
        """Opens a new window to change the secret key"""
        popup = Toplevel(self.root)
        popup.geometry("300x100")
        center(popup)