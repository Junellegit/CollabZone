from flask import Blueprint

proj_bp = Blueprint("projects", __name__, template_folder="templates")
from . import routes, sockets  # noqa
kanban_ns = sockets.kanban_ns  # réexporte le namespace pour app.py