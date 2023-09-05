from PIL import Image


def double_exposure(image1: Image.Image, image2: Image.Image, alpha: float = 0.50) -> Image:
    """
    Blend two images together to create a double exposure effect.

    :param image1: The first image.
    :param image2: The second image.
    :param alpha: The blending factor (0.0 for image1, 1.0 for image2, 0.5 for an equal blend).
    :return: The blended image.
    """
    image1.convert('RGB')
    image2.convert('RGB')
    w1, h1 = image1.size
    w2, h2 = image2.size
    if (w1 != w2) or (h1 != h2):
        image2 = image2.resize((w1, h1))

    new_image = Image.blend(image1, image2, alpha)

    return new_image
