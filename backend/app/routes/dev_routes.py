from flask import Blueprint, request, jsonify, current_app
from app.models import User, Doctor, Queue, QueueEntry, Slot
from app import db
from typing import *
from app.utils import create_error_response, create_success_response, fetch_all_doctors, validate_phone_number
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from datetime import datetime

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
                        "id": int,
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
            "id": user.id,
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


@api.route('/view/<int:doctor_id>', methods=['GET'])
def view_queue(doctor_id: int):
    """View the current queue for a specific doctor"""
    try:
        queue = Queue.query.filter_by(doctor_id=doctor_id).first()
        if not queue:
            return create_error_response(
                "Queue not found for this doctor",
                HTTPStatus.NOT_FOUND
            )

        entries = QueueEntry.query.filter_by(
            queue_id=queue.id,
            status="waiting"
        ).order_by(QueueEntry.position).all()

        queue_data = {
            "total_patients": queue.total_patients,
            "current_queue": [{
                "position": entry.position,
                "patient_id": entry.patient_id,
                "status": entry.status
            } for entry in entries]
        }

        return create_success_response(queue_data, HTTPStatus.OK)

    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    

@api.route('/next-status/<int:doctor_id>', methods=['GET'])
def next_patient_status(doctor_id):
    """Get the status of the next patient in the queue"""
    try:
        queue = Queue.query.filter_by(doctor_id=doctor_id).first()
        if not queue:
            return create_error_response(
                "Queue not found for this doctor",
                HTTPStatus.NOT_FOUND
            )

        next_patient = QueueEntry.query.filter_by(
            queue_id=queue.id,
            status="waiting"
        ).order_by(QueueEntry.position).first()

        if not next_patient:
            return create_error_response(
                "No patients in queue",
                HTTPStatus.NOT_FOUND
            )

        return create_success_response({
            "next_patient_id": next_patient.patient_id,
            "position": next_patient.position
        }, HTTPStatus.OK)

    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    

@api.route('/post/slot', methods=['POST'])
def add_slot():
    """
    Endpoint to add a slot to the database.

    Expected JSON format:
    {
        "doctor_id": int,
        "start_time": str,  # ISO format datetime string "YYYY-MM-DDTHH:MM:SS"
        "end_time": str,    # ISO format datetime string "YYYY-MM-DDTHH:MM:SS"
        "slot_type": str    # Optional: "appointment" or "walk_in", defaults to "appointment"
    }

    Returns:
    {
        "status": "success",
        "response": {
            "slot_id": int,
            "doctor_id": int,
            "start_time": str,
            "end_time": str,
            "slot_type": str
        }
    }
    """

    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            raise BadRequest("Invalid JSON payload")
        
        required_fields = ['doctor_id', 'start_time', 'end_time']
        if not all(field in data for field in required_fields):
            raise BadRequest("Missing required fields")

        # Verify doctor exists
        doctor = Doctor.query.get_or_404(data['doctor_id'])

        # Parse datetime strings
        try:
            start_time = datetime.fromisoformat(data['start_time'])
            end_time = datetime.fromisoformat(data['end_time'])
        except ValueError:
            raise BadRequest("Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        
        if end_time <= start_time:
            raise BadRequest("End time must be after start time")
        
        # Create new slot
        new_slot = Slot(
            doctor_id=data['doctor_id'],
            start_time=start_time,
            end_time=end_time,
            slot_type=data.get('slot_type', 'appointment')
        )

        db.session.add(new_slot)
        db.session.commit()

        return create_success_response({
            "slot_id": new_slot.id,
            "doctor_id": new_slot.doctor_id,
            "start_time": new_slot.start_time.isoformat(),
            "end_time": new_slot.end_time.isoformat(),
            "slot_type": new_slot.slot_type
        }, HTTPStatus.CREATED)
    
    except BadRequest as e:
        return create_error_response(str(e), HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route('/get/slots', methods=['GET'])
def get_slots():
    """
    Get all the slots in the database.
    """
    try:
        slots = Slot.query.all()

        if not slots:
            return create_error_response(
                "No users available in the system",
                HTTPStatus.NOT_FOUND
            )
        
        slots_data = [{
            "slot_id": slot.id,
            "doctor_id": slot.doctor_id,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "slot_type": slot.slot_type
        } for slot in slots]

        return create_success_response(
            slots_data,
            HTTPStatus.OK
        )

    except BadRequest as e:
        return create_error_response(
            str(e),
            HTTPStatus.BAD_REQUEST
        )
