"""
Complete Python Decorators for Database Operations
This module demonstrates all the decorator patterns for database management.
"""

import sqlite3
import functools
import time

# Global cache for query results
query_cache = {}

def log_queries(func):
    """
    Decorator to log SQL queries before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            query = args[0]
        else:
            query = "Unknown query"
        
        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    
    return wrapper

def with_db_connection(func):
    """
    Decorator that automatically handles database connections.
    Opens a connection, passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    
    return wrapper

def transactional(func):
    """
    Decorator that manages database transactions.
    Automatically commits on success or rolls back on error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            conn.execute("BEGIN")
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed successfully")
            return result
        
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries database operations on failure.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(retries + 1):
                try:
                    result = func(*args, **kwargs)
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
            
            raise last_exception
        
        return wrapper
    return decorator

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query for cache key
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 1:
            query = args[1]
        
        if query is None:
            return func(*args, **kwargs)
        
        cache_key = f"{func.__name__}:{query}"
        
        if cache_key in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[cache_key]
        
        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        query_cache[cache_key] = result
        print(f"Result cached for query: {query}")
        
        return result
    
    return wrapper

# Example usage functions
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Demo function
def demo_all_decorators():
    """Demonstrate all decorators in action"""
    print("=== Database Decorators Demo ===\n")
    
    # Create a simple users table for testing
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Jane Smith', 'jane@example.com')")
    conn.commit()
    conn.close()
    
    print("1. Testing log_queries decorator:")
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users\n")
    
    print("2. Testing with_db_connection decorator:")
    user = get_user_by_id(user_id=1)
    print(f"User: {user}\n")
    
    print("3. Testing transactional decorator:")
    update_user_email(user_id=1, new_email='newemail@example.com')
    print()
    
    print("4. Testing retry_on_failure decorator:")
    users = fetch_users_with_retry()
    print(f"Fetched {len(users)} users with retry\n")
    
    print("5. Testing cache_query decorator:")
    users1 = fetch_users_with_cache(query="SELECT * FROM users")
    users2 = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"First call: {len(users1)} users, Second call: {len(users2)} users\n")

if __name__ == "__main__":
    demo_all_decorators()
