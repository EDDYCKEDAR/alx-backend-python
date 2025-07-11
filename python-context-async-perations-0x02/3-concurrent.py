import asyncio
import aiosqlite
import sqlite3

async def async_fetch_users():
    """
    Asynchronous function to fetch all users from the database.
    
    Returns:
        list: All users from the database
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        print(f"async_fetch_users: Retrieved {len(results)} users")
        return results

async def async_fetch_older_users():
    """
    Asynchronous function to fetch users older than 40.
    
    Returns:
        list: Users older than 40
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        print(f"async_fetch_older_users: Retrieved {len(results)} users older than 40")
        return results

async def fetch_concurrently():
    """
    Execute both async functions concurrently using asyncio.gather.
    
    Returns:
        tuple: Results from both queries
    """
    print("Starting concurrent database queries...")
    
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("Concurrent queries completed!")
    
    return all_users, older_users

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
        (8, 'Henry Ford', 'henry@example.com', 38),
        (9, 'Ivy Chen', 'ivy@example.com', 55),
        (10, 'Jack Brown', 'jack@example.com', 33)
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
        sample_users
    )
    
    conn.commit()
    conn.close()
    print("Sample database created successfully!")

def display_results(all_users, older_users):
    """
    Display the results from both queries in a formatted way.
    
    Args:
        all_users (list): All users from the database
        older_users (list): Users older than 40
    """
    print("\n=== Results from Concurrent Queries ===")
    
    print(f"\nAll Users ({len(all_users)} total):")
    print("ID | Name          | Email                | Age")
    print("-" * 50)
    for user in all_users:
        print(f"{user[0]:2} | {user[1]:12} | {user[2]:19} | {user[3]}")
    
    print(f"\nUsers Older Than 40 ({len(older_users)} total):")
    print("ID | Name          | Email                | Age")
    print("-" * 50)
    for user in older_users:
        print(f"{user[0]:2} | {user[1]:12} | {user[2]:19} | {user[3]}")

async def main():
    """
    Main async function to demonstrate concurrent database operations.
    """
    # Create sample database first
    create_sample_database()
    
    print("\n=== Concurrent Asynchronous Database Queries ===")
    
    # Run concurrent queries
    all_users, older_users = await fetch_concurrently()
    
    # Display results
    display_results(all_users, older_users)
    
    print("\n=== Performance Comparison ===")
    
    # Measure time for concurrent execution
    import time
    
    start_time = time.time()
    await fetch_concurrently()
    concurrent_time = time.time() - start_time
    
    # Measure time for sequential execution
    start_time = time.time()
    await async_fetch_users()
    await async_fetch_older_users()
    sequential_time = time.time() - start_time
    
    print(f"Concurrent execution time: {concurrent_time:.4f} seconds")
    print(f"Sequential execution time: {sequential_time:.4f} seconds")
    print(f"Time saved: {sequential_time - concurrent_time:.4f} seconds")

if __name__ == "__main__":
    # Run the concurrent fetch using asyncio.run()
    asyncio.run(main())
