from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config
from models import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Blueprints
    from auth import auth_bp
    from projects import proj_bp, kanban_ns
    from chat import chat_ns

    app.register_blueprint(auth_bp)
    app.register_blueprint(proj_bp)
    socketio.on_namespace(kanban_ns)
    socketio.on_namespace(chat_ns)

    @app.route("/")
    def index():
        return "Welcome to CollabZone"

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(user_id)

    return app


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)


if __name__ == "__main__":
    main()