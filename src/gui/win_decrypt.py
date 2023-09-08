from tkinter import *
from tkinter import filedialog as fd

from gui.modules import *


class DecryptWin(Frame):
    """Window for decryption"""

    def __init__(self, root, object, text, key):
        """Creates the layout"""
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title("Decrypted - Typing Colors")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        root.bind("<Configure>", self.updatecanvas)

        self.object = object  # the main backend
        self.file = None  # open files
        # split layout
        self.mainframe = Frame(self, bg=DARK_GRAY)
        self.text = Text(
            self.mainframe,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.text.insert("end", text)
        self.text.configure(state="disabled")
        self.canvas = Label(
            self.mainframe, image=self.object.img_scaled(), bg=DARK_GRAY
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {key}")
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.canvas.pack(side="left", fill="both", anchor="w")
        self.text.pack(side="right", expand=True, fill="both", anchor="ne")
        self.mainframe.grid(row=0, column=0, columnspan=2, sticky='nsew')
        Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white").grid(
            row=1, column=0, sticky="w"
        )
        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        sf = max(1, (self.bbox()[3] - 26) / self.object.ar_height)
        img = self.object.img_scaled(int(sf))
        self.canvas.configure(image=img, width=self.object.ar_width*sf, height=self.object.ar_height*sf)
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
