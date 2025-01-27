import pytest
from flask import Flask, json
from app import create_app
from app.database import db
from app.models import Doctor, Slot
from http import HTTPStatus
from datetime import datetime

@pytest.fixture
def client():
    app = create_app('Test')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_add_slot(client):
    # Test adding a slot
    doctor = Doctor(ssn='918234', name='Dr. Smith', specialties='Cardiology', experience=10, opd_rate=500.0)
    db.session.add(doctor)
    db.session.commit()

    response = client.post('/api/dev/post/slot', json={  
        "doctor_id": doctor.id,
        "start_time": "2023-10-01T09:00:00",
        "end_time": "2023-10-01T10:00:00",
        "slot_type": "appointment"
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['status'] == 'success'

    # Test adding a slot with invalid time
    response = client.post('/api/dev/post/slot', json={  
        "doctor_id": doctor.id,
        "start_time": "2023-10-01T10:00:00",
        "end_time": "2023-10-01T09:00:00"
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "End time must be after start time" in response.json['response']

def test_get_slots(client):
    # Test getting slots when none exist
    response = client.get('/api/dev/get/slots')  
    assert response.status_code == 200
    assert response.json['response'] == []

    # Add a slot and test again
    doctor = Doctor(ssn='823754', name='Dr. Smith', specialties='Cardiology', experience=10, opd_rate=500.0)
    db.session.add(doctor)
    db.session.commit()

    start_time = datetime.fromisoformat("2023-10-01T09:00:00")
    end_time = datetime.fromisoformat("2023-10-01T10:00:00")
    slot = Slot(doctor_id=doctor.id, start_time=start_time, end_time=end_time, slot_type="appointment")
    db.session.add(slot)
    db.session.commit()

    response = client.get('/api/dev/get/slots')  
    assert response.status_code == 200
    assert len(response.json['response']) == 1
