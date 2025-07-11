import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Decorator to log SQL queries before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Check if 'query' is in kwargs or args
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            # Assume first argument is the query if not in kwargs
            query = args[0]
        else:
            query = "Unknown query"
        
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    # This will log the query before executing
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")
