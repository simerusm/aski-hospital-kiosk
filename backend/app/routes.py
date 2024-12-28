from flask import Blueprint, request, jsonify
from app.models import User

api = Blueprint('api', __name__)

@api.route('/auth/id', methods=['POST'])
def authenticate_id():
    '''
    Receiving a user's SSN id, checking if it already exists 
    '''
    data = request.json
    print('hit')
    print(data)
    return jsonify({"message": "Authenticated"}), 200