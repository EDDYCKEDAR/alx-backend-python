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
        mysql.connector.connection: Database connection object or None if failed
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
    Generator function that fetches user data from database in batches.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
        
    Yields:
        list: Batch of user records as dictionaries
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        while True:
            # Fetch batch_size number of rows
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
    Process user data in batches, filtering users over age 25.
    
    Args:
        batch_size (int): Number of rows to process per batch
    """
    # Use the stream_users_in_batches generator to get batches
    for batch in stream_users_in_batches(batch_size):
        # Process each user in the current batch
        for user in batch:
            # Filter users over age 25
            if user['age'] > 25:
                print(user)
