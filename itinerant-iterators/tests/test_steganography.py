# flake8: noqa
import tempfile
from pathlib import Path

from app.steganography import Lsb, decode, encode


def test_lsb_encode_decode():
    message = "secret message"
    lsb = Lsb()
    f = tempfile.NamedTemporaryFile("w", delete=True, suffix=".png")
    encode(message, Path("tests/data/python-logo.jpg"), Path(f.name), lsb)
    got = decode(Path(f.name), lsb)
    f.close()
    assert message == got
