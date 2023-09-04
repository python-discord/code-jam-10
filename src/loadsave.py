from PIL import Image

from backend import TypingColors


def load(file_path, key):
    """Returns the backend object created from loading image in file path."""
    img = Image.open(file_path)
    object = TypingColors(img.convert("RGBA"), key)
    decoded_text = "".join([object.palette.rgbtocol[(r, g, b)] for r, g, b, a in img.getdata()])
    object.update(decoded_text.rstrip())  # transparent could be end of text
    return object


def save(object, file_path="Untitled.png"):
    """Saves backend object into given file."""
    object.canvas.save(file_path)


# testing
# obj = TypingColors(key='hello')
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
# obj = load("Untitled.png", 'hello')
# print(obj.text)
