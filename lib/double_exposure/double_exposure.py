from PIL import Image

from PIL import Image


def create_double_exposure(image1: Image.Image, image2: Image.Image, blend_factor: float = 0.5) -> Image.Image:
    """
    Create a double exposure effect by blending two images together.

    The resulting image will have the dimensions of the first image, and the second image
    will be resized if necessary to match those dimensions before blending.

    :param image1: First input image.
    :param image2: Second input image.
    :param blend_factor: Blend factor determining the weight of each image.
                         Values range from 0.0 (only image1) to 1.0 (only image2).
                         A value of 0.5 will give equal weight to both images.
    :return: A new Image object representing the double exposure effect.
    """

    if not (0.0 <= blend_factor <= 1.0):
        raise ValueError("Blend factor must be between 0.0 and 1.0, inclusive.")

    # Ensure both images are in RGB mode for consistent blending
    image1_rgb = image1.convert('RGB')
    image2_rgb = image2.convert('RGB')

    # Resize the second image to match the dimensions of the first if needed
    if image1_rgb.size != image2_rgb.size:
        image2_rgb = image2_rgb.resize(image1_rgb.size)

    # Blend the two images using the specified blend factor
    blended_image = Image.blend(image1_rgb, image2_rgb, blend_factor)

    return blended_image

