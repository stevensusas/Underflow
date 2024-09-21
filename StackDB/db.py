import pandas as pd
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

def create_tables(connection, database_name):
    """
    Creates the 'providers' and 'services' tables with the appropriate schema and relationships.

    :param connection: MySQL connection object.
    :param database_name: Name of the database to use.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name};")
        
        # SQL statement to create 'providers' table
        create_providers_table = """
        CREATE TABLE IF NOT EXISTS providers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(100),
            detailed_description TEXT
        );
        """

        # SQL statement to create 'services' table
        create_services_table = """
        CREATE TABLE IF NOT EXISTS services (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            cost_per_user_per_hour DECIMAL(10,4),
            detailed_description TEXT,
            type VARCHAR(100),
            service_provider_id INT,
            traffic_upperbound INT,
            FOREIGN KEY (service_provider_id) REFERENCES providers(id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
        );
        """

        # Execute table creation
        cursor.execute(create_providers_table)
        cursor.execute(create_services_table)
        connection.commit()
        print("Tables 'providers' and 'services' created successfully.")
    
    except Error as e:
        print(f"Error: '{e}' occurred while creating tables.")
    finally:
        if cursor:
            cursor.close()

def insert_providers(connection, database_name, providers_df):
    """
    Inserts data into the 'providers' table.

    :param connection: MySQL connection object.
    :param database_name: Name of the database to use.
    :param providers_df: pandas DataFrame containing providers data.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name};")

        # Prepare data: ensure 'Name' is unique
        providers_data = providers_df[['Name', 'Type', 'Detailed Description']].drop_duplicates(subset=['Name'])

        insert_providers_query = """
        INSERT INTO providers (name, type, detailed_description)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            type = VALUES(type),
            detailed_description = VALUES(detailed_description);
        """

        providers_tuples = list(providers_data.itertuples(index=False, name=None))
        cursor.executemany(insert_providers_query, providers_tuples)
        connection.commit()
        print(f"Inserted/Updated {cursor.rowcount} rows into 'providers' table.")

    except Error as e:
        print(f"Error: '{e}' occurred while inserting into 'providers' table.")
    finally:
        if cursor:
            cursor.close()

def fetch_provider_id_map(connection, database_name):
    """
    Fetches a mapping from provider name to provider ID.

    :param connection: MySQL connection object.
    :param database_name: Name of the database to use.
    :return: Dictionary mapping provider names to their IDs.
    """
    provider_id_map = {}
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name};")
        cursor.execute("SELECT id, name FROM providers;")
        results = cursor.fetchall()
        provider_id_map = {name: id for (id, name) in results}
    except Error as e:
        print(f"Error: '{e}' occurred while fetching provider IDs.")
    finally:
        if cursor:
            cursor.close()
    return provider_id_map

def insert_services(connection, database_name, services_df, provider_id_map):
    """
    Inserts data into the 'services' table.

    :param connection: MySQL connection object.
    :param database_name: Name of the database to use.
    :param services_df: pandas DataFrame containing services data.
    :param provider_id_map: Dictionary mapping provider names to IDs.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name};")

        services_data = services_df.copy()

        # Map 'Service Provider' to 'service_provider_id'
        services_data['service_provider_id'] = services_data['Service Provider'].map(provider_id_map)

        # Identify services with missing providers
        missing_providers = services_data[services_data['service_provider_id'].isnull()]['Service Provider'].unique()
        if len(missing_providers) > 0:
            print("Warning: The following service providers were not found in the 'providers' table:")
            for provider in missing_providers:
                print(f"- {provider}")
            print("These services will have NULL as their service_provider_id.")

        # Prepare data for insertion
        services_insert_data = services_data[['Name', 'Cost per user per hour', 'Detailed Description',
                                              'Type', 'service_provider_id', 'Traffic upperbound']]

        # Replace NaN with None for SQL NULL
        services_insert_data = services_insert_data.where(pd.notnull(services_insert_data), None)

        insert_services_query = """
        INSERT INTO services (name, cost_per_user_per_hour, detailed_description, type, service_provider_id, traffic_upperbound)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            cost_per_user_per_hour = VALUES(cost_per_user_per_hour),
            detailed_description = VALUES(detailed_description),
            type = VALUES(type),
            service_provider_id = VALUES(service_provider_id),
            traffic_upperbound = VALUES(traffic_upperbound);
        """

        services_tuples = list(services_insert_data.itertuples(index=False, name=None))
        cursor.executemany(insert_services_query, services_tuples)
        connection.commit()
        print(f"Inserted/Updated {cursor.rowcount} rows into 'services' table.")

    except Error as e:
        print(f"Error: '{e}' occurred while inserting into 'services' table.")
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

    # Paths to your CSV files
    providers_csv = 'service_providers.csv'  # Replace with the path to your first CSV file
    services_csv = 'specific_services.csv'    # Replace with the path to your second CSV file

    # Read CSV files into pandas DataFrames
    try:
        providers_df = pd.read_csv(providers_csv)
        services_df = pd.read_csv(services_csv)
        print("CSV files loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV files: {e}")
        return

    # Establish connection
    connection = create_mysql_connection(host, port, user, password)

    if connection:
        try:
            # Create the database
            create_database(connection, database_name)

            # Create the tables
            create_tables(connection, database_name)

            # Insert data into 'providers' table
            insert_providers(connection, database_name, providers_df)

            # Fetch provider ID mapping
            provider_id_map = fetch_provider_id_map(connection, database_name)

            # Insert data into 'services' table
            insert_services(connection, database_name, services_df, provider_id_map)

        finally:
            # Close connection
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    main()
