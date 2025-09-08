import os
import logging
import pandas as pd
from db.connection import get_connection
from models.student import Student

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_all_students():
    logger.info("Start: get_all_students")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT roll_number, first_name, last_name, age, email_address 
                    FROM school.student;
                """)
                rows = cur.fetchall()
                students = [Student(*row).__dict__ for row in rows]
                logger.info("End: get_all_students")
                return students
    except Exception as e:
        logger.exception("Error in get_all_students")
        raise

def get_student_by_roll(roll_number):
    logger.info(f"Start: get_student_by_roll ({roll_number})")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT roll_number, first_name, last_name, age, email_address 
                    FROM school.student 
                    WHERE roll_number = %s;
                """, (roll_number,))
                row = cur.fetchone()
                logger.info(f"End: get_student_by_roll ({roll_number})")
                return Student(*row).__dict__ if row else None
    except Exception as e:
        logger.exception(f"Error in get_student_by_roll ({roll_number})")
        raise

def create_student(data):
    logger.info("Start: create_student")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO school.student (first_name, last_name, age, email_address)
                    VALUES (%s, %s, %s, %s) RETURNING roll_number;
                """, (
                    data['first_name'], 
                    data['last_name'], 
                    data['age'], 
                    data['email_address']
                ))
                conn.commit()
                roll_number = cur.fetchone()[0]
                logger.info(f"End: create_student (roll_number={roll_number})")
                return roll_number
    except Exception as e:
        logger.exception("Error in create_student")
        raise

def update_student(roll_number, data):
    logger.info(f"Start: update_student ({roll_number})")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE school.student
                    SET first_name = %s, last_name = %s, age = %s, email_address = %s
                    WHERE roll_number = %s;
                """, (
                    data['first_name'], 
                    data['last_name'], 
                    data['age'], 
                    data['email_address'], 
                    roll_number
                ))
                conn.commit()
                rowcount = cur.rowcount
                logger.info(f"End: update_student ({roll_number}) - Rows affected: {rowcount}")
                return rowcount
    except Exception as e:
        logger.exception(f"Error in update_student ({roll_number})")
        raise

def delete_student(roll_number):
    logger.info(f"Start: delete_student ({roll_number})")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM school.student 
                    WHERE roll_number = %s;
                """, (roll_number,))
                conn.commit()
                rowcount = cur.rowcount
                logger.info(f"End: delete_student ({roll_number}) - Rows affected: {rowcount}")
                return rowcount
    except Exception as e:
        logger.exception(f"Error in delete_student ({roll_number})")
        raise

def export_students_to_excel():
    logger.info("Start: export_students_to_excel")
    try:
        students = get_all_students()
        df = pd.DataFrame(students)
        output_path = r"C:\python-basics\docs\student_data.xlsx"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)
        logger.info(f"End: export_students_to_excel - File saved at {output_path}")
        return output_path
    except Exception as e:
        logger.exception("Error in export_students_to_excel")
        raise
