from math import ceil, sqrt

from PIL import Image


def encode(source: bytes) -> Image.Image:
    size = ceil(sqrt(ceil(len(source) / 3)))
    image = Image.new("RGB", (size, size))
    x = 0
    y = 0
    iterator = iter(source)

    for byte in iterator:
        image.putpixel((x, y), (byte, next(iterator, 0), next(iterator, 0)))
        x += 1
        if x >= size:
            x = 0
            y += 1

    return image


def decode(source: Image.Image) -> bytes:
    size = source.size[0]
    output = bytearray()

    for y in range(size):
        for x in range(size):
            pixel = source.getpixel((x, y))
            output.extend(pixel)

    return bytes(output)


if __name__ == "__main__":
    with open(__file__, "rb") as f:
        encoded = encode(f.read())
        encoded.save(__file__ + ".png")
