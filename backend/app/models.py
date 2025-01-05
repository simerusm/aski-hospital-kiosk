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
    ssn = db.Column(db.String(12), nullable=False, unique=True)
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
    - ssn: (STRING) SSN of the doctor
    - name: (STRING) Name of the doctor
    - specialties: (STRING) Key specialties of the doctor given in csv format
    - experience: (INT) Years of experience
    - opd_rate: (FLOAT) Consultation fee
    - is_available: (BOOL) Availability status
    - phone: (STRING) Phone number of doctor
    - profile_picture: (STRING) Path to doctor's profile picture

    Backref Attributes:
    - queue: (DB.MODEL) Backwards reference defined in Queue model
    '''

    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(12), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    specialties = db.Column(db.String(255), nullable=False)  # e.g., "Cardiology, General Medicine"
    experience = db.Column(db.Integer, nullable=False)  # Years of experience
    opd_rate = db.Column(db.Float, nullable=False)  # Consultation fee
    is_available = db.Column(db.Boolean, default=True)  # Availability status
    phone = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)  # URL or path to profile pic

    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialties}>"
    

class Queue(db.Model):
    """
    Queue model for managing doctor-patient queues.

    Attributes:
    - id: (INT) Primary key ID of the queue
    - doctor_id: (INT) Foreign key referencing the associated doctor
    - total_patients: (INT) Number of patients currently in the queue
    - estimated_wait_time: (STRING) Total estimated wait time for the queue
    """
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False, unique=True)
    total_patients = db.Column(db.Integer, default=0)
    estimated_wait_time = db.Column(db.String(50), nullable=True)

    # Establish relationship with Doctor, adding backwards reference in Doctors model (adding queue attribute)
    doctor = db.relationship('Doctor', backref=db.backref('queue', uselist=False))

    def __repr__(self):
        return f"<Queue for Doctor ID {self.doctor_id} - {self.total_patients} Patients>"
    

class QueueEntry(db.Model):
    """
    QueueEntry model for individual patients in a doctor's queue.

    Attributes:
    - id: (INT) Primary key ID of the queue entry
    - queue_id: (INT) Foreign key referencing the associated queue
    - patient_id: (INT) Foreign key referencing the patient
    - position: (INT) Position of the patient in the queue
    - status: (STRING) Status of the patient in the queue (e.g., "waiting", "in_consultation")
    """
    id = db.Column(db.Integer, primary_key=True)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="waiting")

    # Establish relationships
    queue = db.relationship('Queue', backref=db.backref('entries', lazy=True))
    patient = db.relationship('User', backref=db.backref('queue_entries', lazy=True))

    def __repr__(self):
        return f"<QueueEntry Patient ID {self.patient_id} in Queue {self.queue_id}>"

class Slot(db.Model):
    """
    Slot model for managing doctor's appointment slots.

    Attributes:
    - id: (INT) Primary key ID of the slot
    - doctor_id: (INT) Foreign key referencing the doctor
    - start_time: (DATETIME) Start time of the slot
    - end_time: (DATETIME) End time of the slot
    - is_available: (BOOL) Whether the slot is available
    - patient_id: (INT) Foreign key referencing the patient (null if unbooked)
    - slot_type: (STRING) Either 'walk_in' or 'appointment'
    """
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    slot_type = db.Column(db.String(20), default='appointment')

    # Relationships
    doctor = db.relationship('Doctor', backref=db.backref('slots', lazy=True))
    patient = db.relationship('User', backref=db.backref('appointments', lazy=True))


