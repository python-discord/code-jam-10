from tkinter import *
from tkinter import filedialog as fd

from backend.typingcolors import TypingColors
from gui.modules import *


class TypingColorsWin(Frame):
    """Window for typingcolors"""

    def __init__(self, root: Tk):
        """Creates the layout"""
        # create the window
        self.root = root
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title("New File - Typing Colors")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=25)
        root.bind("<Configure>", self.updatecanvas)

        self.typingColors = TypingColors()  # the main backend
        self.typingColors.set_key(root.key)
        self.file = None  # open files
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
        # TODO: CHANGE THE DEFAULT TEXT
        self.text.insert(END, "Edit me !")
        self.canvas = Label(
            self.mainframe,
            image=self.typingColors.img_scaled(0.6 * self.root.winfo_width()),
            bg=DARK_GRAY,
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {root.key} | (Click to Copy)")

        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.pack(side="left", expand=True, fill="both", anchor="w")
        self.canvas.pack(side="right", fill="both", anchor="e")
        self.mainframe.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.key_status = Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white")
        self.key_status.grid(row=1, column=0, sticky="w")
        self.key_status.bind("<Button-1>", self.copy_key_to_clipboard)

        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
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

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        sf = max(1, (self.grid_bbox(0, 0)[3]) // self.typingColors.ar_height)
        img = self.typingColors.img_scaled(int(sf), self.root.winfo_width())
        self.canvas.configure(
            image=img,
            width=self.typingColors.ar_width * sf,
            height=self.typingColors.ar_height * sf,
        )
        self.canvas.image = img

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
            self.typingColors.save_as(filename + ".png")

    def edit_key(self):
        """Editing the encryption key"""

        def after():
            self.typingColors.set_key(self.root.key)
            self.typingColors.force_update()
            self.key.set(f"Secret Key: {self.root.key} | (Click to Copy)")

        key_popup(self.root, after)
