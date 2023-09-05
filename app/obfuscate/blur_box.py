from PIL.Image import Image as PILImage

from .obfuscate import Obfuscate


class BlurBox(Obfuscate):
    """BlurBox is a form of obfuscation where it blurs all pixels in a given bounding box."""

    def hide(self, box: tuple[int, int, int, int], image: PILImage):
        """Hide the pixels in the bounding box given in the image.

        Expects the bounding box to be valid for the image.

        Args:
            box (tuple[int, int, int, int]): Bounding box to obfuscate
            image (PILImage): Image to obfuscate
        """
        raise NotImplementedError("TODO: implement blur obfuscation")
