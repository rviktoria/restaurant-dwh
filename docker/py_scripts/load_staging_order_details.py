import psycopg2
from psycopg2 import Error
from datetime import datetime

def insert_log(conn_dest, task_name, status, start_time=None, end_time=None, records_processed=None, error_message=None):
    try:
        cur = conn_dest.cursor()
        run_timestamp = datetime.now()
        cur.execute("""
            INSERT INTO restaurant.replication_logs 
            (run_timestamp, start_time, end_time, task_name, status, records_processed, error_message) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (run_timestamp, start_time, end_time, task_name, status, records_processed, error_message))
        conn_dest.commit()
    except Error as e:
        print("Error inserting log:", e)

def load_staging_order_details():
    try:
        # Connect to restaurant_db
        conn_source = psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="Admin!234",
            host="db",
            port="5432"
        )
        
        # Connect to restaurant_dwh
        conn_dest = psycopg2.connect(
            dbname="restaurant_dwh",
            user="postgres",
            password="Admin!234",
            host="db",
            port="5432"
        )

        # Log start of the process
        start_time = datetime.now()
        insert_log(conn_dest, "load_staging_order_details", "Running", start_time=start_time)

        # Open cursors
        cur_source = conn_source.cursor()
        cur_dest = conn_dest.cursor()

        # Truncate staging table in restaurant_dwh
        cur_dest.execute("TRUNCATE TABLE restaurant.staging_order_details")

        # Fetch data from restaurant_db and insert into restaurant_dwh
        cur_source.execute("SELECT order_details_id, order_id, item_id FROM restaurant.order_details")
        rows = cur_source.fetchall()
        
        # Calculate the number of records processed
        records_processed = len(rows)  # Assuming rows contains the fetched records
        
        for row in rows:
            order_details_id, order_id, item_id = row
            cur_dest.execute("INSERT INTO restaurant.staging_order_details (order_details_id, order_id, item_id, created_date, created_time) VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME)",
                             (order_details_id, order_id, item_id))
        
        # Log successful completion
        end_time = datetime.now()
        insert_log(conn_dest, "load_staging_order_details", "Success", start_time=start_time, end_time=end_time, records_processed=records_processed)   
        
        # Commit changes and close connections
        conn_dest.commit()
        print("Data copied successfully.")        
    except Error as e:
        # Log error and failure
        end_time = datetime.now()
        insert_log(conn_dest, "load_staging_order_details", "Failure", start_time=start_time, end_time=end_time, error_message=str(e))
        print("Error:", e)
        # Re-raise the exception
        raise        
    finally:
        # Close connections
        if conn_source:
            conn_source.close()
        if conn_dest:
            conn_dest.close()

# Call the function to copy data
load_staging_order_details()
