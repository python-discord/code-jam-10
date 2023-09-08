import tkinter as tk
from itertools import count, cycle

from PIL import Image, ImageTk

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"

PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t"


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs

    Source: https://pythonprogramming.altervista.org/animate-gif-in-tkinter/
    The code was modified to fit the needs of this application
    """

    def load(self, im: str, repeat: bool = False, after_exec=None):
        """Loads an image"""
        self.im = im
        self.after_exec = after_exec
        im = Image.open(im)
        self.og_frames = []
        try:
            for i in count(1):
                self.og_frames.append(ImageTk.PhotoImage(im))
                im.seek(i)
        except EOFError:
            pass
        self.frames = (
            cycle(self.og_frames) if repeat else iter(self.og_frames)
        )  # If img needs to be cycled
        try:
            self.delay = im.info["duration"]
        except Exception:
            self.delay = 100
        if len(self.og_frames) == 1:  # If image is not a gif
            self.config(image=next(self.frames))
        else:  # If image is gif
            self.next_frame()

    def unload(self):
        """Unloads the iamge"""
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """Updates the image frame (if gif)"""
        if self.frames:
            try:
                self.config(image=next(self.frames))
                self.after(self.delay, self.next_frame)
            except StopIteration:
                if self.after_exec:
                    self.after_exec()


def center(root: tk.Tk, WIN_W: int, WIN_H: int):
    """Centers a tkinter window"""
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = int((width - WIN_W) / 2)
    y = int(
        (height - WIN_H) / 3
    )  # A bit off center to align it well with the taskbar
    root.geometry(f"+{x}+{y}")


def dynamic_menu_bar(root: tk.Tk, win: classmethod):
    """Packs the menubar for the application"""
    """
        root = Tk root object
        win = The class method to be called
    """
    from gui.win_decrypt import DecryptWin
    from gui.win_steganography import SteganographyWin
    from gui.win_typingcolors import TypingColorsWin

    layouts = {
        "Import": {
            "command": win.open,
            "accelerator": "Ctrl+O",
            "state": "normal"
        },
        "Export": {
            "command": win.export,
            "accelerator": "Ctrl+I",
            "state": "normal"
        },
        "Set Key": {
            "command": root.edit_key,
            "accelerator": "Ctrl+K",
            "state": "normal"
        },
        "--": "",
        "Encrypt": {
            "dropdown": {
                "Typing Colors": {
                    "command": lambda: TypingColorsWin.__init__(TypingColorsWin),
                    "accelerator": "Ctrl+T",
                    "state": "disabled" if win.__class__.__name__ == "TypingColorsWin" else "active"
                },
                "Steganograpy": {
                    "command": lambda: SteganographyWin.__init__(SteganographyWin),
                    "accelerator": "Ctrl+S",
                    "state": "disabled" if win.__class__.__name__ == "SteganographyWin" else "active"
                }
            }
        },
        "Decrypt": {
            "command": lambda: DecryptWin.__init__(DecryptWin, root),
            "accelerator": "Ctrl+D",
            "state": "disabled" if win.__class__.__name__ == "DecryptWin" else "active"
        }
    }

    # Main Menu Bar
    menubar = tk.Menu(root, tearoff=0, font=("Consolas", 12))

    # Add to menu bars
    for name, data in layouts.items():
        menu = tk.Menu(
            root,
            tearoff=0,
            cursor="hand1",
            font=("Consolas", 10),
        )
        if "-" in name:
            menubar.add_separator()
        else:
            try:
                if dropdown := data["dropdown"]:
                    for label, layout in dropdown.items():
                        menu.add_command(
                            label=label,
                            command=layout["command"],
                            accelerator=layout["accelerator"],
                            state=layout["state"],
                            activeforeground=WHITE if layout["state"] == "active" else GRAY,
                            activebackground=GRAY if layout["state"] == "active" else WHITE,
                        )
                    menubar.add_cascade(
                        label=name,
                        menu=menu,
                        compound="left",
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )
            except KeyError:
                menubar.add_command(
                    label=name,
                    command=data["command"],
                    accelerator=data["accelerator"],
                    state=data["state"],
                    activeforeground=WHITE,
                    activebackground=GRAY,
                )
    root.configure(background=DARK_GRAY, menu=menubar)


def edit_key(root):
    """Opens a new window to change the secret key"""
    popup = tk.Toplevel(root)
    popup.title("Edit Key - Pixel Studios")
    popup.geometry("350x150")
    popup.configure(background=GRAY)
    center(popup, 350, 150)


def callback(callback: callable, destroy: list[tk.Widget] = None, *args):
    """Callback a function while destroying existing widgets"""
    if (
        len(destroy) > 0
    ):  # Destroy the previous image labels for a fresh home screen application.
        for i in destroy:
            i.destroy()
    callback(*args)
