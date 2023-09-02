import io
import os
import re
from dataclasses import dataclass

from nicegui import events, ui
from PIL import Image


@dataclass
class Filepaths:
    """Class that has file paths of user image, cover image, and output files"""

    user_image_fe = ""
    cover_image_fe = ""

    def get_user_image_fp(self):
        """Get file path for user iamge"""
        return os.path.join("static", f"user_image.{self.user_image_fe}")

    def get_cover_image_fp(self):
        """Get file path for cover image"""
        return os.path.join("static", f"cover_image.{self.cover_image_fe}")

    def get_encrypted_image_output_path(self):
        """Get file path for encrypted output image"""
        return os.path.join("static", f"encrypt_output.{self.cover_image_fe}")

    def get_decrypted_output_file_path(self, text=False):
        """Get file path for decrypted output, either an image or text file"""
        if text:
            return os.path.join("static", "decrypted_output.txt")
        else:
            return os.path.join("static", f"decrypted_output.{self.cover_image_fe}")


def placeholder_function():  # noqa: D103
    pass


# GUI callback functions
def handle_image_upload(img: events.UploadEventArguments, cover=False):
    """Handle user image to encrypt.

    This function will take the image that was uploaded by the user
    and put it in the static file folder of the repository as
    user_image.(file extension of original image)
    or
    cover_image.(file extension of original image)

    param img: object that has uploaded file
    """
    # Get the binary of the tempfile object
    content = img.content.read()
    # Create a pillow image object using the binary
    with Image.open(io.BytesIO(content)) as image:
        image.load()
        rgb_image = image.convert("RGB")
    # Get the extension using regex and check that it is valid
    acceptable_extensions = ["jpg", "png", "jpeg"]
    file_extension = re.search(r"\.([a-zA-Z0-9]+)$", img.name).group(1)
    if file_extension not in acceptable_extensions:
        ui.notify("Not an acceptable file type!")
        return
    # Save the image locally if the file extension is valid
    if cover:
        file_path = os.path.join("static", f"cover_image.{file_extension}")
    else:
        file_path = os.path.join("static", f"user_image.{file_extension}")
    rgb_image.save(file_path)


def encrypt_event(e: events.ClickEventArguments, value: str, text_input: str = None):
    """Function that checks if conditions for encryption are met and calls encrypt fucntion

    This function will check whether text or image is being encrypted into the cover_iamge.
    If it is an image it will first check if the user_image is smaller or equal
    in size to cover_image. If user_image is too large it will resize it to be the same
    size as the cover_image. Then, the appropriate function will be called to encrypt
    either the text or image into the cover_image. The output image will be saved in static
    folder as output_image.(cover image file extension)

    param e: GUI objects for click event.
    param value: String with type of message will be encrypted. Will be "Text" or "Image".
    param text_input: Message to be encrypted into image
    """
    print("Text input:", text_input)
    # File paths for all images
    user_image_fp = "static/user_image.jpg"
    cover_image_fp = "static/cover_image.jpg"
    # Open the cover image
    with Image.open(cover_image_fp) as cimg:
        cimg.load()
    print("cimg:", cimg.size)
    # File path to encrypted image output
    encrypt_output_image_fp = os.path.join("static", f"encrypt_output.{cimg.format}")
    print("output fp:", encrypt_output_image_fp)
    # Check if user image is larger than cover image, resize if it is
    if value == "Image":
        # Open user image
        with Image.open(user_image_fp) as uimg:
            uimg.load()
        print("uimg:", uimg.size)
        # Check sizes
        if uimg.size[0] > cimg.size[0] and uimg.size[1] > cimg.size[1]:
            cimg = cimg.resize(uimg.size)
        # Call function to encrypt user image into cover image
        output_image = placeholder_function(uimg, cimg)
        # Save the output image
        output_image.save(encrypt_output_image_fp)
    else:
        # Check if there is text Input
        if text_input:
            # Call function to encrypt text into cover image
            output_image = placeholder_function(cimg, text_input)
            # Save the output image
            output_image.save(encrypt_output_image_fp)
        else:
            ui.notify("Please input a text message to encrypt!")
            return


def decrypt_event():
    """Function that does procedures for decryption

    Loads up the cover_image gotten from the user
    and calls the decrypt functions. This will output
    the decrypt function outputs into files for display
    in GUI.
    """
    # File path of cover image
    cover_image_fp = "static/cover_image.*"
    decrypt_output_fp = "static/decrypt_output.*"
    # Open the cover image
    with Image.open(cover_image_fp) as cimg:
        cimg.load()
    # Call the function to decrypt text from image
    decrypt_text, end_code_found = placeholder_function(cimg)
    # Save output as text file
    if end_code_found:
        with open(decrypt_output_fp) as f:
            f.write(decrypt_text)
    else:
        # Call the function to decrypt an image from an image
        decrypt_image = placeholder_function(cimg)
        # Save output as an image
        decrypt_image.save(decrypt_output_fp)


# GUI Contents

# Create Filepaths object to keep track of file paths
file_paths = Filepaths()

# Title of the project
ui.label("The Thick Wrappers Steganography Project")

# Prompt user to choose whether to encrypt or decrypt
ui.label("Select Encrpyt/Decrypt:")
dropdown_encrypt_or_decrypt = ui.select(["Encrypt", "Decrypt"], value="Encrypt")

# Card with user input needed for encrypt with encrypt button
with ui.card().bind_visibility_from(dropdown_encrypt_or_decrypt, "value", value="Encrypt"):
    # Prompt the user to select the message type
    with ui.row():
        ui.label("Choose message type:")
        dropdown_text_or_image = ui.select(["Text", "Image"], value="Text")
    # User input needed if text message type is chosen
    with ui.column().bind_visibility_from(dropdown_text_or_image, "value", value="Text"):
        # Prompt the user for the text they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Text:")
            with ui.column():
                text_to_encrypt = ui.textarea(label="Message", placeholder="Hello World")
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            ui.button("Encrypt", on_click=lambda e:
                      encrypt_event(e, dropdown_text_or_image.value, text_to_encrypt.value))
    # User input needed if image message type is chosen
    with ui.column().bind_visibility_from(dropdown_text_or_image, "value", value="Image"):
        # Prompt the user for the image they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Encrypt:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=handle_image_upload)
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            ui.button("Encrypt", on_click=lambda e: encrypt_event(e, dropdown_text_or_image.value))

# Card with user input needed for decrypt with decrypt button
with ui.card().bind_visibility_from(dropdown_encrypt_or_decrypt, "value", value="Decrypt"):
    with ui.column():
        # Prompt the user for the image they want to decrypt
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Decrypt:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            ui.button("Decrypt", on_click=lambda: ui.notify("Decrypted!"))

# Output area
output = ui.image("https://picsum.photos/id/377/640/360")

# Buttons to download or clear output
with ui.row():
    download_button = ui.button("Download", on_click=lambda: ui.notify("Downloaded!"))
    clear_button = ui.button("Clear")

# Initialize and run the GUI
ui.run()
