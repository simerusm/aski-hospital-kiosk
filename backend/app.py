from flask import Flask
from flask_cors import CORS
from app.routes import patient_routes, queue_routes, dev_routes, slot_routes
from app import db, create_app  # Import the create_app function

DEVELOPMENT_ENV = True

app = create_app()  # Create the app instance

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(patient_routes.api, url_prefix='/api/patients')
app.register_blueprint(queue_routes.api, url_prefix='/api/queue')
app.register_blueprint(dev_routes.api, url_prefix='/api/dev')
app.register_blueprint(slot_routes.api, url_prefix='/api/slots')

with app.app_context():
    db.create_all()  # Create database tables

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)  # Run the app