#!/usr/bin/env python3
"""
4-stream_ages.py - Memory-efficient aggregation with generators
"""

import mysql.connector
from mysql.connector import Error
import seed


def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    This allows for memory-efficient processing of large datasets.
    
    Yields:
        int: User age
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = seed.connect_to_prodev()
        
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            # Execute query to fetch only ages
            cursor.execute("SELECT age FROM user_data")
            
            # Yield each age one by one
            for (age,) in cursor:
                yield age
                
    except Error as e:
        print(f"Error streaming user ages: {e}")
    
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Calculate the average age of all users using the generator.
    This method is memory-efficient as it doesn't load all data at once.
    
    Returns:
        float: Average age of users
    """
    total_age = 0
    count = 0
    
    # Use the generator to process ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


if __name__ == "__main__":
    # Calculate and print the average age
    try:
        average_age = calculate_average_age()
        print(f"Average age of users: {average_age:.2f}")
    except Exception as e:
        print(f"Error calculating average age: {e}")
