from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import numpy as np


def generate_image(alphanumeric: str) -> Image.Image:
    """
    Generate an image of the character

    :param alphanumeric: alphanumeric character
    :return: Generated PIL image
    """
    image_size = (100, 100)
    image = Image.new("L", image_size, "white")

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("CarterOne-Regular.ttf", 120)

    # Draw the character in black on the image
    draw.text((0, -40), alphanumeric, fill="black", font=font, spacing=0)
    image.save(f"{alphanumeric}.png")
    return image


def generate_xor_pair(image: Image.Image, alphanumeric: str) -> Tuple[Image.Image, Image.Image]:
    """
    Split the original image into two separate images in such a way that when you XOR those two images together,
    you can reconstruct the original image

    :param image: greyscale image
    :param alphanumeric: character that is represented in the image
    :return: Tuple pair of generated two images that can rebulid original image when XORed
    """

    # Create two blank images with the same size
    image1 = Image.new("L", image.size)
    image2 = Image.new("L", image.size)

    # Convert images to numpy arrays for manipulation
    original_array = np.array(image)
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    
    # Split the original image randomly into two images
    for i in range(original_array.shape[0]):
        for j in range(original_array.shape[1]):
            """
            A | B | A XOR B
            ----------------
            0 | 0 | 0
            1 | 0 | 1 
            0 | 1 | 1
            1 | 1 | 0
            """
            if original_array[i][j] == 255:
                # If the pixel is white
                if np.random.randint(2) == 0:
                    image1_array[i][j] = 255
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 0
                    image2_array[i][j] = 0
            else:
                if np.random.randint(2) == 0:
                    image1_array[i][j] = original_array[i][j]
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 255
                    image2_array[i][j] = original_array[i][j]

    # Convert numpy arrays back to images
    image1 = Image.fromarray(image1_array)
    image2 = Image.fromarray(image2_array)
    
    # Save the two new images
    image1.save(f"{alphanumeric}_1.png")
    image2.save(f"{alphanumeric}_2.png")
    return image1, image2


if __name__ == "__main__":
    for c in "PYTHON":
        c_img = generate_image(c)
        generate_xor_pair(c_img, c)
