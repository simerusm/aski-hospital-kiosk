import pytest
from flask import Flask, json
from app import create_app
from app.database import db
from app.models import User, Doctor, Slot
from http import HTTPStatus
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = create_app('Test')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_patient_authentication(client):
    # Create a test user
    response = client.post('/api/dev/add/user', json={  
        "ssn": "918234",
        "name": "John Doe",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Test successful authentication
    response = client.post('/api/patients/auth', json={
        "ssn": "918234",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'
    assert 'token' in response.json['response']
    assert 'user' in response.json['response']
    token = response.json['response']['token']

    # Test accessing protected route without token
    response = client.get('/api/slots/available/1')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'Token is missing' in response.json['message']

    # Test accessing protected route with invalid token
    response = client.get('/api/slots/available/1', headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'Invalid token' in response.json['message']

    # Test accessing protected route with valid token
    response = client.get('/api/slots/available/1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK

def test_protected_slot_booking(client):
    # Create a test user
    response = client.post('/api/dev/add/user', json={  
        "ssn": "123456",
        "name": "John Doe",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Create test doctor
    doctor = Doctor(ssn='918274', name='Dr. Smith', specialties='General', experience=10, opd_rate=100.0)
    db.session.add(doctor)
    db.session.commit()

    # Create a test slot
    response = client.post('/api/dev/post/slot', json={  
        "doctor_id": doctor.id,
        "start_time": "2023-10-01T09:00:00",
        "end_time": "2023-10-01T10:00:00",
        "slot_type": "appointment"
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['status'] == 'success'

    # Authenticate and get token
    auth_response = client.post('/api/patients/auth', json={
        "ssn": "123456",
        "phone": "555-123-4567"
    })
    token = auth_response.json['response']['token']

    # Test booking slot with valid token but for another user
    response = client.post('/api/slots/book', 
        headers={'Authorization': f'Bearer {token}'},
        json={
            "slot_id": 1,
            "patient_id": 100  # Different user ID
        }
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "Unauthorized to book for another patient" in response.json['response']

    # Test booking slot with valid token for self
    response = client.post('/api/slots/book',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "slot_id": 1,
            "patient_id": 1
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'


def test_protected_queue_joining(client):
    # Create a test user
    response = client.post('/api/dev/add/user', json={  
        "ssn": "918234",
        "name": "John Doe",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    doctor = Doctor(ssn='918376', name='Dr. Smith', specialties='General', experience=10, opd_rate=100.0)
    db.session.add(doctor)
    db.session.commit()

    # Authenticate and get token
    auth_response = client.post('/api/patients/auth', json={
        "ssn": "918234",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    token = auth_response.json['response']['token']

    # Test an unknown patient (not registered) joining the queue
    response = client.post('/api/queue/join',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "doctor_id": doctor.id,
            "patient_id": 100  # Different user ID
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Patient not found" in response.json['response']

    # Test joining queue with valid token for self
    response = client.post('/api/queue/join',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "doctor_id": doctor.id,
            "patient_id": 1
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['status'] == 'success' 