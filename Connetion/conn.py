import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Function to create a connection to the PostgreSQL database
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to execute a query that does not return results (e.g., INSERT, UPDATE, DELETE)
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        
 # Function to execute a query that returns results (e.g., SELECT)       
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    
def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed successfully")
        
        
# Function to load database credentials from environment variables and create a connection
def connection():
    load_dotenv()

    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    print(db_name, db_user, db_password, db_host, db_port)
    return create_connection(db_name, db_user, db_password, db_host, db_port)