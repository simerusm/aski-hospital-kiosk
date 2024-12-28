from flask import Flask
from app.routes import api
from app import db  # Import the db instance in __init__

DEVELOPMENT_ENV = True

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Test')  # Load configuration
    db.init_app(app)  # Initialize the database with the app
    app.register_blueprint(api, url_prefix='/api')  # Register API routes

    with app.app_context():
        db.create_all()  # Create database tables

    return app

app = create_app()  # Create the app instance

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)  # Run the app