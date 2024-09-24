
import psycopg2


def update_res_users(dbname='default_db_name', user='admin', password='admin'):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname='upward-production',
            user='odoov17',
            password='odoov17',
            host='localhost'
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute(f"UPDATE res_users SET login='{user}', password='{password}' WHERE id=2;")

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        print("Update successful.")

    except Exception as e:
        print("An error occurred:", e)


# Call the function
update_res_users('your_db_name')