from tkinter import *
from tkinter import filedialog as fd

from gui.modules import *


class TypingColorsWin(Frame):
    """Window for typingcolors"""

    def __init__(self, root: Tk, typingcolors: classmethod, key: str):
        """Creates the layout"""
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title("New File - Typing Colors")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        root.bind("<Configure>", self.updatecanvas)

        self.typingColors = typingcolors  # the main backend
        self.file = None  # open files
        # split layout
        self.text = Text(
            self,
            width=30,
            height=16,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(
            self, image=self.typingColors.img_scaled(), bg=DARK_GRAY
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {key}")
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.grid(row=0, column=0, sticky="nsew")
        self.canvas.grid(row=0, column=1, sticky="e")
        Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white").grid(
            row=1, column=0, sticky="nsw"
        )
        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="nse"
        )
        # start the loop
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt: str):
        """Update loop for typingcolours"""
        txt = self.text.get("1.0", "end")
        if txt != prev_txt:  # only update if text changed
            self.typingColors.update(txt)
            self.updatecanvas()
            self.info.set(
                f"{len(txt) - 1} characters   |   {self.typingColors.width}px x {self.typingColors.height}px"
            )
        self.after(50, lambda: self._typingcolors_update(txt))

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        w, h = self.grid_bbox(1, 0)[2:]
        w *= .99
        h *= .99
        if w > h:
            sf = h / self.typingColors.ar_height
        else:
            sf = w / self.typingColors.ar_width
        img = self.typingColors.img_scaled(int(sf))
        self.canvas.configure(image=img)
        self.canvas.image = img

    def open(self):
        """Opens and loads a selected text file"""
        filename = fd.askopenfilename(title="Open", filetypes=[("All", "*.*")])
        if filename:
            content = open(filename, "r").read()
            self.file = filename
            self.winfo_toplevel().title(f"{filename} - Typing Colors")
            self.text.delete(1.0, "end")
            self.text.insert("end", content)
            self.typingColors.update(content)

    def export(self):
        """Exports the canvas to a PNG"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("PNG", "*.png")])
        if filename:
            self.typingColors.save_as(filename)

    def edit_key(self):
        """Opens a new window to change the secret key"""
        popup = Toplevel(self)
        popup.geometry("300x100")
        center(popup)
