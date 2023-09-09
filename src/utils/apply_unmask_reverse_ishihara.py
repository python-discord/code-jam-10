from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap

from lib.reverse_ishihara.reverse_ishihara import unmask_reverse_ishihara
from src.utils.lru_cache import LRUCache

# Create a cache for storing images:
_image_cache = LRUCache(capacity=10)  # Cache capacity of 10 images


def apply_unmask_reverse_ishihara(args: dict) -> QPixmap:
    """
    Apply unmask reverse Ishihara to an image

    :param args: dict
    :return:
    """
    try:
        if "A" in args:
            slider_a = int(args["A"])
        else:
            slider_a = 0
        if "B" in args:
            slider_b = int(args["B"])
        else:
            slider_b = 0

        img_path = str(args["image_to_edit"])
        if not (_img := _image_cache.get(img_path)):
            _img = Image.open(img_path)
            _image_cache.put(img_path, _img)
        img = _img

        # Apply unmask reverse Ishihara with values from sliders
        unmasked_image = unmask_reverse_ishihara(img, slider_a, slider_b)
        # unmasked_image.save("unmasked.png")

        # unmasked_image = unmasked_image.convert('RGBA')
        #
        # data = unmasked_image.tobytes('raw', 'BGRA')
        # q_image = QImage(data, unmasked_image.size[0], unmasked_image.size[1], QImage.Format.Format_RGBA8888)
        # pixmap = QPixmap.fromImage(q_image)
        # resized_pixmap = pixmap.scaled(450, 450)

        q_image = ImageQt(unmasked_image)
        pixmap = QPixmap.fromImage(q_image)
        resized_pixmap = pixmap.scaled(450, 450)

        return resized_pixmap
    except Exception as e:
        print(e)
        return QPixmap()  # Return an empty QPixmap
