import io

from PIL import Image, ImageQt
from PyQt6.QtCore import QBuffer
from PyQt6.QtGui import QImage, QPixmap

from lib.double_exposure.double_exposure import double_exposure


def apply_double_exposure(img1: tuple, img2: tuple, slider_value: int) -> QPixmap:
    """
    Apply double exposure to an image

    :param img1:
    :param img2:
    :param slider_value:
    :return:
    """
    img1_path = str(img1)
    img1 = Image.open(img1_path)

    # Get img2 from path and load as Image
    img2_path = str(img2)
    img2 = Image.open(img2_path)

    print(slider_value)

    # Convert slider value to float between 0 and 1
    adjusted_slider_value = float(slider_value*5) / 100
    print(adjusted_slider_value)

    # Apply double exposure
    pil_img = double_exposure(img1, img2, adjusted_slider_value)

    # Convert PIL Image to QPixMap
    qpixmap = ImageQt.toqpixmap(pil_img)

    return qpixmap


def qimage_to_pil_image(qimage: QImage) -> Image:
    """Converts a PyQt QImage to a PIL Image."""
    buffer = QBuffer()
    buffer.open(QBuffer.OpenModeFlag.ReadWrite)
    qimage.save(buffer, "PNG")
    pil_im = Image.open(io.BytesIO(bytes(buffer.data())))
    return pil_im
