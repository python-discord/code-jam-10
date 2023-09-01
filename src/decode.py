import sys

from PIL import Image

from main import decode

if __name__ == "__main__":
    decoded = decode(Image.open(sys.argv[1])).decode("utf-8")
    print(decoded)
