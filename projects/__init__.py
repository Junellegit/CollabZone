from flask import Blueprint
from .sockets import kanban_ns

projects_bp = Blueprint('projects', __name__, template_folder='templates')

from . import routes, sockets

# Make kanban_ns available when importing from projects package
__all__ = ['projects_bp', 'kanban_ns']
