import requests


def find_bounds(image_file: str, text: str, regex: bool = False) -> list[tuple[int, int, int, int]]:
    """Gets bounding boxes of text from an image based on text to match, which can be regex.

    Args:
        image_file (str): File path to image
        text (str): Text to match, or regex
        regex (bool, optional): If the text is regex. Defaults to False.

    Returns:
        list[tuple[int, int, int, int]]: List of bounding boxes for each character to hide
    """
    data = {
        "text": text,
        "regex": regex
    }
    files = {
        'file': open(image_file, 'rb')
    }
    bounds = requests.post("https://itinerantiterators.hipeople21.repl.co", data=data, files=files)
    return bounds.json()


if __name__ == "__main__":
    import pathlib

    from PIL import Image

    from .colour_box import ColourBox
    current_dir = str(pathlib.Path(__file__).parent)
    bounds = find_bounds(current_dir + '/img2.webp', r"NO ([A-Z]+)", True)
    print(bounds)
    img = Image.open(current_dir + '/img2.webp')
    colour_box = ColourBox((0, 0, 0))
    for bound in bounds:
        colour_box.hide(bound, img)
    img.save(current_dir + '/res.png')
