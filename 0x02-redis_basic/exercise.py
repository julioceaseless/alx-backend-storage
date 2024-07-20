#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for
    a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # store input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the orginal method and store the output
        result = method(self, *args, **kwargs)

        # store the output
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    decorator to count the number of times a method of
    Cache class is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


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

    @call_history
    @count_calls
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


def replay(method: Callable):
    """
    Display the history of calls for a given method.

    Args:
        method (Callable): The method to replay.
    """

    # Get the instance self from the method
    cache_instance = method.__self__

    # get qualified name
    method_name = method.__qualname__

    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = cache_instance._redis.lrange(input_key, 0, -1)
    outputs = cache_instance._redis.lrange(output_key, 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(method_name,
                                     input_data.decode('utf-8'),
                                     output_data.decode('utf-8')))


if __name__ == "__main__":
    """ Run only when called directly """
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
