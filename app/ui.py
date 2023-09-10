import io
from enum import StrEnum

import PySimpleGUI as sg
from PIL import Image

from app import steganography
from app.obfuscate.blur_box import BlurBox
from app.obfuscate.colour_box import ColourBox
from app.obfuscate.find_bounds import find_bounds


class UIKey(StrEnum):
    """Collection of keys on the UI"""

    WATERMARK_TEXT_INPUT = "-WATERMARK-TEXT-INPUT-"
    WATERMARK_ENCODING_MODE = "-WATERMARK-ENCODING-MODE-"
    APPLY_WATERMARK = "-APPLY-WATERMARK-"
    VIEW_WATERMARK = "-VIEW-WATERMARK-"
    APPLY_OBFUSCATE = "-APPLY-OBFUSCATE-"
    OBFUSCATE_TEXT_INPUT = "-OBFUSCATE-TEXT-INPUT-"
    WATERMARK_FRAME = "-WATERMARK-"
    OBFUSCATE_FRAME = "-OBFUSCATE-"
    IMAGE = "-IMAGE-"
    IMAGE2 = "-IMAGE2-"


def main():
    """Main entry point of the UI"""
    sg.set_options(element_padding=(0, 0))
    image = Image.new("RGB", (600, 400))
    mode = "watermark"

    # ------ Menu Definition ------ #
    menu_def = [
        ["File", ["Open", "Save", "Exit"]],
        ["Mode", ["Obfuscate", "Watermark"]],
        ["Help", ["About", "Member List"]],
    ]

    # ------ WaterMark Frame Defintion ------ #
    watermark_frame = [
        [sg.Text("Press 'File > Open' select image to start.", size=(40, 1))],
        [
            sg.Image(
                key=UIKey.IMAGE,
                size=(600, 400),
                pad=(2, (2, 20)),
                tooltip="Press 'File > Open' select image to start.",
            )
        ],
        [
            sg.Text("Enter text:", size=(8, 1)),
            sg.Input(
                "",
                (38, 1),
                focus=True,
                tooltip="Enter text for watermark.",
                pad=((2, 5), 2),
                key=UIKey.WATERMARK_TEXT_INPUT,
            ),
            sg.Combo(
                ["LSB Linear", "LSB Uniform"],
                size=(9, 1),
                key=UIKey.WATERMARK_ENCODING_MODE,
                default_value="LSB Linear",
            ),
            sg.Button(
                "Apply", key=UIKey.APPLY_WATERMARK, size=(8, 1), pad=((24, 0), 2)
            ),
            sg.Button("View", key=UIKey.VIEW_WATERMARK, size=(8, 1), pad=((24, 0), 2)),
        ],
    ]

    # ------ Obfuscation Frame Defintion ------ #
    obfuscation_frame = [
        [sg.Text("Press 'File > Open' select image to start.", size=(40, 1))],
        [
            sg.Image(
                key=UIKey.IMAGE2,
                size=(600, 400),
                pad=(2, (2, 20)),
                tooltip="Press 'File > Open' select image to start.",
            )
        ],
        [
            sg.Text("Enter text:", size=(8, 1)),
            sg.Input(
                "",
                (48, 1),
                focus=True,
                tooltip="Enter text for obfuscation.",
                pad=((2, 5), 2),
                key=UIKey.OBFUSCATE_TEXT_INPUT,
            ),
            sg.Radio("Box", "obfus-type", key="box", default=True, size=(3, 1)),
            sg.Radio("Blur", "obfus-type", key="blur", size=(3, 1)),
            sg.Button("Apply", key=UIKey.APPLY_OBFUSCATE, size=(8, 1), pad=((5, 0), 2)),
        ],
    ]

    # ------ GUI Defintion ------ #
    layout = [
        [
            sg.Menu(
                menu_def,
            )
        ],
        [
            sg.Frame(
                "Watermark", watermark_frame, size=(600, 500), key=UIKey.WATERMARK_FRAME
            ),
            sg.Frame(
                "Obfuscation",
                obfuscation_frame,
                size=(600, 500),
                key=UIKey.OBFUSCATE_FRAME,
                visible=False,
            ),
        ],
    ]

    window = sg.Window(
        "Itinerant iterators v1.0(alpha)",
        layout,
        default_element_size=(12, 1),
        auto_size_text=False,
        auto_size_buttons=False,
        default_button_element_size=(12, 1),
        element_justification="c",
    )

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        # ------ Process menu choices ------ #
        if event == "About":
            # Pop up to show application description
            sg.popup(
                "Itinerant iterators Version 1.0",
                "--------------------------------------------------------------------",
                "This is a GUI tool for obfuscation and steganography.",
                "Power by PySimpleGUI",
                title="About",
                line_width=500,
            )
        elif event == "Member List":
            # Pop up to show member list
            sg.popup(
                "Memeber list",
                "--------------------------------------------------------------------",
                "smileyface12349\t\t",
                "jj-style\t\t",
                "HiPeople21\t\t",
                "CactusBrothers\t\t",
                "cloki0610",
                title="Member List",
                line_width=500,
            )
        elif event == "Open":
            # Open a popup to select file
            filename = sg.popup_get_file(
                "file to open",
                no_window=True,
                file_types=(("All Picture Files", "*.jpg *.png *.jpeg"),),
            )
            print(filename)
            if filename:
                # Open Image
                image = Image.open(filename)
                bio = _get_image_for_ui(image)
                if mode == "watermark":
                    window[UIKey.IMAGE].update(bio.getvalue())
                elif mode == 'obfuscate':
                    window[UIKey.IMAGE2].update(bio.getvalue())

        elif event == "Save":
            # Open a popup to save image
            if image:
                filename = sg.popup_get_file(
                    "file to save",
                    no_window=True,
                    save_as=True,
                    default_extension=".png",
                    file_types=(("JPG", "*.jpg"), ("PNG", "*.png")),
                )
                if filename:
                    if filename.endswith(".jpg"):
                        image.convert("RGB").save(filename, format="JPEG")
                    else:
                        image.save(filename, format="PNG")
        elif event == "Watermark":
            # Switch to watermark frame
            window[UIKey.WATERMARK_FRAME].update(visible=True)
            window[UIKey.OBFUSCATE_FRAME].update(visible=False)
            mode = "watermark"
        elif event == "Obfuscate":
            # Switch to Obfuscate frame
            window[UIKey.WATERMARK_FRAME].update(visible=False)
            window[UIKey.OBFUSCATE_FRAME].update(visible=True)
            mode = "obfuscate"
        elif event == UIKey.APPLY_WATERMARK:
            text = values[UIKey.WATERMARK_TEXT_INPUT]
            encoding_mode = values[UIKey.WATERMARK_ENCODING_MODE]
            pixel_generator = steganography.lsb.pixels_top_left
            if encoding_mode == "LSB Linear":
                pixel_generator = steganography.lsb.pixels_top_left
            elif encoding_mode == "LSB Uniform":
                sg.Popup("Uniform encoding distribution not implemented")
                continue
            lsb = steganography.Lsb(pixels_generator=pixel_generator)
            steg_image = steganography.Image(filename)
            lsb.encode(text, steg_image)
            image = steg_image.image
            bio = _get_image_for_ui(steg_image.image)
            window[UIKey.IMAGE].update(bio.getvalue())
        elif event == UIKey.VIEW_WATERMARK:
            lsb = steganography.Lsb()
            steg_image = steganography.Image(filename)
            decoded_text = lsb.decode(steg_image)
            if decoded_text is None:
                sg.Popup("Image does not contain any encoded data!")
            else:
                window[UIKey.WATERMARK_TEXT_INPUT].Update(decoded_text)
        elif event == UIKey.APPLY_OBFUSCATE:
            text = values[UIKey.OBFUSCATE_TEXT_INPUT]
            bounds = find_bounds(filename, text)
            # print(text)
            # print(bounds)
            img = Image.open(filename)
            if values["box"] is True:
                colour_box = ColourBox((0, 0, 0))
                for bound in bounds:
                    colour_box.hide(bound, img)
            elif values['blur'] is True:
                blur_box = BlurBox()
                for bound in bounds:
                    blur_box.hide(bound, img)
            bio = _get_image_for_ui(img)
            window[UIKey.IMAGE2].update(bio.getvalue())


def _get_image_for_ui(image: Image) -> io.BytesIO:
    """Gets a resized image in memory to display in the UI

    Args:
        image (Image): PIL Image to display

    Returns:
        io.BytesIO: Buffer of image bytes to display
    """
    tmp_img = image
    # Get image size
    cur_width, cur_height = image.size
    # If image width or height oversize, resize the image
    if cur_width > 600 or cur_height > 400:
        new_width = 600 if cur_width > 600 else cur_width
        new_height = 400 if cur_height > 400 else cur_height
        scale = min(new_height / cur_height, new_width / cur_width)
        tmp_img = image.resize(
            (int(cur_width * scale), int(cur_height * scale)), Image.LANCZOS
        )
    # Create a new bio, and save the image into it as png format
    bio = io.BytesIO()
    tmp_img.save(bio, format="PNG")
    return bio
