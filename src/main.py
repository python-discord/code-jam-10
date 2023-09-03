from math import ceil, sqrt

from PIL import Image


def bytes_to_colors(sequence: bytes):
    iterator = iter(sequence)
    for byte in iterator:
        yield (byte << 0) + (next(iterator, 0) << 8) + (next(iterator, 0) << 16)


def encode(source: bytes) -> Image.Image:
    size = ceil(sqrt(ceil(len(source) / 3)))
    image = Image.new("RGB", (size, size))
    # putdata expects a sequence of integers, so we convert the colors to integers.
    colors = list(bytes_to_colors(source))
    image.putdata(colors)
    return image


def decode(image: Image.Image) -> bytes:
    # getdata returns tuples of (r, g, b) values in RGB mode.
    colors = image.getdata()
    source = [value for color in colors for value in color]
    return bytes(source)


if __name__ == "__main__":
    with open(__file__, "rb") as f:
        encoded = encode(f.read())
        encoded.save(__file__ + ".png")
