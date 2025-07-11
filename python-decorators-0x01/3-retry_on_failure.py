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

# Global cache dictionary
query_cache = {}

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Avoids redundant database calls by storing results in memory.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key based on function name and arguments
        # Extract the query from arguments
        query = None
        
        # Check if 'query' is in kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 1:  # First arg is conn, second should be query
            query = args[1]
        
        if query is None:
            # If no query found, execute without caching
            return func(*args, **kwargs)
        
        # Create cache key
        cache_key = f"{func.__name__}:{query}"
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[cache_key]
        
        # Execute the function and cache the result
        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        
        # Store in cache
        query_cache[cache_key] = result
        print(f"Result cached for query: {query}")
        
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # First call will cache the result
    print("First call:")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users\n")
    
    # Second call will use the cached result
    print("Second call:")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users_again)} users from cache\n")
    
    # Different query will not use cache
    print("Third call with different query:")
    specific_users = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
    print(f"Fetched {len(specific_users)} users")
