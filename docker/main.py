import os
import subprocess
import psycopg2
from psycopg2 import Error

# Function to execute Python scripts
def execute_python_scripts(script_name):
    script_path = os.path.join('./py_scripts', script_name)
    print(f"Executing Python script: {script_path}")
    try:
        subprocess.run(["python", script_path])
        print(f"Python script '{script_name}' executed successfully.")
    except Exception as e:
        print(f"Error executing Python script {script_name}: {e}")

# Function to execute SQL scripts
def execute_sql_scripts(db_name, script_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user="postgres",
            password="Admin!234",
            host="db",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        script_path = os.path.join('./sql_scripts', script_name)
        print(f"Executing SQL script: {script_path}")
        with open(script_path, 'r') as f:
            cur.execute(f.read())
        print("SQL script executed successfully.")

        # Commit and close the connection
        conn.commit()
        cur.close()
        conn.close()

    except Error as e:
        print(f"Error executing SQL script: {e}")

if __name__ == "__main__":
    
    # Execute scripts
    
    # Create databases
    execute_python_scripts('create_database_restaurant_db_postgres.py') #Step 1
    execute_python_scripts('create_database_restaurant_dwh_postgres.py') #Step 2
    
    # Create tables
    execute_sql_scripts('restaurant_db', 'create_tables_restaurant_db_postgres.sql') #Step 3
    execute_sql_scripts('restaurant_dwh', 'create_tables_restaurant_dwh_postgres.sql') #Step 4
    execute_sql_scripts('restaurant_dwh', 'create_log_restaurant_dwh_postgres.sql') #Step 5
    
    # Load stagins
    execute_python_scripts('load_staging_menu_category.py') #Step 6
    execute_python_scripts('load_staging_menu_items.py') #Step 7
    execute_python_scripts('load_staging_orders.py') #Step 8
    execute_python_scripts('load_staging_order_details.py') #Step 9
    
    # Load dims and facts    
    execute_sql_scripts('restaurant_dwh', 'load_tables_restaurant_dwh_postgres.sql') #Step 10
    
