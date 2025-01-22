import pytest
from flask import Flask, json
from app import create_app
from app.database import db
from app.models import User, Doctor, Slot, Queue, QueueEntry
from http import HTTPStatus

@pytest.fixture
def client():
    app = create_app('Test')  # Use the create_app function to create the app instance
    app.config['TESTING'] = True
    with app.app_context():  # Ensure the app context is active
        db.create_all()  # Create the database tables
        with app.test_client() as client:
            yield client
        db.drop_all()  # Clean up after tests

def test_view_queue(client):
    # Test viewing queue for a doctor when none exists
    response = client.get('/api/queue/status/10')  
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Add a doctor and a queue
    doctor = Doctor(ssn='123456', name='Dr. Smith', specialties='Cardiology', experience=10, opd_rate=500.0)
    db.session.add(doctor)
    db.session.commit()

    queue = Queue(doctor_id=doctor.id, total_patients=0)
    db.session.add(queue)
    db.session.commit()

    response = client.get(f'/api/queue/status/{doctor.id}')  
    assert response.status_code == HTTPStatus.OK
    assert response.json['response']['total_patients'] == 0

    # Add a user to the queue
    user = User(ssn='718234', name='John Doe', phone='555-123-9128')
    db.session.add(user)
    db.session.commit()

    # Call upon /api/queue routes to join the queue
    response = client.post('/api/queue/join', json={
        "doctor_id": doctor.id,
        "patient_id": user.id
    })
    assert response.status_code == HTTPStatus.CREATED

    # Check the queue status
    response = client.get(f'/api/queue/status/{doctor.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json['response']['total_patients'] == 1

    # Ensure duplicates can't be added
    response = client.post('/api/queue/join', json={
        "doctor_id": doctor.id,
        "patient_id": user.id
    })
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json['response'] == "Patient already in queue"