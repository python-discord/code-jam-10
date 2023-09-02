from functools import cached_property
from pathlib import Path
from typing import Protocol

import cv2


class Image:
    """Image represents images to be encoded with data using steganography"""

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__image = cv2.imread(str(filename), flags=cv2.IMREAD_UNCHANGED)

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


class Steganography(Protocol):
    """Steganography Interface"""

    def encode(self, text: str, img: Image) -> Image:
        """Encode the text into the image

        Args:
            text (str): Text to encode
            img (Image): Image to encode text in

        Returns:
            Image: Image with the given text encoded
        """
        ...

    def decode(self, img: Image) -> str:
        """Decode the text from the image

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
    img = algorithm.encode(text, img)
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
