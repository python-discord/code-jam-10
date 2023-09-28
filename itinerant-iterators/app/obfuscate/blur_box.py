from PIL import ImageFilter
from PIL.Image import Image as PILImage
from PIL.ImageFilter import Filter

from .obfuscate import Obfuscate


class BlurBox(Obfuscate):
    """BlurBox is a form of obfuscation where it blurs all pixels in a given bounding box."""

    def __init__(
        self,
        iterations: int = 20,
        image_filter: Filter = ImageFilter.BoxBlur(radius=10),
    ):
        """Create a new blur obfuscator

        Args:
            iterations (int, optional): Number of blur iterations to apply to the bounding box. Defaults to 20.
            image_filter (Filter, optional): Filter to apply for bluaring. Defaults to box blur blur with radius 10.
        """
        self.__iterations = iterations
        self.__image_filter = image_filter

    def hide(self, box: tuple[int, int, int, int], image: PILImage):
        """Hide the pixels in the bounding box given in the image.

        Expects the bounding box to be valid for the image.

        Args:
            box (tuple[int, int, int, int]): Bounding box to obfuscate
            image (PILImage): Image to obfuscate
        """
        section = image.crop(box=box)
        for i in range(self.__iterations):
            section = section.filter(self.__image_filter)
        image.paste(section, box=box)
        return image
