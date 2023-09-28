from tkinter import *

DARK_GRAY, GRAY, WHITE = "#222831", "#393E46", "#EEEEEE"
TYPINGCOLSCOL, STEGCOL, DECRYPTCOL = "#041C32", "#021A30", "#00041F"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t"


def loading_animation(root):
    """Animates the loading screen"""

    def drawtext(text, red=192):
        """Draws the text"""

        def dropletter(letter, n=0):
            """Animates a single letter"""
            if n == 30:  # animation done
                return
            if n == 4:  # start next letter
                drawtext(text[1:], red + 3)  # generate nice spectrum
            canvas.scale(letter, letterx, centery, 0.9, 0.9)  # move towards given position
            root.after(10, lambda: dropletter(letter, n + 1))  # continue animation

        if not text:  # animation complete
            root.after(
                1500,  # create main window
                lambda: root.callback(root.create_main_window),
            )
            return
        if text[0] == " ":  # skip spaces
            drawtext(text[1:], red)
            return
        # render next letter
        letterx = 770 - 36 * len(text)  # calculate letter position
        dropletter(
            canvas.create_text(
                378,
                -42,
                text=text[0],  # start letter at y-42
                fill="#%02x66ff" % red,  # convert to hex
                font=("Cascadia Mono", 42),
            ),
        )

    centery = root.winfo_height() // 2
    canvas = Canvas(
        root,
        bg=DARK_GRAY,
        width=756,
        height=centery + 25,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(relx=0.5, rely=0, anchor="n")
    drawtext("The Neverending Loops")


def center(root: Tk, WIN_W: int, WIN_H: int):
    """Centers a tkinter window"""
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = int((width - WIN_W) / 2)
    y = int((height - WIN_H) / 3)  # A bit off center to align it well with the taskbar
    root.geometry(f"+{x}+{y}")


def dynamic_menu_bar(root: Tk, win: classmethod):
    """Create the menubar for the window"""
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
                    "state": "disabled" if win.__class__.__name__ == "TypingColorsWin" else "normal",
                },
                "Steganograpy": {
                    "command": root.switch_steganography,
                    "accelerator": "Ctrl+S",
                    "state": "disabled" if win.__class__.__name__ == "SteganographyWin" else "normal",
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
                            activeforeground=WHITE if layout["state"] == "normal" else GRAY,
                            activebackground=GRAY if layout["state"] == "normal" else WHITE,
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
                    activebackground=DECRYPTCOL,
                )

    root.configure(background=DARK_GRAY, menu=menubar)


def key_popup(root, after_exec, empty_key=True):
    """Opens up an edit key window"""

    def enter_key(e=None):
        if not root._valid_key(empty_key=empty_key):
            return
        after_exec()
        root.popup.destroy()

    root.popup = Toplevel(root, bg=DARK_GRAY)
    root.popup.title("Enter New Key")

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
    root.popup.bind("<Return>", enter_key)

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
