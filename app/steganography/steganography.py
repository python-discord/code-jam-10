from functools import cached_property
from pathlib import Path
from typing import Protocol

import PIL
from PIL.Image import Image as PILImage


class Image:
    """Image represents images to be encoded with data using steganography"""

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__image = PIL.Image.open(str(filename)).convert('RGB')

    def __iter__(self):
        """Iterate over the image's pixels."""
        return iter(self.image.getdata())

    @property
    def image(self) -> PILImage:
        """Get the image"""
        return self.__image

    @cached_property
    def max_bytes(self) -> int:
        """Maximum number of bytes that can be encoded in the image"""
        shape = self.__image.size
        return (shape[0] * shape[1] * 3) // 8

    def can_encode(self, b: bytes) -> bool:
        """Check whether the given bytes can be encoded in the image

        Args:
            b (bytes): bytes to be encoded in the image

        Returns:
            bool: whether the given bytes can be encoded in the image
        """
        return len(b) <= self.max_bytes

    @property
    def pixels(self) -> list[list[int]]:
        """Get the pixels of the image

        Returns:
            list[list[int]]: Array of pixels in the image, where each pixel is a list of integers
        """
        return list([list(rgb) for rgb in self.image.getdata()])

    @pixels.setter
    def pixels(self, newdata: list[list[int]]):
        """Set the pixels of the image

        Args:
            newdata (list[list[int]]): Array of pixels to set in the image, where each pixel is a list of integers
        """
        newdata = list([tuple(rgb) for rgb in newdata])
        self.image.putdata(newdata)


    def save(self, file: Path):
        """Save the image to the given file

        Args:
            file (Path): File to save the image to
        """
        # Saving as JPEG breaks encoding due to lossy compression.
        self.image.save(file, format="PNG")


class Steganography(Protocol):
    """Steganography Interface"""

    def encode(self, text: str, img: Image):
        """Encode the text into the image.

        The image is mutated with the encoded data.
        The file is not overwritten and the mutated image can be saved to a new file
        with `Image.save`.

        Args:
            text (str): Text to encode
            img (Image): Image to encode text in
        """
        ...

    def decode(self, img: Image) -> str:
        """Decode the text from the image.

        Args:
            img (Image): Image to decode text from

        Returns:
            str: Text decoded from the image
        """
        ...


def encode(text: str, infile: Path, outfile: Path, algorithm: Steganography):
    """Encode the text in the infile using the given steganography algorithm and save it to outfile.

    Args:
        text (str): Text to encode
        infile (Path): File to encode the text in
        outfile (Path): File to save the image with the encoded text
        algorithm (Steganography): Steganography algorithm to use
    """
    img = Image(infile)
    algorithm.encode(text, img)
    img.save(outfile)


def decode(file: Path, algorithm: Steganography) -> str:
    """Decode the text in the file using the given steganography algorithm

    Args:
        file (Path): File to decode
        algorithm (Steganography): Steganography algorithm to use

    Returns:
        str: decoded message
    """
    return algorithm.decode(Image(file))
