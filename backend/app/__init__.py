from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.routes import patient_routes, queue_routes, dev_routes, slot_routes
from app.database import db

_app_instance = None  # Singleton instance

def create_app(config_name: str = None):
    global _app_instance
    if _app_instance is None:
        _app_instance = Flask(__name__)

        if config_name == 'Test':
            print('test')
            _app_instance.config.from_object('config.Test')
        else:
            print('dev')
            _app_instance.config.from_object('config.Dev')

        # Blueprint app registrations
        _app_instance.register_blueprint(patient_routes.api, url_prefix='/api/patients')
        _app_instance.register_blueprint(slot_routes.api, url_prefix='/api/slots')
        _app_instance.register_blueprint(dev_routes.api, url_prefix='/api/dev')
        _app_instance.register_blueprint(queue_routes.api, url_prefix='/api/queue')

        db.init_app(_app_instance)
        CORS(_app_instance)
    return _app_instance