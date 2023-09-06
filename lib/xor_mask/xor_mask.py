from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import numpy as np
from pathlib import Path


def generate_image(alphanumeric: str, difficulty: int) -> Image.Image:
    """
    Generate an image of the character

    :param alphanumeric: alphanumeric character
    :param difficulty: difficulty level ranging from 1-3
    :return: Generated PIL image
    """

    difficulty_properties = {
        1: {"image_size": (12, 12), "font_size": 14, "offset": (3, -2)},
        2: {"image_size": (50, 50), "font_size": 64, "offset": (8, -10)},
        3: {"image_size": (100, 100), "font_size": 130, "offset": (20, -20)},
    }

    # Get the image properties based on the difficulty level, default to level 3
    properties = difficulty_properties.get(difficulty, difficulty_properties[3])

    image_size = properties["image_size"]
    font_size = properties["font_size"]
    offset = properties["offset"]

    image = Image.new("L", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("BebasNeue-Regular.ttf", font_size)
    # Draw the character in black on the image
    draw.text(offset, alphanumeric, fill="black", font=font, spacing=0)
    binary_image = image.point(lambda p: 255 if p > 128 else 0)
    binary_image.save(Path(f"images/xor_mask/{alphanumeric}.png"))
    return binary_image


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
            if original_array[i][j] >= 128:
                # If the pixel is white
                if np.random.randint(2) == 0:
                    image1_array[i][j] = 255
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 0
                    image2_array[i][j] = 0
            else:
                if np.random.randint(2) == 0:
                    image1_array[i][j] = 0
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 255
                    image2_array[i][j] = 0

    # Convert numpy arrays back to images
    image1 = Image.fromarray(image1_array)
    image2 = Image.fromarray(image2_array)
    
    # Save the two new images
    image1.save(Path(f"images/xor_mask/{alphanumeric}_1.png"))
    image2.save(f"images/xor_mask/{alphanumeric}_2.png")
    return image1, image2
