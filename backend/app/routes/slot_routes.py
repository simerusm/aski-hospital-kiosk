from flask import Blueprint, request
from datetime import datetime, timedelta, timezone
from app.models import Slot, Doctor, User
from app.database import db
from app.utils.utils import create_error_response, create_success_response
from http import HTTPStatus
from app.utils.jwt_utils import token_required

api = Blueprint('slot_api', __name__)

@api.route('/available/<int:doctor_id>', methods=['GET'])
@token_required
def get_available_slots(doctor_id: int):
    """
    Get all available slots for a doctor for the next 7 days

    Return JSON Payload:
    {
        "id": int,
        "start_time": isoformat str datetime,
        "end_time": isoformat str datetime
    }
    """

    try:
        start_date = datetime.now(timezone.utc)
        end_date = start_date + timedelta(days=7)

        available_slots = Slot.query.filter(
            Slot.doctor_id == doctor_id,
            Slot.is_available == True,
            Slot.start_time.between(start_date, end_date)
        ).order_by(Slot.start_time).all()

        slots_data = [{
            "id": slot.id,
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
            "is_available": slot.is_available,
            "doctor_id": slot.doctor_id
        } for slot in available_slots]

        return create_success_response(
            slots_data, 
            HTTPStatus.OK
        )

    except Exception as e:
        return create_error_response(
            str(e), 
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

@api.route('/book', methods=['POST'])
@token_required
def book_slot():
    """
    Book a specific slot for a patient
    
    Expected JSON payload:
    {
        "slot_id": int,
        "patient_id": int
    }
    """
    try:
        data = request.get_json()
        
        # Verify that the authenticated user is booking for themselves
        if str(data['patient_id']) != str(request.user['user_id']):
            return create_error_response(
                "Unauthorized to book for another patient",
                HTTPStatus.FORBIDDEN
            )
            
        slot = Slot.query.filter_by(id=data['slot_id']).first()
        if not slot:
            return create_error_response("Slot not found", HTTPStatus.NOT_FOUND)
        
        if not slot.is_available:
            return create_error_response(
                "Slot is no longer available",
                HTTPStatus.CONFLICT
            )

        slot.is_available = False
        slot.patient_id = data['patient_id']
        db.session.commit()

        return create_success_response({
            "appointment_time": slot.start_time.isoformat(),
            "doctor_id": slot.doctor_id
        }, HTTPStatus.OK)

    except Exception as e:
        return create_error_response(
            str(e), 
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
    

@api.route('/delete/slot/<int:slot_id>', methods=['DELETE'])
def delete_slot(slot_id):
    """
    Delete a slot from the database by its ID.

    Args:
        slot_id (int): The ID of the slot to be deleted.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        print(slot_id)
        # Find the slot by ID
        slot = Slot.query.filter_by(id=slot_id).first()
        if not slot:
            return create_error_response("Slot not found", HTTPStatus.NOT_FOUND)

        # Delete the slot
        db.session.delete(slot)
        db.session.commit()

        return create_success_response(
            "Slot deleted successfully",
            HTTPStatus.OK
        )

    except Exception as e:
        return create_error_response(
            str(e),
            HTTPStatus.INTERNAL_SERVER_ERROR
        )