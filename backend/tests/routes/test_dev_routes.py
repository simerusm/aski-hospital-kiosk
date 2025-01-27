import pytest
from flask import Flask, json
from app import create_app
from app.database import db
from app.models import User, Doctor
from http import HTTPStatus

@pytest.fixture
def client():
    app = create_app('Test')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_get_users(client):
    # Test getting users when none exist
    response = client.get('/api/dev/get/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json['response'] == []

    # Add a user and test again
    user = User(ssn='123-45-6789', name='John Doe', phone='555-1234')
    db.session.add(user)
    db.session.commit()

    response = client.get('/api/dev/get/users')
    assert response.status_code == HTTPStatus.OK

def test_add_user(client):
    # Test adding a user
    response = client.post('/api/dev/add/user', json={  
        "ssn": "123456",
        "name": "John Doe",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Test adding a duplicate user
    response = client.post('/api/dev/add/user', json={  
        "ssn": "123456",
        "name": "John Doe",
        "phone": "555-123-4567"
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "User with this SSN already exists" in response.json['response']

def test_get_doctors(client):
    # Test getting doctors when none exist
    response = client.get('/api/dev/get/doctors')  
    assert response.status_code == HTTPStatus.OK
    assert response.json['response'] == []

    # Add a doctor and test again
    doctor = Doctor(ssn='123456', name='Dr. Smith', specialties='Cardiology', experience=10, opd_rate=500.0)
    db.session.add(doctor)
    db.session.commit()

    response = client.get('/api/dev/get/doctors')  
    assert response.status_code == HTTPStatus.OK
    assert len(response.json['response']) == 1

def test_add_doctor(client):
    # Test adding a doctor
    response = client.post('/api/dev/add/doctor', json={  
        "ssn": "123456",
        "name": "Dr. Smith",
        "specialties": "Cardiology",
        "experience": 10,
        "opd_rate": 500.0
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == 'success'

    # Test adding a duplicate doctor
    response = client.post('/api/dev/add/doctor', json={  
        "ssn": "123456",
        "name": "Dr. Jones",
        "specialties": "Neurology",
        "experience": 5,
        "opd_rate": 600.0
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Doctor with this SSN already exists" in response.json['response']