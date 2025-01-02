from flask import Blueprint, request, jsonify, current_app
from app.models import User, Doctor
from app import db
from typing import *
from app.utils import query_builder, validate_phone_number, create_error_response, create_success_response, fetch_all_doctors
from http import HTTPStatus
from werkzeug.exceptions import BadRequest

api = Blueprint('patient_api', __name__)
    
@api.route('/auth', methods=['POST'])
def authenticate_patient():
    """
    Authenticate a patient using SSN and phone number.

    Args:
        JSON payload containing:
            ssn (str): Social Security Number of the patient
            phone (str): Phone number of the patient for 2FA

    Returns:
        JSON response with authentication status
        
    Raises:
        BadRequest: If required fields are missing or invalid
        ValueError: If phone number format is invalid

    TODO: Add 2FA
    """

    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            raise BadRequest("Invalid JSON payload")
        
        required_fields = ['ssn', 'phone']
        if not all(field in data for field in required_fields):
            raise BadRequest("Missing required fields")

        ssn = data['ssn']  
        
        query = query_builder({"ssn": ssn}, "all", "ssn")

        if len(query) > 1:
            return create_error_response(
                "Multiple users found with the same SSN",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
        if len(query) == 0:
            return create_error_response(
                "User not registered",
                HTTPStatus.NOT_FOUND
            )
        
        user = query[0]

        try:
            phone = validate_phone_number(data['phone'])
        except ValueError as e:
            return create_error_response(
                f"Invalid phone number: {str(e)}",
                HTTPStatus.BAD_REQUEST
            )

        if phone != user.phone:
            return create_error_response(
                "Incorrect phone number associated with SSN",
                HTTPStatus.UNAUTHORIZED
            )

        return create_success_response(
            "Authentication successful",
            HTTPStatus.OK
        )

    except BadRequest as e:
        return create_error_response(
            str(e), 
            HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        return create_error_response(
            "Internal server error",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )


@api.route('/checkin', methods=['POST'])
def checkin():
    """
    Checkin method to update the checkin status of the user.
    """

    data = request.json

    query = query_builder(data, "all", "ssn")

    # Error handling to make sure there's only one user with the ssn
    if len(query) > 1:
        return jsonify({"error": "Multiple users found with the same SSN"}), 409 # Conflict
    elif len(query) == 0:
        # TODO: Redirect to registration
        return jsonify({"error": "User not registered"}), 400
    
    user = query[0]
    if user.checkin_status:
        return jsonify({"message": "User already checked in"}), 200
    
    user.checkin_status = True
    db.session.commit()

    return jsonify({"message": "Authenticated"}), 200


@api.route('/doctors', methods=['GET'])
def fetch_doctors():
    """
    Fetch all available doctors from the system.

    Returns:
        JSON response containing list of doctors with their details:
        {
            "status": "success",
            "data": [
                {
                    "id": int,
                    "name": str,
                    "specialties": str
                },
                ...
            ]
        }
    """
    return fetch_all_doctors()


@api.route('/symptoms/match', methods=['POST'])
def patient_symptom_match():
    """
    Receiving a a patient's symptoms and matching them with the doctor that best suits their needs.

    Expected JSON format:
    {
        "symptoms": str  # Symptoms the patient is facing
    }

    Returns:
    {
        "status": "success",
        "data": {
            "doctor_id": int,      # Unique identifier of the matched doctor
            "doctor_name": str,     # Full name of the matched doctor
            "doctor_specialties": str # Doctor's areas of specialization
        }
    }

    TODO: Implement sophisticated symptom-to-doctor matching algorithm based on specialties
    """
    
    # Brute force implementation - returns the first doctor
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            raise BadRequest("Invalid JSON payload")

        required_field = 'symptoms'
        if not required_field in data:
            raise BadRequest("Missing required field")
        
        # Get the first doctor from the database
        doctor = Doctor.query.first()

        if not doctor:
            return create_error_response(
                "No doctors available in the system",
                HTTPStatus.NOT_FOUND
            )
        
        return create_success_response({
            "doctor_id": doctor.id,
            "doctor_name": doctor.name,
            "doctor_specialties": doctor.specialties
        }, HTTPStatus.OK)
    
    except BadRequest as e:
        return create_error_response(
            str(e), 
            HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        return create_error_response(
            "Internal server error",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )