import sqlite3

class DatabaseConnection:
    """
    A custom class-based context manager for handling database connections.
    Automatically opens and closes database connections using __enter__ and __exit__ methods.
    """
    
    def __init__(self, database_name):
        """
        Initialize the context manager with database name.
        
        Args:
            database_name (str): Name of the database file
        """
        self.database_name = database_name
        self.connection = None
    
    def __enter__(self):
        """
        Enter the context manager - open database connection.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        self.connection = sqlite3.connect(self.database_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager - close database connection.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)  
            exc_tb: Exception traceback (if any)
        """
        if self.connection:
            self.connection.close()
        
        # Return False to propagate any exceptions
        return False

def create_sample_database():
    """
    Create a sample database with users table for testing.
    """
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
        ''')
        
        # Insert sample data
        sample_users = [
            (1, 'Alice Johnson', 'alice@example.com', 30),
            (2, 'Bob Smith', 'bob@example.com', 45),
            (3, 'Charlie Brown', 'charlie@example.com', 25),
            (4, 'Diana Prince', 'diana@example.com', 35),
            (5, 'Eve Wilson', 'eve@example.com', 50)
        ]
        
        cursor.executemany(
            'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
            sample_users
        )
        
        conn.commit()
        print("Sample database created successfully!")

def main():
    """
    Main function to demonstrate the DatabaseConnection context manager.
    """
    # Create sample database first
    create_sample_database()
    
    # Use the context manager to query the database
    print("\n=== Using DatabaseConnection Context Manager ===")
    
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        # Print the results
        print("Query Results:")
        print("ID | Name          | Email                | Age")
        print("-" * 50)
        
        for row in results:
            print(f"{row[0]:2} | {row[1]:12} | {row[2]:19} | {row[3]}")
    
    print("\nDatabase connection closed automatically!")

if __name__ == "__main__":
    main()
