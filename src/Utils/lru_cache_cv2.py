from collections import OrderedDict

import numpy as np


class LRUCacheCV2:
    """LRU Cache implementation using OrderedDict for OpenCV images (numpy arrays)."""

    def __init__(self, capacity: int) -> None:
        self.cache: OrderedDict[str, np.ndarray] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> np.ndarray | None:
        """
        Get an item from the cache.

        :param key: The key associated with the cached image.
        :return: The cached image (numpy array) if it exists, None otherwise.
        """
        if key not in self.cache:
            return None
        else:
            # Move the accessed entry to the end
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: np.ndarray) -> None:
        """
        Put an item in the cache.

        :param key: The key to associate with the image.
        :param value: The image (numpy array) to cache.
        :return: None
        """
        if key in self.cache:
            # If entry is found, remove it and re-insert at the end
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            # If the cache is at capacity, remove the first (oldest) item
            self.cache.popitem(last=False)
        self.cache[key] = value
