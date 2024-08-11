#!/usr/bin/env python3
"""
Implement an expiring cache web tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()


def url_counter(method: Callable) -> Callable:
    """decorator to count the number of times a url was called"""
    @wraps(method)
    def wrapper(*args):
        # keep count
        count_key = f"count:{args[0]}"  # Use the first argument for url
        print(count_key)
        r.incr(count_key)
        # print(f"accessed {r.get(count_key)} times")

        # retrieve cached results
        cache_key = args[0]
        cached_data = r.get(cache_key)
        if cached_data:
            # convert data to string
            # print("found in cache!")
            return cached_data.decode('utf-8')

        # cache results
        result = method(*args)
        r.set(cache_key, result, 10)  # Set expiry time
        # print("caching...")
        return result
    return wrapper


@url_counter
def get_page(url: str) -> str:
    """get page"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page("http://google.com")
    print(int(r.get('count:http://google.com')))
