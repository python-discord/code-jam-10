import sys

from main import encode

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as file:
        encoded = encode(file.read())
        encoded.save(sys.argv[1] + ".png")
