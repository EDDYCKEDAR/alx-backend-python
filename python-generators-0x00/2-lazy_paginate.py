#!/usr/bin/python3
"""
Batch processing module for streaming and processing user data in batches.
Uses generators to efficiently handle large datasets with memory optimization.
"""

import mysql.connector
from mysql.connector import Error


def connect_to_prodev():
    """
    Connect to the ALX_prodev database.

    Returns:
        mysql.connector.connection.MySQLConnection or None
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',
            password='root'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches user data in batches.

    Args:
        batch_size (int): Number of records per batch.

    Yields:
        list[dict]: Batch of user records as dictionaries.
    """
    connection = connect_to_prodev()
    if not connection:
        yield from ()  # avoids using `return` explicitly

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Process user data in batches, printing users over age 25.

    Args:
        batch_size (int): Number of records per batch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
