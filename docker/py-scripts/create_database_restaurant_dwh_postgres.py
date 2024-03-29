import psycopg2
from psycopg2 import OperationalError 

def drop_database():
    try:
        # Connect to the default PostgreSQL database (e.g., postgres or any other existing database)
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Admin!234",
            host="localhost",
            port="5432"
        )
        
        # Set autocommit to True to ensure DROP DATABASE is not run inside a transaction block
        conn.autocommit = True

        # Create a cursor object
        cur = conn.cursor()
        
        # Drop the database if it exists
        cur.execute("DROP DATABASE IF EXISTS restaurant_dwh")

        # Commit the transaction
        conn.commit()
        print("Database dropped successfully.")

    except OperationalError as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()
            
            
def create_database():
    try:
        # Connect to the default PostgreSQL database (e.g., postgres or any other existing database)
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Admin!234",
            host="localhost",
            port="5432"
        )
        
        # Set autocommit to True to ensure CREATE DATABASE is not run inside a transaction block
        conn.autocommit = True

        # Create a cursor object
        cur = conn.cursor()       
 
        # Create a new database
        cur.execute("CREATE DATABASE restaurant_dwh")

        # Commit the transaction
        conn.commit()
        print("Database created successfully.")

    except OperationalError as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

# Call the function to drop and create the database
drop_database()
create_database()
