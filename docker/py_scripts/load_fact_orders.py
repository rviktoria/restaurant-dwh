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

def load_fact_orders():
    try:
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
        insert_log(conn_dest, "load_fact_orders", "Running", start_time=start_time)

        # Open cursors
        cur_dest = conn_dest.cursor()

        # Delete existing records created on the current date from fact_orders table
        cur_dest.execute("DELETE FROM restaurant.fact_orders WHERE created_date = CURRENT_DATE")

        # Insert new records from pre_fact_view into fact_orders table
        cur_dest.execute("""
            INSERT INTO restaurant.fact_orders 
            (order_id, order_line, menu_category_key, menu_item_key, item_price, order_total_lines, order_total_price, date_key, order_date, created_date, created_time)
            SELECT 
                pfo.order_id,
                pfo.order_line,
                pfo.menu_category_key,
                pfo.menu_item_key,
                pfo.item_price,
                pfo.order_total_lines,
                pfo.order_total_price,
                pfo.order_date_key,
                pfo.order_date,
                CURRENT_DATE,
                CURRENT_TIME
            FROM 
                restaurant.v_pre_fact_orders AS pfo;
        """)

        # Get the number of records processed
        records_processed = cur_dest.rowcount

        # Log successful completion
        end_time = datetime.now()
        insert_log(conn_dest, "load_fact_orders", "Success", start_time=start_time, end_time=end_time, records_processed=records_processed)
        
        # Commit changes and close connections
        conn_dest.commit()
        print("Data updated successfully.")
    except Error as e:
        # Log error and failure
        end_time = datetime.now()
        insert_log(conn_dest, "load_staging_menu_category", "Failure", start_time=start_time, end_time=end_time, error_message=str(e))
        print("Error:", e)
        # Re-raise the exception
        raise        
    finally:
        # Close connections
        if conn_dest:
            conn_dest.close()

# Call the function to copy data
load_fact_orders()
