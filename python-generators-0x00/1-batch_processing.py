#!/usr/bin/python3
"""
Batch processing module using generators for memory-efficient streaming.
"""

import mysql.connector
from mysql.connector import Error


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        return mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',
            password='root'
        )
    except Error as e:
        print(f"Error: {e}")
        return  # Exit early if connection fails


def stream_users_in_batches(batch_size):
    """
    Generator that yields user data in batches.
    """
    connection = connect_to_prodev()
    if not connection:
        return  # Exit if DB connection fails

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and prints those older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
    return  # Not required, but harmless to signal end of function
