import random

import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFont


def reverse_ishihara(image: Image.Image, message: str = None,
                     color_blind_color: tuple = (155, 155, 0), noise_color: tuple = (150, 151, 0),
                     noise_density: float = 0.006, dot_radius: int = 6) -> Image.Image:
    """
    Generate a reverse Ishihara image from an input image.

    :param image: PIL Image object
    :param message: Optional message or number to display using dots
    :param color_blind_color: Color for the message, distinguishable by color-blind individuals
    :param noise_color: Color for noise, not distinguishable by non-color blind individuals from the message color
    :param noise_density: Density of the noise in the image (0 to 1)
    :param dot_radius: Radius of the noise dots
    :return: PIL Image object
    """
    draw = ImageDraw.Draw(image)

    # Draw the message using dots if provided
    if message:
        font_path = "MontserratRegular-BWBEl.ttf"  # Point to a TTF or OTF font file on your machine
        font = ImageFont.truetype(font_path, int(image.height * 0.5))

        left, top, right, bottom = font.getbbox(message)
        text_width, text_height = right - left, bottom - top

        text_img = Image.new('1', (text_width, text_height), color='white')
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((-left, -top), message, fill='black', font=font)  # Notice the negative offsets

        dot_density_for_text = 0.001  # This determines the density of the dots. Adjust as needed (0 to 1).

        center_x_offset = (image.width - text_width) // 2
        center_y_offset = (image.height - text_height) // 2

        # For each black pixel in the text image, draw a dot on the main image
        for y in range(text_height):
            for x in range(text_width):
                if text_img.getpixel((x, y)) == 0 and random.random() < dot_density_for_text:
                    # Adjust these lines to position the text at the center
                    center_x = x + center_x_offset
                    center_y = y + center_y_offset
                    draw.ellipse([(center_x - dot_radius, center_y - dot_radius),
                                  (center_x + dot_radius, center_y + dot_radius)], fill=color_blind_color)

    # Add noise
    num_noise_dots = int(noise_density * image.width * image.height)
    for _ in range(num_noise_dots):
        x = random.randint(0 + dot_radius, image.width - 1 - dot_radius)
        y = random.randint(0 + dot_radius, image.height - 1 - dot_radius)
        draw.ellipse([(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)], fill=noise_color)

    return image


def unmask_reverse_ishihara(image: Image.Image, a_scale: int = 2, b_scale: int = 2) -> Image.Image:
    """
    Reverse a reverse Ishihara image to reveal the hidden message.

    :param image: PIL Image object
    :param a_scale:
    :param b_scale:
    :return: PIL Image object
    """
    # Convert image to Lab color space
    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile = ImageCms.createProfile("LAB")

    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
    lab_image = ImageCms.applyTransform(image, rgb2lab_transform)

    # Convert Lab image to numpy array for easier manipulation
    lab_array = np.array(lab_image)

    # Increase contrast in a and b channels
    l_channel, a_channel, b_channel = lab_array[:, :, 0], lab_array[:, :, 1], lab_array[:, :, 2]

    # Center around zero and scale
    a_channel = (a_channel - 128) * a_scale + 128
    b_channel = (b_channel - 128) * b_scale + 128

    # Ensure values remain in the 0-255 range
    a_channel = np.clip(a_channel, 0, 255)
    b_channel = np.clip(b_channel, 0, 255)

    # Reconstruct the Lab image
    enhanced_lab_array = np.stack([l_channel, a_channel, b_channel], axis=2).astype(np.uint8)
    enhanced_lab_image = Image.fromarray(enhanced_lab_array)

    # Convert back to RGB
    lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
    enhanced_rgb_image = ImageCms.applyTransform(enhanced_lab_image, lab2rgb_transform)

    return enhanced_rgb_image
