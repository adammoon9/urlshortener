import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///urls.db')