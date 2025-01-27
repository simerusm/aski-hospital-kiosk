import pytest
from flask import Flask, json
from app import create_app
from app.database import db
from app.models import User, Doctor, Slot, Queue, QueueEntry
from http import HTTPStatus
from app.utils.jwt_utils import generate_token

@pytest.fixture
def client():
    app = create_app('Test')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_view_queue(client):
    # Create a user first for authentication
    auth_user = User(ssn='987654', name='Auth User', phone='555-987-6543')
    db.session.add(auth_user)
    db.session.commit()

    # Generate JWT token for authentication
    token = generate_token(auth_user.id, auth_user.ssn)
    headers = {'Authorization': f'Bearer {token}'}

    # Test viewing queue for a doctor when none exists
    response = client.get('/api/queue/status/10', headers=headers)  
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Add a doctor and a queue
    doctor = Doctor(ssn='123456', name='Dr. Smith', specialties='Cardiology', experience=10, opd_rate=500.0)
    db.session.add(doctor)
    db.session.commit()

    queue = Queue(doctor_id=doctor.id, total_patients=0)
    db.session.add(queue)
    db.session.commit()

    response = client.get(f'/api/queue/status/{doctor.id}', headers=headers)  
    assert response.status_code == HTTPStatus.OK
    assert response.json['response']['total_patients'] == 0

    # Add a user to the queue
    user = User(ssn='718234', name='John Doe', phone='555-123-9128')
    db.session.add(user)
    db.session.commit()

    # Call upon /api/queue routes to join the queue
    response = client.post('/api/queue/join', 
        headers=headers,
        json={
            "doctor_id": doctor.id,
            "patient_id": user.id
        })
    assert response.status_code == HTTPStatus.CREATED

    # Check the queue status
    response = client.get(f'/api/queue/status/{doctor.id}', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json['response']['total_patients'] == 1

    # Ensure duplicates can't be added
    response = client.post('/api/queue/join', 
        headers=headers,
        json={
            "doctor_id": doctor.id,
            "patient_id": user.id
        })
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json['response'] == "Patient already in queue"