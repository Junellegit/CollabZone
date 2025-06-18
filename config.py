# config.py
from pathlib import Path
BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = "change-me-en-prod"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR/'school_pm.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_ASYNC_MODE = "threading"  # 100 % Python, pas dʼeventlet