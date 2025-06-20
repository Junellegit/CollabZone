from flask import Blueprint

projects_bp = Blueprint(
    'projects',
    __name__,
    template_folder='templates',
    url_prefix='/projects'
)

from . import routes
