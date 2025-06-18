from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates")
from . import routes  # noqa: E402  (import tardif pour éviter les boucles)