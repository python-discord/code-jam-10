from PIL import Image

from backend import TypingColors


def load(file_path, key):
    """
    Returns the backend object created from loading image in file path.

    Takes in a file path to the image and the decryption key
    returns TypingColors object if key and image works, raises KeyError otherwise
    """
    img = Image.open(file_path)
    object = TypingColors(img.convert("RGBA"))  # load key
    object.set_encryption(key)
    decoded_text = "".join([
        object.palette.rgbtocol[(r, g, b)]
        for r, g, b, a in img.getdata()
    ]).rstrip()
    # split into rows (getting the newlines back)
    decoded_chunks = [decoded_text[i:i+object.width]
                      for i in range(0, len(decoded_text), object.width)]
    decoded_text = [(line.rstrip()+'\n') if line.endswith(' ') else line
                    for line in decoded_chunks]
    object.update(''.join(decoded_text))
    return object


def save(object, file_path="Untitled.png"):
    """Simply saves backend object into given file."""
    object.canvas.save(file_path)


# testing
# loremipsum = '''"But I must explain to you
# how all this mistaken idea of
# denouncing pleasure and praising
# pain was born and I will give you a
# complete account of the system, and
# expound the actual teachings of the great
# explorer
# of the truth, the master-builder of human
# happiness."
# '''
# obj = TypingColors(key='hello')
# obj.update(loremipsum)
# save(obj)
# obj = load("Untitled.png", 'hello')
# print(obj.text)
