import mysql.connector

import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Database connection details
host = "localhost"
username = "root"
password = "admin123"
database = "travel_packages"

# Connect to the MySQL Database
connection = create_connection(host, username, password, database)

# SQL query for creating a table
create_packages_table = """
CREATE TABLE IF NOT EXISTS packages (
    id INT AUTO_INCREMENT,
    from_city VARCHAR(255) NOT NULL,
    to_city VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    package_type VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
"""

# Execute the query to create the table
execute_query(connection, create_packages_table)

def insert_packages_data(connection, data):
    cursor = connection.cursor()
    query = """
    INSERT INTO packages (from_city, to_city, cost, package_type)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, data)
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()

sample_data = [
    ("New York", "London", 1200.00, "Economy"),
    ("Dubai", "Tokyo", 800.00, "Business"),
    ("Berlin", "Moscow", 550.00, "Economy"),
    ("Sydney", "Paris", 1500.00, "First Class"),
    ("Mumbai", "Singapore", 700.00, "Economy"),
    ("Cairo", "Cape Town", 950.00, "Business"),
    ("Beijing", "Seoul", 300.00, "Economy"),
    ("San Francisco", "New York", 200.00, "Economy"),
    ("Toronto", "Vancouver", 400.00, "Business"),
    ("Sao Paulo", "Lisbon", 850.00, "Economy"),
    ("Los Angeles", "Bangkok", 1300.00, "First Class"),
    ("London", "New York", 1000.00, "Economy"),
    ("Istanbul", "Dubai", 550.00, "Business"),
    ("Hong Kong", "Shanghai", 250.00, "Economy"),
    ("Paris", "Rome", 350.00, "Economy"),
    ("Delhi", "Sydney", 1000.00, "Business"),
    ("Moscow", "Prague", 300.00, "Economy"),
    ("Mexico City", "Lima", 400.00, "Economy"),
    ("Jakarta", "Tokyo", 750.00, "Business"),
    ("Buenos Aires", "Miami", 900.00, "Economy"),
    ("Milan", "Madrid", 250.00, "Economy"),
    ("Bangkok", "Kuala Lumpur", 150.00, "Business"),
    ("Lisbon", "Barcelona", 200.00, "Economy"),
    ("Chicago", "Toronto", 300.00, "Economy"),
    ("Amsterdam", "Berlin", 160.00, "Business")
]


# Use the connection function and insert function
connection = create_connection(host, username, password, database)
if connection is not None:
    insert_packages_data(connection, sample_data)
    connection.close()
    print("MySQL connection is closed")


# Close the connection
if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")


