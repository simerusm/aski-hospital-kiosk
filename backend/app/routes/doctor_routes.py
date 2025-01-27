from flask import request, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth
from flask_jwt_extended import jwt_required
from flask_api import status
from backend.models import Doctor, db
from backend.utils import create_success_response, create_error_response
from http import HTTPStatus

api = Resource()
auth = HTTPTokenAuth()

@api.route('/availability/<int:doctor_id>', methods=['PUT'])
def update_availability(doctor_id):
    """
    Update doctor's availability status
    
    Expected JSON payload:
    {
        "is_available": bool
    }
    """
    try:
        data = request.get_json()

        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return create_error_response("Doctor not found", HTTPStatus.NOT_FOUND)
        doctor.is_available = data['is_available']
        db.session.commit()
        
        return create_success_response({
            "doctor_id": doctor_id,
            "is_available": doctor.is_available
        }, status.HTTP_200_OK)
    except Exception as e:
        return create_error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR) 