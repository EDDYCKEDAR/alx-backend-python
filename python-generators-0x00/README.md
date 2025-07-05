# Python Generators with MySQL Database

This project demonstrates the use of Python generators for efficient database operations with MySQL. The implementation focuses on memory-efficient data processing using generators to stream, batch process, and paginate large datasets.

## Project Structure

```
python-generators-0x00/
├── seed.py                 # Database setup and seeding
├── 0-stream_users.py       # Generator for streaming database rows
├── 1-batch_processing.py   # Batch processing with generators
├── 2-lazy_paginate.py      # Lazy loading paginated data
├── 4-stream_ages.py        # Memory-efficient age aggregation
├── user_data.csv           # Sample CSV data for seeding
├── README.md              # This file
└── test_scripts/          # Test scripts for each module
    ├── 0-main.py
    ├── 1-main.py
    ├── 2-main.py
    └── 3-main.py
```

## Requirements

### System Requirements
- Python 3.7+
- MySQL Server 5.7+
- MySQL Connector Python

### Python Packages
```bash
pip install mysql-connector-python
```

## Database Setup

### 1. MySQL Configuration
Make sure MySQL is running and update the database credentials in `seed.py`:
```python
# Update these values in seed.py
host='localhost'
user='your_mysql_username'
password='your_mysql_password'
```

### 2. Database Schema
The project creates a database `ALX_prodev` with the following table structure:

```sql
CREATE TABLE user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(3,0) NOT NULL,
    INDEX idx_user_id (user_id)
);
```

## Files Description

### seed.py
Database setup and seeding script that:
- Connects to MySQL server
- Creates the `ALX_prodev` database
- Creates the `user_data` table
- Populates the table with sample data from CSV

**Functions:**
- `connect_db()`: Connects to MySQL database server
- `create_database(connection)`: Creates the ALX_prodev database
- `connect_to_prodev()`: Connects to the ALX_prodev database
- `create_table(connection)`: Creates the user_data table
- `insert_data(connection, data)`: Inserts data from CSV file

### 0-stream_users.py
Generator that streams database rows one by one for memory-efficient processing.

**Functions:**
- `stream_users()`: Generator that yields user records one by one

**Usage:**
```python
from itertools import islice

# Get first 6 users
for user in islice(stream_users(), 6):
    print(user)
```

### 1-batch_processing.py
Batch processing implementation for handling large datasets efficiently.

**Functions:**
- `stream_users_in_batches(batch_size)`: Generator that fetches data in batches
- `batch_processing(batch_size)`: Processes batches to filter users over age 25

**Usage:**
```python
# Process users in batches of 50
batch_processing(50)
```

### 2-lazy_paginate.py
Lazy loading pagination implementation that fetches pages only when needed.

**Functions:**
- `paginate_users(page_size, offset)`: Fetches a specific page of users
- `lazy_pagination(page_size)`: Generator for lazy page loading

**Usage:**
```python
# Iterate through pages of 100 users each
for page in lazy_pagination(100):
    for user in page:
        print(user)
```

### 4-stream_ages.py
Memory-efficient aggregation using generators to calculate average age.

**Functions:**
- `stream_user_ages()`: Generator that yields user ages one by one
- `calculate_average_age()`: Calculates average age without loading all data

**Usage:**
```python
# Calculate average age efficiently
average_age = calculate_average_age()
print(f"Average age of users: {average_age:.2f}")
```

## Running the Project

### 1. Database Setup
```bash
# Run the seed script to set up database and populate data
python seed.py
```

### 2. Test Individual Components

#### Stream Users Test
```bash
python 0-stream_users.py
```

#### Batch Processing Test
```bash
python 1-batch_processing.py
```

#### Lazy Pagination Test
```bash
python 2-lazy_paginate.py
```

#### Age Aggregation Test
```bash
python 4-stream_ages.py
```

### 3. Using Provided Test Scripts

```bash
# Test database setup
python 0-main.py

# Test user streaming
python 1-main.py

# Test batch processing
python 2-main.py

# Test lazy pagination
python 3-main.py
```

## Key Concepts Demonstrated

### 1. Generator Functions
- Use of `yield` keyword for lazy evaluation
- Memory-efficient data processing
- Iterator protocol implementation

### 2. Database Streaming
- Cursor-based data retrieval
- Connection management
- Memory-efficient database operations

### 3. Batch Processing
- Fixed-size batch processing
- Offset-based pagination
- Filtering and transformation

### 4. Lazy Loading
- On-demand data fetching
- Page-by-page data retrieval
- Memory optimization

### 5. Aggregation
- Streaming aggregation functions
- Memory-efficient calculations
- Real-time data processing

## Performance Benefits

1. **Memory Efficiency**: Generators process data one item at a time
2. **Lazy Evaluation**: Data is fetched only when needed
3. **Scalability**: Can handle datasets larger than available memory
4. **Resource Management**: Proper connection handling and cleanup

## Error Handling

All scripts include comprehensive error handling for:
- Database connection failures
- SQL execution errors
- File I/O errors
- Resource cleanup in finally blocks

## Best Practices Implemented

1. **Context Management**: Proper resource cleanup
2. **Error Handling**: Comprehensive exception handling
3. **Documentation**: Clear docstrings and comments
4. **Code Organization**: Modular function design
5. **Testing**: Test scripts for validation

## Notes

- The project uses UUID for user_id generation
- Database connections are properly managed with cleanup
- All generators follow the iterator protocol
- Code is optimized for memory efficiency over speed
- CSV data is provided as sample data for testing

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**: Check MySQL server status and credentials
2. **CSV File Not Found**: Ensure `user_data.csv` exists in the project directory
3. **Permission Errors**: Verify MySQL user has necessary privileges
4. **Memory Issues**: Generators should handle large datasets efficiently

### Database Connection Issues
```python
# Check MySQL service status
sudo systemctl status mysql

# Verify database exists
mysql -u root -p -e "SHOW DATABASES;"
```

## License

This project is part of the ALX Backend Python curriculum and is for educational purposes.
