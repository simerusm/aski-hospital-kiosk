from flask import Flask
from app.routes.patient_routes import api as patient_routes_api
from app import db, create_app  # Import the create_app function

DEVELOPMENT_ENV = True

app = create_app()  # Create the app instance

app.register_blueprint(patient_routes_api, url_prefix='/api/patients')
#app.register_blueprint(queue_routes.api, url_prefix='/api/queue')
#app.register_blueprint(slot_routes.api, url_prefix='/api/slots')

with app.app_context():
    db.create_all()  # Create database tables

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)  # Run the app