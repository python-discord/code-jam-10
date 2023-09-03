import unittest
from pathlib import Path

from PIL import Image

from .hidden_in_ascii import img_to_ascii, seed_secret, ascii_to_img


class TestHiddenInAscii(unittest.TestCase):
    """Test cases for hidden_in_ascii.py"""

