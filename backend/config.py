class Prod:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Test:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dummy.db'  # Use a test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Dev:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'  # Use a development database
    SQLALCHEMY_TRACK_MODIFICATIONS = False