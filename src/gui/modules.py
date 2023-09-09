from tkinter import *

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t"


def loading_animation(root, after, *args):
    """Animates the loading screen"""

    def drawtext(text):
        """Draws the text"""

        def dropletter(letter, n, after_drop, *after_args):
            """Animates a single letter"""
            if n > 30:
                after_drop(*after_args)
                return
            canvas.scale(letter, 790 - 55 * len(text), 240, 0.9, 0.9)
            root.after(10, lambda: dropletter(letter, n + 1, after_drop, *after_args))

        if not text:  # animation complete
            root.after(1000, lambda: after(*args))
            return
        if text[0] == " ":  # skip spaces
            drawtext(text[1:])
            return
        # render next letter
        dropletter(
            canvas.create_text(
                400, 0, text=text[0], fill="white", font=("Cascadia Mono", 66)
            ),
            0,
            lambda: drawtext(text[1:]),
        )

    canvas = Canvas(root, bg=DARK_GRAY)
    canvas.pack(fill="both", expand=True)
    drawtext("Pixel Studios")


def center(root: Tk, WIN_W: int, WIN_H: int):
    """Centers a tkinter window"""
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = int((width - WIN_W) / 2)
    y = int((height - WIN_H) / 3)  # A bit off center to align it well with the taskbar
    root.geometry(f"+{x}+{y}")


def dynamic_menu_bar(root: Tk, win: classmethod):
    """Packs the menubar for the application"""
    """
        root = Tk root object
        win = The class method to be called
    """
    layouts = {
        "Import": {"command": win.open, "accelerator": "Ctrl+O", "state": "normal"},
        "Export": {"command": win.export, "accelerator": "Ctrl+I", "state": "normal"},
        "Set Key": {
            "command": win.edit_key,
            "accelerator": "Ctrl+K",
            "state": "normal",
        },
        "--": "",
        "Encrypt": {
            "dropdown": {
                "Typing Colors": {
                    "command": root.switch_typingcolors,
                    "accelerator": "Ctrl+T",
                    "state": "disabled"
                    if win.__class__.__name__ == "TypingColorsWin"
                    else "normal",
                },
                "Steganograpy": {
                    "command": root.switch_steganography,
                    "accelerator": "Ctrl+S",
                    "state": "disabled"
                    if win.__class__.__name__ == "SteganographyWin"
                    else "normal",
                },
            }
        },
        "Decrypt": {
            "command": root.switch_decrypt,
            "accelerator": "Ctrl+D",
            "state": "disabled" if win.__class__.__name__ == "DecryptWin" else "normal",
        },
    }

    # Main Menu Bar
    menubar = Menu(root)

    # Add to menu bars
    for name, data in layouts.items():
        menu = Menu(
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
                            activeforeground=WHITE
                            if layout["state"] == "normal"
                            else GRAY,
                            activebackground=GRAY
                            if layout["state"] == "normal"
                            else WHITE,
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


def key_popup(root, after_exec):
    """Opens up an edit key window"""

    def enter_key():
        if not root._valid_key():
            return
        after_exec()
        root.popup.destroy()

    root.popup = Toplevel(root, bg=DARK_GRAY)

    # Centering the popup in the center of the window
    w = 350
    h = 200
    x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)

    root.popup.geometry(f"{w}x{h}+{x}+{y}")

    # ? if you want to show the previous key as default value in the pop uncomment next line
    root.key_method_text = StringVar(root.popup, "")
    root.key_method = Entry(
        root.popup,
        width=25,
        font=("Consolas", 12),
        bd=0,
        textvariable=root.key_method_text,
    )
    root.key_method.pack(pady=30)
    root.popup.bind("<Return>", lambda e: enter_key())

    root.error = Label(
        root.popup,
        text="",
        font=("Consolas", 10, "bold"),
        bg=DARK_GRAY,
        fg=BRIGHT_RED,
        pady=2,
    )
    root.error.pack()
    submit = Button(
        root.popup,
        text="Edit Key",
        font=("Consolas", 12, "bold"),
        bg=GREEN,
        fg=WHITE,
        padx=5,
        pady=3,
        cursor="hand2",
        bd=0,
        command=enter_key,
    )
    submit.pack()
