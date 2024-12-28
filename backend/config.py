class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Use a test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Test:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dummy.db'  # Use a test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False