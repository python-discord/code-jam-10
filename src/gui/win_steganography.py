from tkinter import *
from tkinter import filedialog as fd

from PIL import Image, ImageTk

from backend.steganography import ExistingImage
from gui.modules import DARK_GRAY, dynamic_menu_bar, key_popup


class SteganographyWin(Frame):
    """Window for steganography"""

    def __init__(self, root, filename):
        """Creates the layout"""
        self.root = root
        # Image and backend
        self.image = Image.open(filename)
        self.steganography = ExistingImage(self.image, root.key)
        self.file = None
        # create the window
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title("New File - Steganography")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=25)
        root.bind("<Configure>", self.updatecanvas)
        # split layout
        self.mainframe = Frame(self, bg=DARK_GRAY)
        self.text = Text(
            self.mainframe,
            width=30,
            height=16,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(
            self.mainframe, image=ImageTk.PhotoImage(self.image), bg=DARK_GRAY
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {root.key} | (Click to Copy)")

        self.info = StringVar()
        self.info.set("0 characters")
        self.text.pack(side="left", expand=True, fill="both", anchor="w")
        self.canvas.pack(side="right", anchor="e")
        self.mainframe.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.key_status = Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white")
        self.key_status.grid(row=1, column=0, sticky="w")
        self.key_status.bind("<Button-1>", self.copy_key_to_clipboard)

        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        self._updateinfo()

    def copy_key_to_clipboard(self, _event):
        """Copies key used to encrypt images to the clipboard"""
        # Copying to clipboard
        self.clipboard_clear()
        self.clipboard_append(self.root.key)
        # Updating UI
        self.key.set(f"Secret Key: {self.root.key} | (Copied)")
        self.root.after(
            2000, lambda: self.key.set(f"Secret Key: {self.root.key} | (Click to Copy)")
        )

    def _updateinfo(self):
        """Updates text length"""
        textlen = len(self.text.get(1.0, "end"))
        self.info.set(f"{textlen} characters")
        self.after(10, self._updateinfo)

    def updatecanvas(self, event=None):
        """Updates the image to fit window size"""
        w, h = self.mainframe.winfo_width() // 2, self.mainframe.winfo_height()
        if w * h < 100:  # not rendered yet
            w, h = 100, 100
        thumbnail = self.image.copy()
        thumbnail.thumbnail((w, h))
        img = ImageTk.PhotoImage(thumbnail, Image.BOX)
        self.canvas.configure(image=img, width=w, height=h)
        self.canvas.image = img

    def open(self):
        """Opens selected image"""
        filename = fd.askopenfilename(
            title="Select Image", filetypes=[("All", "*.png")]
        )
        if filename:
            self.file = filename
            self.root.title(f"{filename} - Steganography")
            self.image = Image.open(filename)
            self.steganography.__init__(self.image, self.key)
            self.updatecanvas()

    def export(self):
        """Exports the encoded image"""
        self.steganography.text = self.text.get(1.0, "end")
        encoded_image = self.steganography.encode()
        result = Image.fromarray(encoded_image)
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("All", "*.png")])
        result.save(filename)

    def edit_key(self):
        """Changes encryption key"""

        def after():
            self.steganography = ExistingImage(self.image, self.root.key)
            self.key.set(f"Secret Key: {self.root.key} | (Click to Copy)")

        key_popup(self.root, after)
