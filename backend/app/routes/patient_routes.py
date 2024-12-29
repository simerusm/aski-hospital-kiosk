from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app import db
from typing import *
from app.utils import query_builder, parse_phone_number

api = Blueprint('api', __name__)
    
@api.route('/auth', methods=['POST'])
def authenticate_patient():
    """
    Receiving a a patient's information and verifying if they exist in the system.

    Expected JSON format:
    {
        "ssn": "string",   # Social Security Number of the patient
        "phone": "string"  # Phone number of the patient for 2FA
    }

    TODO: New patient registration is not handled in the kiosk just yet.
    """

    data = request.json

    query = query_builder(data, "all", "ssn")

    # Error handling to make sure there's only one
    if len(query) > 1:
        return jsonify({"error": "Multiple users found with the same SSN"}), 500 # Server error
    elif len(query) == 0:
        # TODO: Redirect to registration
        return jsonify({"error": "User not registered"}), 400
    
    user = query[0]

    # Phone number validation, ensuring phone number is in the proper format
    phone = parse_phone_number(data['phone'])

    # Ensuring remaining data is consistent
    if phone != user.phone:
        return jsonify({"error": "Incorrect phone number associated with ssn"}), 400

    return jsonify({"message": "Authenticated"}), 200


@api.route('/checkin', methods=['POST'])
def checkin():
    """
    Checkin method to update the checkin status of the user.
    """

    data = request.json

    query = query_builder(data, "all", "ssn")

    # Error handling to make sure there's only one
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