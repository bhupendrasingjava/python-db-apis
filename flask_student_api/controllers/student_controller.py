import logging
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from werkzeug.exceptions import BadRequest, InternalServerError

from services.student_service import (
    get_all_students,
    get_student_by_roll,
    create_student,
    update_student,
    delete_student,
    export_students_to_excel
)

# Logger setup
logger = logging.getLogger('student_api')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Students'],
    'responses': {
        200: {
            'description': 'List of all students',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'roll_number': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'age': {'type': 'integer'},
                        'grade': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_students():
    try:
        students = get_all_students()
        logger.info("Fetched all students")
        return jsonify(students)
    except Exception:
        logger.exception("Error fetching students")
        raise InternalServerError("Internal server error")

@student_bp.route('/<int:roll_number>', methods=['GET'])
@swag_from({
    'tags': ['Students'],
    'parameters': [
        {
            'name': 'roll_number',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Roll number of the student'
        }
    ],
    'responses': {
        200: {
            'description': 'Student details',
            'schema': {
                'type': 'object',
                'properties': {
                    'roll_number': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'grade': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Student not found'}
    }
})
def get_student(roll_number):
    try:
        student = get_student_by_roll(roll_number)
        if student:
            logger.info(f"Fetched student with roll number {roll_number}")
            return jsonify(student)
        logger.warning(f"Student with roll number {roll_number} not found")
        return jsonify({'error': 'Student not found'}), 404
    except Exception:
        logger.exception(f"Error fetching student {roll_number}")
        raise InternalServerError("Internal server error")

@student_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Students'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'age', 'grade'],
                'properties': {
                    'name': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'grade': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Student created',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'roll_number': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Invalid input'}
    }
})
def add_student():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'age', 'grade')):
            logger.warning("Invalid input data for student creation")
            raise BadRequest("Missing required fields: name, age, grade")
        roll_number = create_student(data)
        logger.info(f"Created student with roll number {roll_number}")
        return jsonify({'message': 'Student created', 'roll_number': roll_number}), 201
    except BadRequest as e:
        raise e
    except Exception:
        logger.exception("Error creating student")
        raise InternalServerError("Internal server error")

@student_bp.route('/<int:roll_number>', methods=['PUT'])
@swag_from({
    'tags': ['Students'],
    'parameters': [
        {
            'name': 'roll_number',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Roll number of the student to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'grade': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Student updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Student not found'},
        400: {'description': 'Invalid input'}
    }
})
def modify_student(roll_number):
    try:
        data = request.get_json()
        if not data:
            logger.warning("No data provided for student to update")
            raise BadRequest("No data provided")
        updated = update_student(roll_number, data)
        if updated:
            logger.info(f"Updated student with roll number {roll_number}")
            return jsonify({'message': 'Student updated'})
        logger.warning(f"Student with roll number {roll_number} not found for update")
        return jsonify({'error': 'Student not found'}), 404
    except BadRequest as e:
        raise e
    except Exception:
        logger.exception(f"Error updating student {roll_number}")
        raise InternalServerError("Internal server error")

@student_bp.route('/<int:roll_number>', methods=['DELETE'])
@swag_from({
    'tags': ['Students'],
    'parameters': [
        {
            'name': 'roll_number',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Roll number of the student to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Student deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Student not found'}
    }
})
def remove_student(roll_number):
    try:
        deleted = delete_student(roll_number)
        if deleted:
            logger.info(f"Deleted student with roll number {roll_number}")
            return jsonify({'message': 'Student deleted'})
        logger.warning(f"Student with roll number {roll_number} not found for deletion")
        return jsonify({'error': 'Student not found'}), 404
    except Exception:
        logger.exception(f"Error deleting student {roll_number}")
        raise InternalServerError("Internal server error")

@student_bp.route('/exportToExcel', methods=['GET'])
@swag_from({
    'tags': ['Students'],
    'responses': {
        200: {
            'description': 'Student data exported to Excel',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'file_path': {'type': 'string'}
                }
            }
        }
    }
})
def export_to_excel():
    try:
        file_path = export_students_to_excel()
        logger.info(f"Exported student data to Excel at {file_path}")
        return jsonify({"message": "Student data exported successfully", "file_path": file_path})
    except Exception:
        logger.exception("Error exporting student data to Excel")
        raise InternalServerError("Internal server error")
