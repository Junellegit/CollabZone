from flask_socketio import Namespace, emit, join_room
from models import db, Task

class KanbanNamespace(Namespace):
    def on_join(self, data):
        join_room(data["project_id"])

    def on_move_task(self, data):
        task = Task.query.get(data["task_id"])
        if task:
            task.status = data["status"]
            db.session.commit()
            emit("task_moved", data, room=data["project_id"])

kanban_ns = KanbanNamespace("/kanban")