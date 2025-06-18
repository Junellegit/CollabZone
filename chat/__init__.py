from flask import Blueprint
from .sockets import chat_ns

chat_bp = Blueprint('chat', __name__, template_folder='templates')

__all__ = ['chat_bp', 'chat_ns']
