#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union


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
