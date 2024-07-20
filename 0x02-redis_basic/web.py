#!/usr/bin/python3
"""
Implement an expiring cache web tracker
"""

import requests
import redis
from functools import wraps
from typing import Callable

r = redis.Redis()


def cache_result(expiration: int):
    """
    Decorator to cache the result of a function call for a specified time.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the result is already cached
            cached_result = r.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            # Call the original function and cache the result
            result = func(url)
            r.setex(url, expiration, result)
            return result
        return wrapper
    return decorator


def count_access(func: Callable) -> Callable:
    """
    Decorator to count how many times a URL is accessed.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count
        count_key = f"count:{url}"
        r.incr(count_key)

        # Call the original function
        return func(url)
    return wrapper


@cache_result(expiration=10)
@count_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    
    Args:
        url (str): The URL to fetch.
        
    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/https://example.com"
    print(get_page(test_url))  # Fetches the content and caches it
    print(get_page(test_url))  # Retrieves the content from the cache
    print(r.get(f"count:{test_url}").decode('utf-8'))  # Outputs the access count

