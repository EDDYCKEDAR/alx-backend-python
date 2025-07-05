#!/usr/bin/env python3
"""
0-stream_users.py - Generator that streams rows from SQL database one by one
"""

import mysql.connector
from mysql.connector import Error
import seed


def stream_users():
    """
    Generator function that yields rows one by one from the user_data table.
    Uses yield to create a generator that fetches data lazily.
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = seed.connect_to_prodev()
        
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Execute query to fetch all users
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Yield each row one by one
            for row in cursor:
                yield row
                
    except Error as e:
        print(f"Error streaming users: {e}")
    
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    # Test the generator
    from itertools import islice
    
    print("Testing stream_users generator (first 3 rows):")
    for user in islice(stream_users(), 3):
        print(user)
