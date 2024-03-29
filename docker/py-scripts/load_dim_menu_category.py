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

def load_dim_menu_category():
    try:
        # Connect to restaurant_dwh
        conn_dest = psycopg2.connect(
            dbname="restaurant_dwh",
            user="postgres",
            password="Admin!234",
            host="localhost",
            port="5432"
        )

        # Log start of the process
        start_time = datetime.now()
        insert_log(conn_dest, "load_dim_menu_category", "Running", start_time=start_time)

        # Open cursor
        cur_dest = conn_dest.cursor()

        # Get count of records before merge
        cur_dest.execute("SELECT COUNT(*) FROM restaurant.dim_menu_category")
        records_before = cur_dest.fetchone()[0]

        # Merge data into dim_menu_category table with SCD logic
        cur_dest.execute("""
            MERGE INTO restaurant.dim_menu_category AS target
            USING restaurant.v_pre_dim_menu_category AS source 
            ON target.menu_category_name_id = source.menu_category_name_id
            WHEN MATCHED 
            AND (target.menu_category_name_eng <> source.menu_category_name_eng)
            THEN
                UPDATE 
                SET 
                    menu_category_name_eng = source.menu_category_name_eng,
                    modified_date = CURRENT_DATE,
                    modified_time = CURRENT_TIME
                    
            WHEN NOT MATCHED THEN
                INSERT (menu_category_name_id, menu_category_name_eng, created_date, created_time, modified_date, modified_time)
                VALUES (source.menu_category_name_id, source.menu_category_name_eng, CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');	
        """)

        # Get count of records after merge
        cur_dest.execute("SELECT COUNT(*) FROM restaurant.dim_menu_category")
        records_after = cur_dest.fetchone()[0]

        # Calculate the number of records processed
        records_processed = records_after - records_before

        # Log successful completion
        end_time = datetime.now()
        insert_log(conn_dest, "load_dim_menu_category", "Success", start_time=start_time, end_time=end_time, records_processed=records_processed)
        
        # Commit changes and close connection
        conn_dest.commit()
        print("Data updated successfully.")
    except Error as e:
        # Log error and failure
        end_time = datetime.now()
        insert_log(conn_dest, "load_dim_menu_category", "Failure", start_time=start_time, end_time=end_time, error_message=str(e))
        print("Error:", e)
        # Re-raise the exception to ensure it's propagated
        raise e
    finally:
        # Close connection
        if conn_dest:
            conn_dest.close()

# Call the function to load dim_menu_category table
load_dim_menu_category()
