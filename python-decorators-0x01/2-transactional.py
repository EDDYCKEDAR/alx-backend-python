import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles database connections.
    Opens a connection, passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        
        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()
    
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries database operations on failure.
    
    Args:
        retries (int): Number of retry attempts (default: 3)
        delay (int): Delay between retries in seconds (default: 2)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(retries + 1):  # +1 to include the initial attempt
                try:
                    # Try to execute the function
                    result = func(*args, **kwargs)
                    
                    # If successful, return the result
                    if attempt > 0:
                        print(f"Operation succeeded on attempt {attempt + 1}")
                    return result
                
                except Exception as e:
                    last_exception = e
                    
                    if attempt < retries:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries + 1} attempts failed. Giving up.")
            
            # If all retries failed, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    try:
        # Attempt to fetch users with automatic retry on failure
        users = fetch_users_with_retry()
        print(f"Successfully fetched {len(users)} users")
    except Exception as e:
        print(f"Failed to fetch users after all retries: {e}")
