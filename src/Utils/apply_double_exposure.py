import io
from collections import OrderedDict

from PIL import Image
from PyQt6.QtCore import QBuffer
from PyQt6.QtGui import QImage, QPixmap

from lib.double_exposure.double_exposure import double_exposure


class LRUCache:
    """LRU Cache implementation using OrderedDict"""

    def __init__(self, capacity: int) -> None:
        self.cache: OrderedDict[str, Image] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Image:
        """
        Get an item from the cache

        :param key:
        :return:
        """
        if key not in self.cache:
            return None
        else:
            # Move the accessed entry to the end
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: Image) -> None:
        """
        Put an item in the cache

        :param key:
        :param value:
        :return:
        """
        if key in self.cache:
            # If entry is found, remove it and re-insert at the end
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            # If the cache is at capacity, remove the first (oldest) item
            self.cache.popitem(last=False)
        self.cache[key] = value


# Now integrate the LRUCache into your previous function:
_image_cache = LRUCache(capacity=10)  # Cache capacity of 10 images


def apply_double_exposure(img1: tuple, img2: tuple, slider_value: int) -> QPixmap:
    """
    Apply double exposure to an image

    :param img1:
    :param img2:
    :param slider_value:
    :return:
    """
    img1_path = str(img1)
    if not (_img := _image_cache.get(img1_path)):
        _img = Image.open(img1_path)
        _image_cache.put(img1_path, _img)
    img1 = _img

    img2_path = str(img2)
    if not (_img := _image_cache.get(img2_path)):
        _img = Image.open(img2_path)
        _image_cache.put(img2_path, _img)
    img2 = _img

    # Convert slider value to float between 0 and 1
    adjusted_slider_value = float(slider_value*5) / 100

    # Apply double exposure
    blended_image = double_exposure(img1, img2, adjusted_slider_value)

    # Convert blended PIL image to QPixmap
    blended_image_rgba = blended_image.convert("RGBA")
    data = blended_image_rgba.tobytes("raw", "BGRA")
    qim = QImage(data, blended_image.width, blended_image.height, QImage.Format.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)

    return pixmap


def qimage_to_pil_image(qimage: QImage) -> Image:
    """Converts a PyQt QImage to a PIL Image."""
    buffer = QBuffer()
    buffer.open(QBuffer.OpenModeFlag.ReadWrite)
    qimage.save(buffer, "PNG")
    pil_im = Image.open(io.BytesIO(bytes(buffer.data())))
    return pil_im
