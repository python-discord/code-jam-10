from PIL import Image

from backend import TypingColors


def load(file_path, key):
    """
    Returns the backend object created from loading image in file path.

    Takes in a file path to the image and the decryption key
    returns TypingColors object if key and image works, raises KeyError otherwise
    """
    img = Image.open(file_path)
    w, h = img.size
    object = TypingColors(img.convert("RGBA"))
    object.set_encryption(key)  # load the key
    decoded_text = "".join([
        object.palette[(r, g, b, a)]
        for r, g, b, a in img.getdata()
    ]).rstrip()  # get the text
    # split into rows and turning spaces to newlines
    decoded_chunks = [decoded_text[i:i+w]
                      for i in range(0, len(decoded_text), w)]
    decoded_text = ''.join([(line.rstrip()+'\n') if line.endswith(' ') else line
                            for line in decoded_chunks])
    object.update(decoded_text)
    return object, decoded_text  # return the text for the gui


def save(object, file_path="Untitled.png"):
    """Simply saves backend object into given file."""
    object.canvas.save(file_path, "PNG")
