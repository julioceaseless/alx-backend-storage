#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache():
    """
    Cache class
    """
    def __init__(self):
        """
        Initialize the cache instance
        Connect to Redis server and flush the database
        """
        self._redis = redis.Redis()
        # clear Redis database
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]):
        """
        Store data in Redis using a randomly generated key
        """
        self.data = data
        key = str(uuid.uuid4())

        # store data
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes],
            Union[str, int, float, bytes]]] = None) -> (
                    Optional[Union[str, int, float, bytes]]):
        """
        Retrieve data from Redis using the given key and optional
        conversion function.
        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable[[bytes], Union[str, int, float, bytes]]]):
            Optional function to convert the data.
        Returns:
            Optional[Union[str, int, float, bytes]]: The converted data or None
            if the key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis and convert it to a string.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The data converted to a string or None if the key
            does not exist.
        """
        return self.get(key, lambda data: data.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The data converted to an integer or None if the key
            does not exist.
        """
        return self.get(key, int)


if __name__ == "__main__":
    """ Run only when called directly """
    cache = Cache()

    TEST_CASES = {
            b"foo": None,
            123: int,
            "bar": lambda d: d.decode("utf-8")
            }
    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
