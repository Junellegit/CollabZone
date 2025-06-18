from flask import Blueprint

# Blueprint pour la partie HTTP (affichage du chat)
chat_bp = Blueprint(
    'chat',
    __name__,
    template_folder='templates',
    url_prefix='/chat'
)

# On importe les handlers WebSocket (namespace) juste après
from . import sockets
