import mysql.connector
from mysql.connector import Error

def create_mysql_connection(host, port, user, password):
    """
    Establishes a connection to the MySQL database.

    :param host: RDS endpoint.
    :param port: Port number (default 3306).
    :param user: Username.
    :param password: Password.
    :return: MySQL connection object or None.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        if connection.is_connected():
            print("Successfully connected to MySQL Server.")
            return connection
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to MySQL.")
    return None

def create_database(connection, database_name):
    """
    Creates a new database.

    :param connection: MySQL connection object.
    :param database_name: Name of the database to create.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        print(f"Database '{database_name}' created or already exists.")
    except Error as e:
        print(f"Error: '{e}' occurred while creating the database.")
    finally:
        if cursor:
            cursor.close()

def main():
    # Hardcoded RDS connection details
    host = 'stackunderflow.cha8ies4obs2.us-east-1.rds.amazonaws.com'  # Replace with your RDS endpoint
    port = 3306  # MySQL default port
    user = 'admin'  # Replace with your MySQL username
    password = '12345678'  # Replace with your MySQL password
    database_name = 'StackUnderflow'  # Replace with the database name you want to create

    # Establish connection
    connection = create_mysql_connection(host, port, user, password)

    if connection:
        # Create the database
        create_database(connection, database_name)

        # Close connection
        connection.close()
        print("MySQL connection is closed.")

if __name__ == "__main__":
    main()


# 