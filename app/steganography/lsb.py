from .. import byteutils
from .steganography import Image, Steganography

EOM = "$$$"


class Lsb(Steganography):
    """Least Significant Bit Implementation of Steganography"""

    def encode(self, text: str, img: Image) -> Image:
        """Encode the text in the image.

        Args:
            text (str): text to encode in the image
            img (Image): Image to encode the text in

        Raises:
            ValueError: If the input text cannot be encoded in the image.

        Returns:
            Image: Image that has the given text encoded in it
        """
        bytes_input = (text + EOM).encode()

        if not img.can_encode(bytes_input):
            raise ValueError("Input text exceeds the maximum bytes that can be encoded")

        bits = byteutils.iter_bits(bytes_input)
        for row in img:
            for pixel in row:
                for idx, channel in enumerate(pixel):
                    try:
                        bit = next(bits)
                        if bool(bit):
                            pixel[idx] = byteutils.set_bit(pixel[idx], 0)
                        else:
                            pixel[idx] = byteutils.clear_bit(pixel[idx], 0)
                    except StopIteration:
                        return img

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
        for row in img:
            for pixel in row:
                for channel in pixel:
                    lsb = channel & 1
                    char += (2**bit_idx) * lsb
                    bit_idx = (bit_idx - 1) % 8
                    if bit_idx == 7:
                        text += chr(char)
                        char = 0
                        if text.endswith(EOM):
                            return text[: -len(EOM)]
