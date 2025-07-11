import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that handles both database connection and query execution.
    Takes a query and parameters as input and manages the entire process.
    """
    
    def __init__(self, database_name, query, parameters=None):
        """
        Initialize the context manager with database name, query, and parameters.
        
        Args:
            database_name (str): Name of the database file
            query (str): SQL query to execute
            parameters (tuple): Parameters for the query (optional)
        """
        self.database_name = database_name
        self.query = query
        self.parameters = parameters or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager - open connection and execute query.
        
        Returns:
            list: Query results
        """
        # Open database connection
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters
        if self.parameters:
            self.cursor.execute(self.query, self.parameters)
        else:
            self.cursor.execute(self.query)
        
        # Fetch results
        self.results = self.cursor.fetchall()
        
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager - close cursor and connection.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            self.connection.close()
        
        # Return False to propagate any exceptions
        return False

def create_sample_database():
    """
    Create a sample database with users table for testing.
    """
    conn = sqlite3.connect('users.db')
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
    
    # Insert sample data with various ages
    sample_users = [
        (1, 'Alice Johnson', 'alice@example.com', 30),
        (2, 'Bob Smith', 'bob@example.com', 45),
        (3, 'Charlie Brown', 'charlie@example.com', 25),
        (4, 'Diana Prince', 'diana@example.com', 35),
        (5, 'Eve Wilson', 'eve@example.com', 50),
        (6, 'Frank Miller', 'frank@example.com', 28),
        (7, 'Grace Lee', 'grace@example.com', 42),
        (8, 'Henry Ford', 'henry@example.com', 38)
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
        sample_users
    )
    
    conn.commit()
    conn.close()
    print("Sample database created successfully!")

def main():
    """
    Main function to demonstrate the ExecuteQuery context manager.
    """
    # Create sample database first
    create_sample_database()
    
    print("\n=== Using ExecuteQuery Context Manager ===")
    
    # Use the context manager to execute the query
    with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
        print("Query: SELECT * FROM users WHERE age > 25")
        print("Results:")
        print("ID | Name          | Email                | Age")
        print("-" * 50)
        
        for row in results:
            print(f"{row[0]:2} | {row[1]:12} | {row[2]:19} | {row[3]}")
    
    print("\nDatabase connection and cursor closed automatically!")
    
    # Demonstrate with different queries
    print("\n=== Additional Query Examples ===")
    
    # Query all users
    with ExecuteQuery('users.db', "SELECT * FROM users") as results:
        print(f"\nTotal users in database: {len(results)}")
    
    # Query users older than 40
    with ExecuteQuery('users.db', "SELECT name, age FROM users WHERE age > ?", (40,)) as results:
        print(f"\nUsers older than 40:")
        for row in results:
            print(f"  - {row[0]} (age {row[1]})")

if __name__ == "__main__":
    main()
