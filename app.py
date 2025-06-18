from flask import Flask, render_template
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config
from models import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, async_mode=app.config.get('SOCKETIO_ASYNC_MODE', 'threading'))

    # Blueprints
    from auth import auth_bp
    from projects import projects_bp, kanban_ns
    from chat import chat_bp, chat_ns

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(chat_bp)
    
    # Register socket namespaces
    socketio.on_namespace(kanban_ns)
    socketio.on_namespace(chat_ns)

    @app.route("/")
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('projects.dashboard'))
        return redirect(url_for('auth.login'))

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(user_id)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "Internal Server Error: " + str(error), 500

    return app


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    # Run with socketio
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()