from flask import Flask
from flask_cors import CORS
from app import create_app
from app.database import db

DEVELOPMENT_ENV = True

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)