from pathlib import Path

import numpy as np
from PIL import Image


class ExistingImage:
    """
    Encodes(Decodes) text into(from) an existing image without noticeably altering the image.

        Requires a (symmetric) key to encode/decode the text.
    """

    def __init__(
        self, input_image: str | bytes | Path | Image.Image, key: str, text: str = None
    ) -> None:
        self.text = text
        self.input_image = (
            np.asarray(input_image)
            if isinstance(input_image, Image.Image)
            else np.asarray(Image.open(input_image))
        )
        self.key = f"==={key}==="

    def __bin__(self, secret: str):
        return "".join([format(ord(i), "08b") for i in secret])

    @staticmethod
    def __encode(
        image: np.ndarray, binary_secret_data: str, n_bits: int = 1
    ) -> np.ndarray:
        data_index = 0
        data_len = len(binary_secret_data)
        bin_parts = [
            binary_secret_data[i : i + n_bits]
            for i in range(0, len(binary_secret_data), n_bits)
        ]

        for row in image[:-1]:
            for pxl in row:
                for i, clr in enumerate(pxl):
                    if data_index >= data_len:
                        break

                    pxl[i] = clr >> n_bits << n_bits | int(bin_parts[data_index], 2)
                    data_index += 1

        image[-1][-1][-1] = image[-1][-1][-1] >> 3 << 3 | n_bits
        image[-1][-1][-2] = image[-1][-1][-2] >> 3 << 3 | 1
        return image

    def encode(self):
        """Encode the given secret into the img"""
        # print("[*] Encoding data...")
        secret_data = self.text + self.key

        for i in range(1, 5):
            if (len(secret_data) + 1) <= (
                (self.input_image.shape[0] - 1) * self.input_image.shape[1] * 3 * i // 8
            ):
                break
        else:
            print("Image too small for given secret")
            return

        return self.__encode(self.input_image.copy(), self.__bin__(secret_data), i)

    @staticmethod
    def __decode(image: np.ndarray, key: str, n_bits: int = 1) -> str:
        len_key = len(key)

        def __get_binary_from_img(image, key, n_bits):
            binary_data = ""
            for row in image:
                for pxl in row:
                    for clr in pxl:
                        binary_data += f"{(clr & n_bits):b}"
                        # if key in binary_data:
                        if key == binary_data[-len_key:]:
                            binary_data = binary_data.replace(key, "")
                            return binary_data
            print("invalid image")

        binary_data = __get_binary_from_img(image, key, n_bits)

        bytes_data = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]

        decoded_data = ""
        for byte in bytes_data:
            decoded_data += chr(int(byte, 2))

        return decoded_data

    def decode(self):
        """Decode the given img to reveeal the secret text"""
        # print("[+] Decoding image...")

        n_bits = self.input_image[-1][-1][-1] & 7

        if (1 > n_bits) or (n_bits > 4):
            print("invalid image")
            return

        return self.__decode(
            self.input_image, self.__bin__(self.key), int("1" * n_bits)
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", help="The text data to encode into the image")
    parser.add_argument("-e", "--encode", help="Encode the following image")
    parser.add_argument("-d", "--decode", help="decode the following image")
    parser.add_argument(
        "-k", "--key", help="The encryption key to be used for encoding/decoding"
    )

    args = parser.parse_args()

    if args.encode:
        input_image = Path(args.encode)
        file = input_image.parts[-1]
        filename, ext = file.split(".")
        output_image = Path(*input_image.parts[:-1], f"{filename}_encoded.{ext}")

        encoder = ExistingImage(input_image, args.key, args.text)

        encoded_image = encoder.encode()
        Image.fromarray(encoded_image).save(output_image)
        print("[+] Saved encoded image.")
    if args.decode:
        input_image = Path(args.decode)

        decoder = ExistingImage(input_image, args.key)

        decoded_data = decoder.decode()
        print("[+] Decoded data:", decoded_data)

"""
Usage example:

>> python existing_img_backend.py -h
usage: existing_img_backend.py [-h] [-t TEXT] [-e ENCODE] [-d DECODE] [-k KEY]

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  The text data to encode into the image
  -e ENCODE, --encode ENCODE
                        Encode the following image
  -d DECODE, --decode DECODE
                        decode the following image
  -k KEY, --key KEY     The encryption key to be used for encoding/decoding

>> python existing_img_backend.py -t "encryption test 1" -e "./great_wave_unscrambled.png" -k "test key 1"
[+] Saved encoded image.

>> python existing_img_backend.py -d "./great_wave_unscrambled_encoded.png" -k "test key 1"
[+] Decoded data: encryption test 1
"""
