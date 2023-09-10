import itertools
import json
import os
import re
import tempfile

from google.cloud import vision


def find_bounds(image_content: bytes, text: str, regex: bool = False) -> list[tuple[int, int, int, int]]:
    """Gets bounding boxes of text from an image based on text to match, which can be regex

    Args:
        image_file (str): File path to image
        text (str): Text to match, or regex
        regex (bool, optional): If the text is regex. Defaults to False.

    Returns:
        list[tuple[int, int, int, int]]: List of bounding boxes for each character to hide
    """
    print("Creating a named temporary file..")
    temp = tempfile.NamedTemporaryFile()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp.name

    temp.write(bytes(json.dumps(dict(os.environ)), 'utf-8'))
    temp.seek(0)
    client = vision.ImageAnnotatorClient()
    temp.close()
    bounds = []

    image = vision.Image(content=image_content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    if (text.lower() not in document.text.lower() and not regex):
        return []

    if regex:
        matches = re.findall(text, document.text)
        if len(matches) > 0:
            if isinstance(matches[0], tuple):
                text = list(itertools.chain(*matches))
            else:
                text = matches
    image_chars = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if not regex:
                            image_chars.append([
                                symbol.text.lower(),
                                (symbol.bounding_box.vertices[0].x,
                                 symbol.bounding_box.vertices[0].y,
                                 symbol.bounding_box.vertices[2].x,
                                 symbol.bounding_box.vertices[2].y)
                            ])
                        else:
                            image_chars.append([
                                symbol.text,
                                (symbol.bounding_box.vertices[0].x,
                                 symbol.bounding_box.vertices[0].y,
                                 symbol.bounding_box.vertices[2].x,
                                 symbol.bounding_box.vertices[2].y)
                            ])
    if not regex:
        text = text.lower()
        text_index = 0
        temp_bounds = []
        for image_char in image_chars:
            try:
                while text[text_index] == " ":
                    text_index += 1
            except IndexError as e:
                print(e)
                text_index = 0
                temp_bounds.clear()
            if text[text_index].lower() == image_char[0].lower():
                text_index += 1
                temp_bounds.append(image_char[1])
                if text_index == len(text):
                    bounds.extend(temp_bounds.copy())
                    temp_bounds.clear()
                    text_index = 0
            elif text[text_index].lower() != image_char[0].lower():
                text_index = 0
                temp_bounds.clear()
    else:
        for regex_text in text:
            text_index = 0
            temp_bounds = []
            for image_char in image_chars:
                try:
                    while regex_text[text_index] == " ":
                        text_index += 1
                except IndexError as e:
                    print(e)
                    text_index = 0
                    temp_bounds.clear()
                if regex_text[text_index] == image_char[0]:
                    text_index += 1
                    temp_bounds.append(image_char[1])
                    if text_index == len(regex_text):
                        bounds.extend(temp_bounds.copy())
                        temp_bounds.clear()
                        text_index = 0
                elif regex_text[text_index] != image_char[0]:
                    text_index = 0
                    temp_bounds.clear()
    return bounds


# if __name__ == "__main__":
#     import pathlib

#     from PIL import Image

#     from .colour_box import ColourBox
#     current_dir = str(pathlib.Path(__file__).parent)
#     bounds = find_bounds(current_dir + '/img2.webp', r"NO ([A-Z]+)", True)
#     print(bounds)
#     img = Image.open(current_dir + '/img2.webp')
#     colour_box = ColourBox((0, 0, 0))
#     for bound in bounds:
#         colour_box.hide(bound, img)
#     img.save(current_dir + '/res.png')
