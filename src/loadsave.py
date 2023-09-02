from PIL import Image
from PIL.PngImagePlugin import PngInfo

from backend import PaintingColors


def load(file_path):
    """Returns the backend object created from loading image in file path."""
    img = Image.open(file_path)
    metadata = img.text
    object = PaintingColors(img.convert("RGBA"))
    decoded_text = ""
    for char, (r, g, b) in metadata.items():  # importing pallete from metadata
        object.pallete[char] = (ord(r), ord(g), ord(b), 255)

    rev_pallete = {v: k for k, v in object.pallete.items()}  # map col to char
    rev_pallete[(0, 0, 0, 0)] = " "  # transparent spaces

    for pixel in img.getdata():  # decode the text pixel by pixel
        decoded_text += rev_pallete[pixel]

    object.update(decoded_text.rstrip())  # transparent could be end of text
    return object


def save(object, file_path="Untitled.png"):
    """Saves backend object into given file."""
    metadata = PngInfo()  # store pallete information in metadata
    for char, (r, g, b, a) in object.pallete.items():
        metadata.add_text(char, f"{chr(r)}{chr(g)}{chr(b)}")  # 3 bytes per key
    object.canvas.save(file_path, pnginfo=metadata)


# testing
# obj = PaintingColors()
# loremipsum = '''"But I must explain to you how all this mistaken idea of
# denouncing pleasure and praising pain was born and I will give you a complete
# account of the system, and expound the actual teachings of the great explorer
# of the truth, the master-builder of human happiness. No one rejects, dislikes,
# or avoids pleasure itself, because it is pleasure, but because those who do not
# know how to pursue pleasure rationally encounter consequences that are extremely
# painful. Nor again is there anyone who loves or pursues or desires to obtain
# pain of itself, because it is pain, but because occasionally circumstances occur
# in which toil and pain can procure him some great pleasure. To take a trivial
# example, which of us ever undertakes laborious physical exercise, except to
# obtain some advantage from it? But who has any right to find fault with a man
# who chooses to enjoy a pleasure that has no annoying consequences, or one who
# avoids a pain that produces no resultant pleasure?"
# '''.replace("\n"," ")
# obj.update(loremipsum)
# save(obj)
# obj = load("Untitled.png")
# print(obj.text)
