#!/usr/bin/env python3
"""
1-batch_processing.py - Batch processing of large data using generators
"""

import mysql.connector
from mysql.connector import Error
import seed


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: A batch of user records as dictionaries
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = seed.connect_to_prodev()
        
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Get total count for pagination
            cursor.execute("SELECT COUNT(*) as total FROM user_data")
            total_rows = cursor.fetchone()['total']
            
            offset = 0
            
            # Fetch data in batches
            while offset < total_rows:
                cursor.execute(
                    f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}"
                )
                batch = cursor.fetchall()
                
                if not batch:
                    break
                    
                yield batch
                offset += batch_size
                
    except Error as e:
        print(f"Error streaming users in batches: {e}")
    
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Size of each batch to process
    """
    try:
        # Process each batch
        for batch in stream_users_in_batches(batch_size):
            # Filter users over 25 years old
            for user in batch:
                if user['age'] > 25:
                    print(user)
                    
    except Exception as e:
        print(f"Error in batch processing: {e}")


if __name__ == "__main__":
    # Test batch processing
    print("Testing batch processing with batch size 10:")
    batch_processing(10)
