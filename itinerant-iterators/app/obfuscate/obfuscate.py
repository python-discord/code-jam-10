from typing import Protocol

from PIL.Image import Image as PILImage


class Obfuscate(Protocol):
    """Obfuscate defines the behaviour to obfuscate the part of the image given in the bounding box."""

    def hide(self, box: tuple[int, int, int, int], image: PILImage):
        """Hide the pixels in the bounding box given in the image.

        Expects the bounding box to be valid for the image.

        Args:
            box (tuple[int, int, int, int]): Bounding box to obfuscate
            image (PILImage): Image to obfuscate
        """
        ...


def validate_bounding_box(box: tuple[int, int, int, int], image: PILImage) -> bool:
    """Validate whether a bounding box fits within an image

    Args:
        box (tuple[int, int, int, int]): bounding box to test
        image (PILImage): image to check bounding bix against

    Returns:
        bool: whether the image fully contains the bounding box
    """
    size = image.size
    left, up, right, down = box
    return (
        left >= 0
        and right <= size[0]
        and up >= 0
        and down <= size[1]
        and right >= left
        and down >= up
    )
