import argparse
import random
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw


def prepare_input(img_path: str) -> Tuple[Image.Image, List[int]]:
    """
    Prepare the input image by center cropping into a square

    :param img_path: input image file path
    :return: Tuple of cropped input Image and the coordinates of the cropped area
    """
    img = Image.open(img_path)

    # Calculate the square size
    width, height = img.size
    size = min(width, height)

    # Calculate the coordinates for cropping
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    # Crop the image to a square
    return img.crop((left, top, right, bottom)), [left, top, right, bottom]


def avg_greyscale(img: Image.Image) -> float:
    """
    Calculates average greyscale or luminance value of an input image

    :param img: input image
    :return: average luminance
    """
    np_img = np.array(img)
    w, h = np_img.shape
    return np.average(np_img.reshape(w * h))


def img_to_ascii(img: Image.Image, cols: int, scale: float, dens: int) -> List[str]:
    """
    Given Image and dims (rows, cols) returns an m*n list of Images

    :param img: input image file
    :param cols: number of columns
    :param scale: aspect ratio scale
    :param dens: greyscale density level
    :return: ascii text generated from input image
    """
    # The amount of text to white space in each of these character determines the greyscale value
    greyscale_strs = [
        "@%#*+=-:. ",  # 10 characters,
        "@%W*hdwOLUzurt|1i}?+>,' ",  # 24 characters,
        "@B$%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1lIi!{}[]?-_+~<>;:,^`'. ",  # 70 characters,
    ]

    # Convert to grayscale (L stands for luminance)
    gs_img = img.convert("L")
    gs_img_w, gs_img_h = gs_img.size[0], gs_img.size[1]

    w = gs_img_w / cols  # tile width
    h = w / scale  # tile height
    rows = int(gs_img_h / h)  # Number of rows of text

    # Input image size validation
    # TODO put this near the arg parser
    if gs_img_w < cols or gs_img_h < rows:
        raise ValueError("Image not big enough for specified number of columns.")

    # Generate ascii art
    ascii_ = []
    for r in range(rows):
        y1 = int(r * h)
        y2 = gs_img_h if r == rows - 1 else int((r + 1) * h)
        ascii_.append("")

        for c in range(cols):
            x1 = int(c * w)
            x2 = gs_img_w if c == cols - 1 else int((c + 1) * w)

            # Find average luminance of the cropped tile
            avg = int(avg_greyscale(gs_img.crop((x1, y1, x2, y2))))

            # Find corresponding ascii character by greyscale value and append to the row
            i = int((avg * (len(greyscale_strs[dens]) - 1)) / 255)
            ascii_[r] += greyscale_strs[dens][i]

    return ascii_


def ascii_to_img(ascii_text_file_path: str, output_dest_path: str, coordinates: List[int]) -> Image.Image:
    """
    Creates image file from ascii text file

    :param ascii_text_file_path: ascii text file path
    :param output_dest_path: output destination file path
    :param coordinates: coordinates used to crop the original image
    :return: Generated image from converting ascii text into PNG
    """
    with open(ascii_text_file_path, "r") as file:
        ascii_text = file.read()

    img_w, img_h = (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1])
    img = Image.new("L", (img_w, img_h), "white")

    # Draw text to image
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox(xy=(0, 0), text=ascii_text)
    left, top, right, bottom = bbox
    w = right - left
    h = bottom - top
    draw.text((0, 0), ascii_text, fill="black")
    img = img.crop((0, 0, w, h))  # Crop out white spaces
    img.save(output_dest_path, "png")
    return img


def seed_secret(ascii_file_path: str, secret: str, binary_mode: bool) -> None:
    """
    Insert the secret phrase randomly somewhere in the ascii file

    :param ascii_file_path: ascii text file path
    :param secret: secret phrase to hide
    :param binary_mode: whether to hide the text in binary representation
    :return: None
    """
    with open(ascii_file_path, "r") as file:
        lines = file.readlines()

    random_line = random.randint(0, len(lines) - 1)

    # Convert to binary representation if chosen 'insane mode'
    if binary_mode:
        secret = "".join(map(bin, bytearray(secret, "utf8")))

    line_length = len(lines[random_line])
    secret_length = len(secret)

    # Raise error if the secret is longer than 10th of the entire ascii art
    if secret_length > (line_length * len(lines) // 10):
        raise ValueError("The secret phrase is too long to be hidden in this ascii art.")

    # Replace the ascii art with secret message on randomly selected place
    # TODO if secret is longer than the line length, overflow to the next line.
    # If there is no next line, shift the random line by -1 to make room
    position = random.randint(0, line_length - secret_length - 1)
    lines[random_line] = (
        "".join([lines[random_line][0:position], secret, lines[random_line][position + secret_length:]])
    )

    with open(ascii_file_path, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts input image into ascii art and saves the resulting text back into image (.png)"
    )
    parser.add_argument("--input", dest="input", required=True, help="Input image")
    parser.add_argument(
        "--secret",
        dest="secret",
        required=True,
        help="Secret phrase to hide in the ascii art",
    )
    parser.add_argument(
        "--ascii-file",
        dest="ascii_file",
        required=False,
        default="ascii.txt",
        help="Output location for generated ascii text file",
    )
    parser.add_argument(
        "--output",
        dest="output",
        required=False,
        default="result.png",
        help="Output location for generated image file",
    )
    parser.add_argument(
        "--density",
        dest="dens",
        required=False,
        default=2,
        help="Resolution of greyscale (0: Low, 1: Medium, 2: High (Default))",
    )
    parser.add_argument(
        "--insane-mode",
        dest="insane_mode",
        required=False,
        action="store_true",
        help="Hides secret phrase in binary string!!!",
    )
    args = parser.parse_args()
    input_img, coordinates = prepare_input(args.input)
    scale = 0.39  # Aspect ratio of monospace characters
    cols = int((coordinates[2] - coordinates[0]) // 10)  # 1/10 th of the square cropped image

    with open(args.ascii_file, "w") as f:
        for row in img_to_ascii(input_img, cols, scale, int(args.dens)):
            f.write(row + "\n")
    seed_secret(args.ascii_file, args.secret, args.insane_mode)
    output_img = ascii_to_img(args.ascii_file, args.output, coordinates)
    output_img.resize(input_img.size)
    output_img.save(args.output)
