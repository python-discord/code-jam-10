from tkinter import *
from tkinter import filedialog as fd

from PIL import ImageTk

from backend.typingcolors import TypingColors
from gui.modules import *


class DecryptWin(Frame):
    """Window for decryption"""

    def __init__(self, root, object, decoded_text):
        """Creates the layout"""
        # identify mode and set image
        self.root = root
        if isinstance(object, TypingColors):
            self.mode = "Typing Colors"
            self.image = object.canvas
            self.ar_width, self.ar_height = object.ar_width, object.ar_height
        else:
            self.mode = "Steganography"
            self.image = Image.fromarray(object.input_image)
            self.aspect_ratio = self.image.width / self.image.height
        # create window
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title(f"Decrypted - {self.mode}")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=25)

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
        self.text.insert("end", decoded_text)
        self.text.configure(state="disabled")
        self.canvas = Label(
            self.mainframe, image=ImageTk.PhotoImage(self.image), bg=DARK_GRAY
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {root.key}")
        self.info = StringVar()
        self.info.set(f"{len(decoded_text)} characters   |   {self.image.width}px x {self.image.height}px")
        self.canvas.pack(side="left", fill="both", anchor="w")
        self.text.pack(side="right", expand=True, fill="both", anchor="ne")
        self.mainframe.grid(row=0, column=0, columnspan=2, sticky='nsew')
        Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white").grid(
            row=1, column=0, sticky="w"
        )
        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        root.bind("<Configure>", self.updatecanvas)

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        if self.mode == "Typing Colors":
            sf = max(1, (self.grid_bbox(0, 0)[3]) // self.ar_height)
            w, h = int(self.ar_width*sf), int(self.ar_height*sf)
        else:
            if self.aspect_ratio < 1:  # tall image, use width
                sf = max(1, self.grid_bbox(0, 0)[2] // self.image.width)
            else:  # opposite
                sf = max(1, self.grid_bbox(0, 0)[3] // self.image.height)
            w, h = int(self.image.width*sf), int(self.image.height*sf)
        img = ImageTk.PhotoImage(self.image.resize((w, h), Image.BOX))
        self.canvas.configure(image=img, width=w, height=h)
        self.canvas.image = img

    def open(self):
        """Opens and loads a selected image file"""
        self.root.decrypt(self.root.key)

    def export(self):
        """Exports the decrypted text to a file"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("TXT", "*.txt")])
        if filename:
            open(filename, 'w').write(self.text.get(1.0, 'end'))

    def edit_key(self):
        """Edits decryption key"""
        key_popup(self.root, lambda: self.root.decrypt(self.root.key))
