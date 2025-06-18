# config.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-en-prod')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR/'school_pm.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use eventlet for async mode to match gunicorn configuration
    SOCKETIO_ASYNC_MODE = "eventlet"