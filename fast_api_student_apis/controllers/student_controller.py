import logging
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import JSONResponse
from models.models import Student



from services.student_service import (
    get_all_students,
    get_student_by_roll,
    create_student,
    update_student,
    delete_student,
    export_students_to_excel
)

router = APIRouter()
logger = logging.getLogger("student_api")

@router.get("/", response_model=list[Student], tags=["Students"])
async def get_students():
    try:
        students = get_all_students()
        logger.info("Fetched all students")
        return students
    except Exception:
        logger.exception("Error fetching students")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{roll_number}", response_model=Student, tags=["Students"])
async def get_student(roll_number: int = Path(..., description="Roll number of the student")):
    try:
        student = get_student_by_roll(roll_number)
        if student:
            logger.info(f"Fetched student with roll number {roll_number}")
            return student
        logger.warning(f"Student with roll number {roll_number} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception:
        logger.exception(f"Error fetching student {roll_number}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", status_code=201, tags=["Students"])
async def add_student(student: Student):
    try:
        roll_number = create_student(student.dict())
        logger.info(f"Created student with roll number {roll_number}")
        return {"message": "Student created", "roll_number": roll_number}
    except Exception:
        logger.exception("Error creating student")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{roll_number}", tags=["Students"])
async def modify_student(roll_number: int, student: Student):
    try:
        updated = update_student(roll_number, student.dict())
        if updated:
            logger.info(f"Updated student with roll number {roll_number}")
            return {"message": "Student updated"}
        logger.warning(f"Student with roll number {roll_number} not found for update")
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception:
        logger.exception(f"Error updating student {roll_number}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{roll_number}", tags=["Students"])
async def remove_student(roll_number: int):
    try:
        deleted = delete_student(roll_number)
        if deleted:
            logger.info(f"Deleted student with roll number {roll_number}")
            return {"message": "Student deleted"}
        logger.warning(f"Student with roll number {roll_number} not found for deletion")
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception:
        logger.exception(f"Error deleting student {roll_number}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/export/to-excel", tags=["Students"])
async def export_to_excel():
    
    try:
        file_path = export_students_to_excel()
        logger.info(f"Exported student data to Excel at {file_path}")
        return {"message": "Student data exported successfully", "file_path": file_path}
    except Exception:
        logger.exception("Error exporting student data to Excel")
        raise HTTPException(status_code=500, detail="Internal server error")

