import psycopg

# Database connection parameters
host = "localhost"
port = 5432
database = "employee"
user = "postgres"
password = "postgres"

# Connect to the PostgreSQL database
try:
    # Establish connection using psycopg
    conn = psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password
    )

    # Open a cursor to perform database operations
    with conn.cursor() as cursor:
        # Execute query to fetch all records from employees table
        cursor.execute("SELECT id, email_id, first_name, last_name FROM employees;")
        records = cursor.fetchall()

        # Print the records
        for record in records:
            print(f"ID: {record[0]}, Email: {record[1]}, First Name: {record[2]}, Last Name: {record[3]}")

    # Close the connection
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
