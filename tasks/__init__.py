from flask import Blueprint

tasks_bp = Blueprint(
    'tasks',
    __name__,
    template_folder='templates',
    url_prefix='/tasks'
)

from . import routes
