import psycopg

# Database connection parameters
host = "localhost"
port = 5432
database = "employee"
user = "postgres"
password = "postgres"

# List of new student records to insert
new_students = [
    ("Alice", "Smith", 21, "alice.smith@example.com"),
    ("Bob", "Johnson", 22, "bob.johnson@example.com"),
    ("Carol", "Williams", 20, "carol.williams@example.com"),
    ("David", "Brown", 23, "david.brown@example.com"),
    ("Eve", "Davis", 19, "eve.davis@example.com")
]

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
        # Insert multiple records into the student table
        cursor.executemany("""
            INSERT INTO school.student (first_name, last_name, age, email_address)
            VALUES (%s, %s, %s, %s);
        """, new_students)

    conn.commit()
    conn.close()
    print("5 new student records inserted successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
