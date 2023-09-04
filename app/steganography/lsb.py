from .. import byteutils
from .steganography import Image, Steganography

EOM = "$$$"


class Lsb(Steganography):
    """Least Significant Bit Implementation of Steganography"""

    def encode(self, text: str, img: Image):
        """Encode the text in the image.

        The image is mutated by this function so a new image is not created.
        The file is not overwritten and the mutated image can be saved to a new file
        with `Image.save`.

        Args:
            text (str): text to encode in the image
            img (Image): Image to encode the text in

        Raises:
            ValueError: If the input text cannot be encoded in the image.
        """
        bytes_input = (text + EOM).encode()

        if not img.can_encode(bytes_input):
            raise ValueError("Input text exceeds the maximum bytes that can be encoded")

        bits = byteutils.iter_bits(bytes_input)
        pixel_data = img.pixels
        for pixel in pixel_data:
            for idx, channel in enumerate(pixel):
                try:
                    bit = next(bits)
                    if bool(bit):
                        pixel[idx] = byteutils.set_bit(channel, 0)
                    else:
                        pixel[idx] = byteutils.clear_bit(channel, 0)
                except StopIteration:
                    img.pixels = pixel_data
                    return

    def decode(self, img: Image) -> str:
        """Decode the text from the image

        Args:
            img (Image): Image to decode text from

        Returns:
            str: Text decoded from the image
        """
        char = 0
        bit_idx = 7
        text = ""
        for pixel in img:
            for channel in pixel:
                lsb = channel & 1
                char += (2**bit_idx) * lsb
                bit_idx = (bit_idx - 1) % 8
                if bit_idx == 7:
                    text += chr(char)
                    char = 0
                    if text.endswith(EOM):
                        return text[: -len(EOM)]
