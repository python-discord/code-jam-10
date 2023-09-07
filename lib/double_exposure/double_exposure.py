from PIL import Image


def double_exposure(img1: Image, img2: Image, alpha: float = 0.5) -> Image:
    """
    Blend two images together using alpha blending

    :param img1: PIL Image
    :param img2: PIL Image
    :param alpha: int
    :return:
    """
    # Check that both images are 450x450 and if not, resize them
    if img1.size != (450, 450):
        img1 = img1.resize((450, 450))

    if img2.size != (450, 450):
        img2 = img2.resize((450, 450))

    # Convert both images to RGB
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Blend the images
    blended = Image.blend(img1, img2, alpha)

    return blended
