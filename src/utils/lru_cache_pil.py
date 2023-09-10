from collections import OrderedDict

from PIL.Image import Image


class LRUCachePIL:
    """LRU Cache implementation using OrderedDict"""

    def __init__(self, capacity: int) -> None:
        self.cache: OrderedDict[str, Image] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Image | None:
        """
        Get an item from the cache

        :param key:
        :return:
        """
        if key not in self.cache:
            return None
        else:
            # Move the accessed entry to the end
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: Image) -> None:
        """
        Put an item in the cache

        :param key:
        :param value:
        :return:
        """
        if key in self.cache:
            # If entry is found, remove it and re-insert at the end
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            # If the cache is at capacity, remove the first (oldest) item
            self.cache.popitem(last=False)
        self.cache[key] = value
