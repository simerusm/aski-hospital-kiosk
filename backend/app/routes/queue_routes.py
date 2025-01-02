from flask import Blueprint, request, jsonify
from app.models import User, Doctor, Queue, QueueEntry
from app import db
from app.utils import create_error_response, create_success_response
from http import HTTPStatus
from werkzeug.exceptions import BadRequest

api = Blueprint('queue_api', __name__)

@api.route('/join', methods=['POST'])
def join_queue():
    """
    Add a patient to a specific doctor's queue.
    
    Expected JSON payload:
    {
        "doctor_id": int,
        "patient_id": int
    }
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["doctor_id", "patient_id"]):
            raise BadRequest("Missing required fields")

        # Verify doctor and patient exist
        doctor = Doctor.query.get_or_404(data['doctor_id'])
        patient = User.query.get_or_404(data['patient_id'])

        queue = Queue.query.filter_by(doctor_id=doctor.id).first()
        if not queue:
            queue = Queue(doctor_id=doctor.id)
            db.session.add(queue)
            db.session.flush()

        existing_entry = QueueEntry.query.filter_by(
            queue_id=queue.id,
            patient_id=patient.id,
            status="waiting"
        ).first()
        if existing_entry:
            return create_error_response(
                "Patient already in queue",
                HTTPStatus.CONFLICT
            )

        position = queue.total_patients + 1
        new_entry = QueueEntry(
            queue_id=queue.id,
            patient_id=patient.id,
            position=position,
            status="waiting"
        )
        
        queue.total_patients += 1
        queue.estimated_wait_time = f"{position * 15} minutes"

        db.session.add(new_entry)
        db.session.commit()

        return create_success_response({
            "position": position,
            "estimated_wait": queue.estimated_wait_time
        }, HTTPStatus.CREATED)

    except BadRequest as e:
        return create_error_response(str(e), HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@api.route('/status/<int:doctor_id>', methods=['GET'])
def get_queue_status(doctor_id):
    """
    Get the current status of a doctor's queue.

    Returns:
        JSON response containing:
        {
            "total_patients": int,          # Total number of patients in the queue
            "estimated_wait_time": str,     # Estimated wait time for the queue
            "current_queue": [               # List of patients currently in the queue
                {
                    "position": int,        # Position of the patient in the queue
                    "patient_id": int,     # ID of the patient
                    "status": str          # Status of the patient in the queue
                },
                ...
            ]
        }
    """

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
            "estimated_wait_time": queue.estimated_wait_time,
            "current_queue": [{
                "position": entry.position,
                "patient_id": entry.patient_id,
                "status": entry.status
            } for entry in entries]
        }

        return create_success_response(queue_data, HTTPStatus.OK)

    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route('/next/<int:doctor_id>', methods=['GET'])
def process_next_patient(doctor_id):
    """
    Move to the next patient in the queue.

    Returns:
        JSON response containing:
        {
            "patient_id": int,              # ID of the patient being processed
            "remaining_patients": int        # Number of patients remaining in the queue
        }
    """

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

        db.session.delete(next_patient)
        queue.total_patients -= 1

        remaining_patients = QueueEntry.query.filter_by(
            queue_id=queue.id,
            status="waiting"
        ).all()
        
        for patient in remaining_patients:
            patient.position -= 1

        if queue.total_patients > 0:
            queue.estimated_wait_time = f"{queue.total_patients * 15} minutes"
        else:
            queue.estimated_wait_time = "0 minutes"

        db.session.commit()

        return create_success_response({
            "patient_id": next_patient.patient_id,
            "remaining_patients": queue.total_patients
        }, HTTPStatus.OK)

    except Exception as e:
        return create_error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
