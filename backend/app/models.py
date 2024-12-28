from app import db

class User(db.Model):
    '''
    User relation object.

    Attributes/Columns:
    - id: SSN of the patient
    - name: Name of the patient
    - phone: Phone number of the patient
    '''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Doctor(db.Model):
    '''
    Doctor relation object.

    Attributes/Columns:
    - name: Name of the doctor
    - specialties: Key specialties of the doctor given in csv format
    - experience: Years of experience
    - opd_rate: Consulation fee
    - is_available: Availability status
    - phone: Phone number of doctor
    - profile_picture: Path to doctor's profile picture
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
    

