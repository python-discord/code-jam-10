import itertools
import re

from google.cloud import vision


def find_bounds(image_file:str, text:str, regex:bool=False):
    
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

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
                        image_chars.append([symbol.text.lower(), (symbol.bounding_box.vertices[0].x, symbol.bounding_box.vertices[0].y, symbol.bounding_box.vertices[2].x, symbol.bounding_box.vertices[2].y)])

    if not regex:
        text_index = 0
        temp_bounds = []
        for image_char in image_chars:
            try:
                while text[text_index] == " ":
                    text_index += 1
            except IndexError as e:
                print(e)
                # equal = False
                text_index = 0
                temp_bounds.clear()
            if text[text_index].lower() == image_char[0]:
                # equal = True
                
                text_index += 1
                temp_bounds.append(image_char[1])
                if text_index == len(text):
                    bounds.extend(temp_bounds.copy())
                    temp_bounds.clear()
                    text_index = 0
            elif text[text_index].lower() != image_char[0]:
                text_index = 0
                temp_bounds.clear()
                
    
    return bounds




if __name__ == "__main__":
    import pathlib
    from .colour_box import ColourBox
    from PIL import Image
    current_dir = str(pathlib.Path(__file__).parent)
    bounds = find_bounds(current_dir + '/img2.webp', "Oscar Wilde")
    print(bounds)
    img = Image.open(current_dir + '/img2.webp')
    colour_box = ColourBox((0, 0, 0))
    for bound in bounds:
        colour_box.hide(bound, img)
    img.save(current_dir + '/res.png')