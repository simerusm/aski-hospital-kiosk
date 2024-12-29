from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
_app_instance = None  # Singleton instance

def create_app():
    global _app_instance
    if _app_instance is None:
        _app_instance = Flask(__name__)
        _app_instance.config.from_object('config.Test')
        db.init_app(_app_instance)
        CORS(_app_instance)
    return _app_instance