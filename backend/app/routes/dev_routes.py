from flask import Blueprint, request, jsonify, current_app
from app.models import User, Doctor
from app import db
from typing import *
from app.utils import create_error_response, create_success_response, fetch_all_doctors, validate_phone_number
from http import HTTPStatus
from werkzeug.exceptions import BadRequest

api = Blueprint('dev_api', __name__)

@api.route('/get/users', methods=['GET'])
def get_users():
    """
    Endpoint to get all users from the database.

    Returns:
        JSON response containing list of doctors with their details:
            {
                "status": "success",
                "data": [
                    {
                        "ssn": int,
                        "name": str,
                        "phone": str,
                        "checkin_status": bool
                    },
                    ...
                ]
            }
    """
    try:
        users = User.query.all()
        
        if not users:
            return create_error_response(
                "No users available in the system",
                HTTPStatus.NOT_FOUND
            )
        
        users_data = [{
            "ssn": user.id,
            "name": user.name,
            "phone": user.phone,
            "checkin_status": user.checkin_status
        } for user in users]
        
        return create_success_response(
            users_data,
            HTTPStatus.OK
        )

    except BadRequest as e:
        return create_error_response(
            str(e),
            HTTPStatus.BAD_REQUEST
        )


@api.route('/add/user', methods=['POST'])
def add_user():
    """
    Endpoint to add a user to the database.

    Expected JSON format:
    {
        "ssn": str,
        "name": str,
        "phone": str 
    }

    Returns:
    {
        "status": "success",
        "response": "User added"
    }
    """

    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            raise BadRequest("Invalid JSON payload")

        # Validate the fields
        required_fields = ['ssn', 'name', 'phone']
        if not all(field in data for field in required_fields):
            raise BadRequest("Missing required fields")
        
        # Check for duplicate additions
        user = User.query.filter_by(ssn=data['ssn']).all()
        if len(user) > 0:
            raise BadRequest("User with this SSN already exists")
        
        try:
            phone = validate_phone_number(data['phone'])
        except ValueError as e:
            return create_error_response(
                f"Invalid phone number: {str(e)}",
                HTTPStatus.BAD_REQUEST
            )
        
        new_user = User(ssn=data['ssn'], name=data['name'], phone=phone)
        db.session.add(new_user)
        db.session.commit()

        return create_success_response(
            "User added",
            HTTPStatus.OK
        )

    except BadRequest as e:
        return create_error_response(
            str(e),
            HTTPStatus.BAD_REQUEST
        )


@api.route('/get/doctors', methods=['GET'])
def get_doctors():
    """
    Endpoint to get all doctors in the system.
    """
    return fetch_all_doctors()


@api.route('/add/doctor', methods=['POST'])
def add_doctor():
    """
    Endpoint to add a doctor to the database.

    Expected JSON format:
    {
        "ssn": str,
        "name": str,
        "specialties": str (csv), 
        "experience": int,
        "opd_rate": float
    }

    Returns:
    {
        "status": "success",
        "response": "Doctor added"
    }
    """

    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            raise BadRequest("Invalid JSON payload")

        # Validate the fields
        required_fields = ['ssn', 'name', 'specialties', 'experience', 'opd_rate']
        if not all(field in data for field in required_fields):
            raise BadRequest("Missing required fields")
        
        # Check for duplicate additions
        doctor = Doctor.query.filter_by(ssn=data['ssn']).all()
        if len(doctor) > 0:
            raise BadRequest("Doctor with this SSN already exists")

        new_doctor = Doctor(ssn=data['ssn'], name=data['name'], specialties=data['specialties'], experience=data['experience'], opd_rate=data['opd_rate'])
        db.session.add(new_doctor)
        db.session.commit()

        return create_success_response(
            "Doctor added",
            HTTPStatus.OK
        )
        
    except BadRequest as e:
        return create_error_response(
            str(e),
            HTTPStatus.BAD_REQUEST
        )
    except TypeError as e:
        return create_error_response(
            f"Type error: {str(e)}",
            HTTPStatus.BAD_REQUEST
        )
