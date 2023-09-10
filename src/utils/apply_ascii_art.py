from pathlib import Path

from PyQt6.QtGui import QPixmap

from lib.hidden_in_ascii.hidden_in_ascii import (
    ascii_to_img, generate_ascii_file, prepare_input, seed_secret
)


def apply_ascii_art(args: dict) -> QPixmap:
    """
    Apply ASCII art to the given image

    :param args: a dictionary of arguments
    :return: QPixmap of the image
    """
    try:
        image_dir_path = Path(Path(__file__).parent.parent, "images")
        input_img, coordinates = prepare_input(Path(str(args.get("image_to_edit"))))
        output_img_path = Path(image_dir_path, "ascii_output.png")
        ascii_file_path = Path(image_dir_path, "ascii.txt")
        generate_ascii_file(input_img, ascii_file_path, 2)
        seed_secret(ascii_file_path, str(args.get("secret")), False)
        ascii_to_img(ascii_file_path, coordinates, input_img.size, output_img_path)
        pixmap = QPixmap(str(output_img_path))
        return pixmap
    except Exception as e:
        print(e)
        return QPixmap()
