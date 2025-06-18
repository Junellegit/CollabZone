import os
from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO

import config
from models import db, Task, Message, Membership, User

# Instanciation de SocketIO au niveau module
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialisation des extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Callback nécessaire pour Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialisation de SocketIO
    socketio.init_app(app)

    # Enregistrement des blueprints
    from auth.routes       import auth_bp
    from chat               import chat_bp
    from projects.routes   import projects_bp
    from tasks.routes      import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def root():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        status_filter = request.args.get('status', 'all')
        project_ids = [m.project_id for m in current_user.memberships]

        # Filtrage des tâches par projet et statut
        query = Task.query.filter(Task.project_id.in_(project_ids))
        if status_filter in ['todo', 'in-progress', 'done']:
            query = query.filter_by(status=status_filter)
        tasks = query.order_by(Task.created_at.desc()).all()

        messages = Message.query.order_by(Message.timestamp.desc()).all()
        return render_template(
            'index.html',
            tasks=tasks,
            messages=messages,
            status_filter=status_filter
        )

    return app

if __name__ == '__main__':
    # Création de l'app puis lancement avec socketio
    app = create_app()
    socketio.run(app, debug=True)
