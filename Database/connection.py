from Database import sql_config
import psycopg
from contextlib import contextmanager

@contextmanager
def get_connection():
    connection = None
    try:
        connection = psycopg.connect(
            dbname=sql_config.DB_NAME,
            host=sql_config.DB_HOST,
            password=sql_config.DB_PASSWORD,
            user=sql_config.DB_USER,
            port=sql_config.DB_PORT
        )
        yield connection
        
    except psycopg.OperationalError as e:
        print("❌ Could not connect to PostgreSQL server.")
        print(f"💡 Detail: {e}")
        print("\nExiting program for safety...")
        
    except psycopg.Error as e:
        # This catches bugs inside your routes (like bad SQL syntax) and prints them to your console
        print(f"❌ Database Query Error: {e}")
        raise e  # Passes the error back up so you can see it in your browser/Postman
        
    finally:
        if connection is not None:
            connection.close()
