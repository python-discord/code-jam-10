import random

import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans


def pixelate_and_group_colors_sampled(image: Image.Image, group_number: int, sample_fraction: float = 0.1) -> Image:
    """
    Pixelate and group colors of an image using MiniBatchKMeans clustering

    :param image: PIL Image
    :param group_number: number of groups to cluster colors into
    :param sample_fraction: fraction of pixels to sample for clustering
    :return: PIL Image with pixelated and grouped colors
    """
    # Resize to reduce colors
    orig_size = image.size

    # Resize to reduce colors
    small = image.resize((32, 32), resample=Image.BILINEAR)
    result = small.resize(orig_size, Image.NEAREST)

    # Convert to numpy array for clustering
    data = np.array(result)
    pixels = data.reshape((-1, 3))

    # Sample a fraction of the pixels
    num_samples = int(len(pixels) * sample_fraction)
    sampled_pixels = random.sample(list(pixels), num_samples)

    # Apply MiniBatchKMeans clustering on sampled pixels
    kmeans = MiniBatchKMeans(n_clusters=group_number, n_init=3).fit(sampled_pixels)
    cluster_centers = kmeans.cluster_centers_

    # Assign all pixels to nearest cluster centers
    labels = kmeans.predict(pixels)
    new_pixels = np.array([list(cluster_centers[label]) for label in labels], dtype=np.uint8)

    # Reshape to original image shape
    new_image_data = new_pixels.reshape(data.shape)

    # Convert back to Image and return
    new_image = Image.fromarray(new_image_data)
    return new_image


def swap_colors(img: Image.Image, color1: tuple, color2: tuple) -> Image.Image:
    """
    Swap two colors in an image.

    :param img: PIL Image
    :param color1: tuple representing the first color
    :param color2: tuple representing the second color
    :return: PIL Image with swapped colors
    """
    img_array = np.array(img)

    mask1 = (img_array == color1).all(-1)
    mask2 = (img_array == color2).all(-1)

    img_array[mask1] = color2
    img_array[mask2] = color1

    return Image.fromarray(img_array)
