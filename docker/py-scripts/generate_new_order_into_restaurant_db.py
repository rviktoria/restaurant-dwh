import psycopg2
import random
from psycopg2 import Error

def add_order(conn):
    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Add a record to the orders table
        cur.execute("INSERT INTO restaurant.orders (order_date, order_time) VALUES (CURRENT_DATE, CURRENT_TIME) RETURNING order_id;")
        order_id = cur.fetchone()[0]  # Retrieve the generated order_id

        # Commit the transaction
        conn.commit()

        return order_id
    except Error as e:
        print("Error:", e)
        conn.rollback()
    finally:
        # Close the cursor
        cur.close()

def add_order_details(conn, order_id):
    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Retrieve a list of all menu_item_ids
        cur.execute("SELECT menu_item_id FROM restaurant.menu_items;")
        menu_item_ids = [row[0] for row in cur.fetchall()]

        # Generate random order details
        for _ in range(random.randint(1, 5)):
            item_id = random.choice(menu_item_ids)  # Select a random menu_item_id
            cur.execute("INSERT INTO restaurant.order_details (order_id, item_id) VALUES (%s, %s);", (order_id, item_id))

        # Commit the transaction
        conn.commit()
    except Error as e:
        print("Error:", e)
        conn.rollback()
    finally:
        # Close the cursor
        cur.close()

def main():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="Admin!234",
            host="localhost",
            port="5432"
        )

        # Add a record to the orders table and retrieve the generated order_id
        order_id = add_order(conn)

        # Add order details for the generated order_id
        add_order_details(conn, order_id)

        print("Data added successfully.")
    except Error as e:
        print("Error:", e)
    finally:
        # Close the database connection
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
