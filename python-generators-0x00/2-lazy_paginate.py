#!/usr/bin/env python3
"""
2-lazy_paginate.py - Lazy loading paginated data using generators
"""

import mysql.connector
from mysql.connector import Error
import seed


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Number of records to skip
        
    Returns:
        list: List of user records for the current page
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated data from the users database.
    Only fetches the next page when needed.
    
    Args:
        page_size (int): Number of records per page
        
    Yields:
        list: A page of user records
    """
    offset = 0
    
    while True:
        # Fetch the current page
        page = paginate_users(page_size, offset)
        
        # If page is empty, we've reached the end
        if not page:
            break
            
        # Yield the current page
        yield page
        
        # Move to the next page
        offset += page_size


# Alternative implementation name to match the expected import
def lazy_paginate(page_size):
    """
    Alternative name for lazy_pagination to match expected function name.
    """
    return lazy_pagination(page_size)


if __name__ == "__main__":
    # Test lazy pagination
    print("Testing lazy pagination with page size 5:")
    page_count = 0
    
    for page in lazy_pagination(5):
        page_count += 1
        print(f"\n--- Page {page_count} ---")
        for user in page:
            print(user)
        
        # Only show first 2 pages for testing
        if page_count >= 2:
            break
