from app import db

class User(db.Model):
    '''
    User relation object.

    Attributes/Columns:
    - id: (INT) Primary key ID of the patient
    - ssn: (STRING) SSN of the patient
    - name: (STRING) Name of the patient
    - phone: (STRING) Phone number of the patient
    - checkin_status: (BOOL) Checkin status of the patient
    '''

    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(12), nullable=True, unique=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    checkin_status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Patient Object - ssn: {self.ssn}>"

class Doctor(db.Model):
    '''
    Doctor relation object.

    Attributes/Columns:
    - id: (INT) Primary key ID of the doctor
    - name: (STRING) Name of the doctor
    - specialties: (STRING) Key specialties of the doctor given in csv format
    - experience: (INT) Years of experience
    - opd_rate: (FLOAT) Consultation fee
    - is_available: (BOOL) Availability status
    - phone: (STRING) Phone number of doctor
    - profile_picture: (STRING) Path to doctor's profile picture
    '''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialties = db.Column(db.String(255), nullable=False)  # e.g., "Cardiology, General Medicine"
    experience = db.Column(db.Integer, nullable=False)  # Years of experience
    opd_rate = db.Column(db.Float, nullable=False)  # Consultation fee
    is_available = db.Column(db.Boolean, default=True)  # Availability status
    phone = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)  # URL or path to profile pic

    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialties}>"
    



