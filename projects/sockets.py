from flask_socketio import Namespace, emit
from flask_login import current_user
from flask import render_template
from . import chat_bp

@chat_bp.route('/')
def chat_box():
    return render_template('chat_box.html')

class ChatNamespace(Namespace):
    def on_connect(self):
        print(f"{current_user.username} connecté au chat")
        emit('user_connected', {'user': current_user.username}, broadcast=True)

    def on_message(self, data):
        # on renvoie le message à tous
        emit('message', {
            'user': current_user.username,
            'msg': data['msg']
        }, broadcast=True)
