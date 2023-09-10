from PIL import Image


def double_exposure(img1: Image, img2: Image, alpha: float = 0.5) -> Image:
    """
    Blend two images together using alpha blending

    :param img1: PIL Image
    :param img2: PIL Image
    :param alpha: int
    :return:
    """
    # Convert both images to RGB
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Resize img2 to match img1's size
    img2 = img2.resize(img1.size)

    # Blend the images
    blended = Image.blend(img1, img2, alpha)

    return blended
