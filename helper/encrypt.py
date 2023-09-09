import numpy as np
from PIL import Image

from . import utility
from .constant import BITS_4, Direction

# Added as message end
END_TEXT = ",,,.."
END_BYTES = list(map(ord, END_TEXT))


def encrypt_text_to_image(text: str, image: Image.Image) -> Image.Image | None:
    """
    Encode a text string in randomly selected coordinates of an image

    :param text Message to encrypt.
    :param image Pillow `Image` object in which `text` will be encrypted. Must have only three color planes.

    This function encrypts a string in an image. Non-ASCII characters are
    stripped from the string, and a copy of the image is made. For each character, a pixel of the copy is selected,
    going left and down from the top left corner.
    For each pixel, the 7 bits of the corresponding ASCII code are encoded in
    the three least significant bits
    of each color plane (red, green, blue).
    Blue receives only one bit. The modified copy with the encoded message is
    returned.

    If the input text contains more characters than the image has pixels,
    encryption is impossible, so `None` is returned.
    """
    # Convert to ASCII and add padding indicating message end
    bytes = utility.to_bytes(utility.strip_non_ascii(text.strip())) + END_BYTES
    n = len(bytes)
    cols, rows = image.size
    extent = cols * rows
    # Alert caller if too many bytes to encode
    if n > extent:
        return None

    # Create array from ASCII codes with image's width and height,
    # padded with zeroes
    bytes = np.array(bytes, dtype=np.uint8)
    pixels = np.array(image, dtype=np.uint8)
    mask = np.concatenate(
        (bytes, np.zeros(extent - n, dtype=np.uint8)), dtype=np.uint8
    ).reshape((rows, cols))

    modulus = 2**3
    # Needed to identify which pixels need LSBs cleared
    full_rows = n // cols
    last_row_cols = n % cols

    # First clear all rows where all pixels are used
    pixels[:full_rows, :, :] = utility.clear_least_significant_bits(
        pixels[:full_rows, :, :], 3
    )
    # And last, partially filled row, if it exists
    if full_rows < rows and last_row_cols > 0:
        pixels[full_rows, :last_row_cols, :] = utility.clear_least_significant_bits(
            pixels[full_rows, :last_row_cols, :], 3
        )
    # Add array to each channel to encode bits
    # Red
    pixels[:, :, 0] += mask % modulus
    mask >>= 3
    # Green
    pixels[:, :, 1] += mask % modulus
    mask >>= 3
    # Blue
    pixels[:, :, 2] += mask
    return Image.fromarray(pixels)


def encrypt_image_to_image(cover: Image.Image, secret: Image.Image) -> Image.Image:
    """
    Function encrypts image into image

    Apply image steganography by resetting the cover image's least significant 4 bits,
    take the secret image's most significant 4 bits and add both numpy arrays together
    Sum of arrays is converted back into Pillow Image and returned

    :param cover: Image you want to hide into
    :param secret: Image you want to hide
    :return: A steganography Image object
    """
    cover_asarray = np.asarray(cover)
    secret_asarray = np.asarray(secret)
    cover_msb = utility.shift_image_bits_asarray(cover_asarray, Direction.RIGHT, BITS_4)
    cover_lsb_reset = utility.shift_image_bits_asarray(cover_msb, Direction.LEFT, BITS_4)
    secret_msb = utility.shift_image_bits_asarray(secret_asarray, Direction.RIGHT, BITS_4)
    stega_asarray = cover_lsb_reset.copy()
    if secret_msb.size < cover_lsb_reset.size:
        height, width, _ = secret_msb.shape
        stega_asarray[:height, :width] += secret_msb
    else:
        stega_asarray += secret_msb
    return Image.fromarray(stega_asarray)
