import unittest
from PIL import Image
from .double_exposure import double_exposure


class DoubleExposureTestCase(unittest.TestCase):
    """Tests For double_exposure.py"""
    def test_size(self):
        # Load two example images
        image1 = Image.new("RGB", (200, 200))
        image2 = Image.new("RGB", (200, 200))

        # Call the double_exposure function
        result_image = double_exposure(image1, image2)

        # Check if the size of the result image matches the input images
        self.assertEqual(result_image.size, (200, 200))

    def test_alpha_zero(self):
        # Create two images with different colors
        image1 = Image.new("RGB", (200, 200), (255, 0, 0))  # Red
        image2 = Image.new("RGB", (200, 200), (0, 255, 0))  # Green

        # Blend the images with alpha = 0.0 (result should be the first image)
        result_image = double_exposure(image1, image2, alpha=0.0)

        # Check if the result image matches the first image
        self.assertEqual(result_image, image1)

    def test_alpha_one(self):
        # Create two images with different colors
        image1 = Image.new("RGB", (200, 200), (255, 0, 0))  # Red
        image2 = Image.new("RGB", (200, 200), (0, 255, 0))  # Green

        # Blend the images with alpha = 1.0 (result should be the second image)
        result_image = double_exposure(image1, image2, alpha=1.0)

        # Check if the result image matches the second image
        self.assertEqual(result_image, image2)


