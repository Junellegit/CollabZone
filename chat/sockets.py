from datetime import datetime
from flask_socketio import Namespace, emit, join_room
from models import db, Message

class ChatNamespace(Namespace):
    def on_join(self, data):
        join_room(data["project_id"])

    def on_send_message(self, data):
        msg = Message(text=data["text"],
                      project_id=data["project_id"],
                      author_id=data["author_id"])
        db.session.add(msg)
        db.session.commit()
        data["timestamp"] = datetime.utcnow().isoformat()
        emit("receive_message", data, room=data["project_id"])

chat_ns = ChatNamespace("/chat")