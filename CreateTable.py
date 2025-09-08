import psycopg

# Database connection parameters
host = "localhost"
port = 5432
database = "employee"
user = "postgres"
password = "postgres"

try:
    # Connect to the PostgreSQL database
    conn = psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password
    )

    with conn.cursor() as cursor:
        # Create schema
        cursor.execute("CREATE SCHEMA IF NOT EXISTS school;")

        # Create student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS school.student (
                roll_number SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                age INTEGER,
                email_address VARCHAR(100)
            );
        """)

        # Insert a single record
        cursor.execute("""
            INSERT INTO school.student (first_name, last_name, age, email_address)
            VALUES (%s, %s, %s, %s);
        """, ("John", "Doe", 20, "john.doe@example.com"))

    conn.commit()
    conn.close()
    print("Schema and student table created successfully, and one record inserted.")

except Exception as e:
    print(f"An error occurred: {e}")
