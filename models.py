import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def generate_uuid():
    """Retourne un identifiant unique de 32 caractères (hex)."""
    return uuid.uuid4().hex


class User(UserMixin, db.Model):
    id = db.Column(db.String(32), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Pseudo/nickname
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), nullable=False, default="etudiant")  # prof, etudiant, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Helpers password
    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class Project(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.String(32), db.ForeignKey("user.id"))
    owner = db.relationship("User", backref="owned_projects")
    tasks = db.relationship("Task", backref="project", lazy=True)
    messages = db.relationship("Message", backref="project", lazy=True)
    files = db.relationship("File", backref="project", lazy=True)


class Task(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="todo")  # todo, doing, done
    project_id = db.Column(db.String(32), db.ForeignKey("project.id"))
    assignee_id = db.Column(db.String(32), db.ForeignKey("user.id"))
    assignee = db.relationship("User", backref="assigned_tasks")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.String(32), db.ForeignKey("project.id"))
    author_id = db.Column(db.String(32), db.ForeignKey("user.id"))
    author = db.relationship("User", backref="messages")


class File(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=generate_uuid)
    filename = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.String(32), db.ForeignKey("project.id"))