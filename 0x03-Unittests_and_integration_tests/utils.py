#!/usr/bin/env python3
"""Utility functions for GitHub client."""

import requests
from typing import Dict, Any


def access_nested_map(nested_map: Dict[Any, Any], path: tuple) -> Any:
    """Access nested map with path tuple."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict[Any, Any]:
    """Get JSON data from URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Decorator to memoize function results."""
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper
