from functools import cached_property
from pathlib import Path

import byteutils
import cv2


class Image:
    """Image represents images to be encoded with data using steganography"""

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__image = cv2.imread(str(filename))

    def __iter__(self):
        return iter(self.image)

    @property
    def image(self) -> cv2.typing.MatLike:
        """Get the image"""
        return self.__image

    @cached_property
    def max_bytes(self) -> int:
        """Maximum number of bytes that can be encoded in the image"""
        shape = self.__image.shape
        return (shape[0] * shape[1] * 3) // 8

    def can_encode(self, b: bytes) -> bool:
        """Check whether the given bytes can be encoded in the image

        Args:
            b (bytes): bytes to be encoded in the image

        Returns:
            bool: whether the given bytes can be encoded in the image
        """
        return len(b) <= self.max_bytes

    def save(self, file: Path) -> bool:
        """Save the image to the given file

        Args:
            file (Path): File to save the image to

        Returns:
            bool: Whether the save was successful
        """
        return cv2.imwrite(str(file), self.image)


def _encode(text: str, img: Image) -> Image:
    """Encode the text in the image.

    Args:
        text (str): text to encode in the image
        img (Image): Image to encode the text in

    Raises:
        ValueError: If the input text cannot be encoded in the image.

    Returns:
        Image: Image that has the given text encoded in it
    """
    bytes_input = text.encode()

    if not img.can_encode(bytes_input):
        raise ValueError("Input text exceeds the maximum bytes that can be encoded")

    bits = byteutils.iter_bits(bytes_input)
    for row in img:
        for pixel in row:
            for idx, channel in enumerate(pixel):
                try:
                    bit = next(bits)
                    if bool(bit):
                        print(f"{channel} | {bit} = {channel | bool(bit)}")
                        pixel[idx] = channel | bool(bit)
                    else:
                        print(f"{channel} & {bit} = {channel & bool(bit)}")
                        pixel[idx] = channel & bool(bit)
                except StopIteration:
                    return img


def encode(text: str, infile: Path, outfile: Path):
    """Encode the text in the infile and save it to outfile.

    Args:
        text (str): Text to encode
        infile (Path): File to encode the text in
        outfile (Path): File to save the image with the encoded text
    """
    img = Image(infile)
    img = _encode(text, img)
    img.save(outfile)


if __name__ == "__main__":
    encode("hello", Path("car.jpg"), Path("out.jpg"))
