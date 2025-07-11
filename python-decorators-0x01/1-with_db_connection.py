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

def transactional(func):
    """
    Decorator that manages database transactions.
    Automatically commits on success or rolls back on error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Begin transaction (SQLite is in autocommit mode by default)
            conn.execute("BEGIN")
            
            # Execute the function
            result = func(conn, *args, **kwargs)
            
            # Commit the transaction on success
            conn.commit()
            print("Transaction committed successfully")
            
            return result
        
        except Exception as e:
            # Rollback the transaction on error
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception
    
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage
if __name__ == "__main__":
    # Update user's email with automatic transaction handling
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("Email updated successfully")
    except Exception as e:
        print(f"Failed to update email: {e}")
