from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
from sqlalchemy import desc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vraie_cle_secrete_a_remplacer'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

socketio = SocketIO(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MODELES
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='assigned_to', lazy=True)
    contributions = db.relationship('Contribution', backref='member', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')
    assigned_member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    contribution_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.String(100))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATION BDD + DEMO
with app.app_context():
    db.create_all()
    if not User.query.first():
        # Démo : 2 users, membres, tâches
        user1 = User(username="john", email="john@example.com")
        user1.set_password("password")
        user2 = User(username="jane", email="jane@example.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()
        member1 = Member(name="John Doe", email="john@example.com", role="Développeur", user_id=user1.id)
        member2 = Member(name="Jane Smith", email="jane@example.com", role="Designer", user_id=user2.id)
        db.session.add_all([member1, member2])
        db.session.commit()
        task1 = Task(title="Conception de l'interface", description="Créer le design de l'application", status="todo", assigned_member_id=member2.id)
        task2 = Task(title="Développement backend", description="Fonctionnalités serveur", status="in_progress", assigned_member_id=member1.id)
        db.session.add_all([task1, task2])
        db.session.commit()

# ROUTES WEB
@app.route('/')
@login_required
def home():
    member = Member.query.filter_by(user_id=current_user.id).first()
    member_id = member.id if member else None
    return render_template('index.html', member_id=member_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Email ou mot de passe invalide', 'error')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email déjà utilisé', 'error')
            return render_template('signup.html', form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash('Nom d\'utilisateur déjà utilisé', 'error')
            return render_template('signup.html', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#API FEED
@app.route('/api/feed')
@login_required
def feed():
    # Récupère les 10 derniers fichiers et messages, ordonnés par date décroissante
    files = File.query.order_by(desc(File.upload_date)).limit(10).all()
    messages = Message.query.order_by(desc(Message.created_at)).limit(10).all()
    events = []
    for f in files:
        events.append({
            "type": "file",
            "date": f.upload_date.isoformat(),
            "user": f.uploaded_by,
            "filename": f.filename
        })
    for m in messages:
        user = User.query.get(m.sender_id)
        events.append({
            "type": "message",
            "date": m.created_at.isoformat(),
            "user": user.username if user else "Anonyme",
            "content": m.content
        })
    # Tri par date décroissante
    events.sort(key=lambda e: e["date"], reverse=True)
    # On limite à 15 actus (ajuste si tu veux)
    return jsonify(events[:15])

# API TACHES
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    member = Member.query.filter_by(user_id=current_user.id).first()
    tasks = Task.query.filter_by(assigned_member_id=member.id).all() if member else []
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'created_at': task.created_at.isoformat(),
        'assigned_member': {'name': task.assigned_to.name if task.assigned_to else None}
    } for task in tasks])

@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    new_task = Task(
        title=data.get('title'),
        description=data.get('description', ''),
        status='todo',
        assigned_member_id=member.id
    )
    db.session.add(new_task)
    db.session.commit()
    socketio.emit('task_added', {
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'status': new_task.status,
        'assigned_member': {'name': member.name}
    })
    return jsonify({'message': 'Task created successfully', 'id': new_task.id}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    db.session.commit()
    socketio.emit('task_updated', {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status
    })
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_deleted', {'id': task_id})
    return jsonify({'message': 'Task deleted successfully'})

# API CHAT
@app.route('/api/messages', methods=['GET'])
@login_required
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    result = [{
        'id': msg.id,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'sender': {'name': User.query.get(msg.sender_id).username}
    } for msg in messages]
    return jsonify(result)

@app.route('/api/user')
@login_required
def api_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

@app.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    msg = Message(sender_id=current_user.id, content=data.get('content'))
    db.session.add(msg)
    db.session.commit()
    socketio.emit('new_message', {
        'id': msg.id,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'sender': {'name': current_user.username}
    })
    return jsonify({'message': 'Message envoyé'})

# API FICHIERS
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier reçu.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné.'}), 400
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        uploaded_by = current_user.username
        db.session.add(File(filename=filename, uploaded_by=uploaded_by))
        db.session.commit()
        return jsonify({'message': 'Fichier uploadé avec succès', 'filename': filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files', methods=['GET'])
@login_required
def list_files():
    files = File.query.order_by(File.upload_date.desc()).all()
    return jsonify([
        {'filename': f.filename, 'uploaded_by': f.uploaded_by, 'upload_date': f.upload_date.isoformat()}
        for f in files
    ])

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API DASHBOARD/CONTRIBUTIONS
@app.route('/api/dashboard/data')
@login_required
def dashboard_data():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        return jsonify({
            'todo': 0,
            'in_progress': 0,
            'done': 0
        })
    return jsonify({
        'todo': Task.query.filter_by(assigned_member_id=member.id, status='todo').count(),
        'in_progress': Task.query.filter_by(assigned_member_id=member.id, status='in_progress').count(),
        'done': Task.query.filter_by(assigned_member_id=member.id, status='done').count()
    })

@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_profile():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        return jsonify({'error': 'Profil non trouvé'}), 404
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'name': member.name,
        'role': member.role
    })

@app.route('/api/user/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    user = User.query.get(current_user.id)
    member = Member.query.filter_by(user_id=current_user.id).first()
    
    if not member:
        return jsonify({'error': 'Profil non trouvé'}), 404
        
    # Mise à jour des champs de l'utilisateur
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    # Mise à jour des champs du membre
    if 'name' in data:
        member.name = data['name']
    if 'role' in data:
        member.role = data['role']
    
    db.session.commit()
    return jsonify({
        'message': 'Profil mis à jour avec succès',
        'user': {
            'username': user.username,
            'email': user.email,
            'name': member.name,
            'role': member.role
        }
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
