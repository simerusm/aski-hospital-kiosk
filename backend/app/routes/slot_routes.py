from flask import Blueprint, request
from datetime import datetime, timedelta
from app.models import Slot, Doctor, User
from app import db
from app.utils import create_error_response, create_success_response
from http import HTTPStatus

api = Blueprint('slot_api', __name__)

@api.route('/available/<int:doctor_id>', methods=['GET'])
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
        start_date = datetime.now()
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
        slot = Slot.query.get_or_404(data['slot_id'])
        
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

# @api.route('/mode', methods=['POST'])
# def select_mode():
#     """
#     Choose between walk-in queue or scheduled appointment
    
#     Expected JSON payload:
#     {
#         "mode": str,  # Either "walk_in" or "appointment"
#         "patient_id": int,
#         "doctor_id": int
#     }
#     """
#     try:
#         data = request.get_json()
#         mode = data['mode']
        
#         if mode == "walk_in":
#             # Use existing queue system
#             # Redirect to queue/join endpoint
#             return create_success_response({
#                 "redirect": f"/api/queue/join",
#                 "method": "POST",
#                 "data": {
#                     "doctor_id": data['doctor_id'],
#                     "patient_id": data['patient_id']
#                 }
#             }, HTTPStatus.OK)
            
#         elif mode == "appointment":
#             # Redirect to slot selection
#             return create_success_response({
#                 "redirect": f"/api/slots/available/{data['doctor_id']}",
#                 "method": "GET"
#             }, HTTPStatus.OK)
            
#         else:
#             return create_error_response(
#                 "Invalid mode selected",
#                 HTTPStatus.BAD_REQUEST
#             )

#     except Exception as e:
#         return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
