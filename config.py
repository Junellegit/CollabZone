import os

# Chemin absolu vers le dossier du projet
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Clé secrète pour Flask (changez-la en production !)
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# URI de la base de données : on cherche d'abord la variable d'environnement DATABASE_URL,
# sinon on crée un fichier SQLite 'collabzone.db' à la racine du projet.
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(BASEDIR, 'collabzone.db')
)

# Désactive le signal de suivi des modifications, pour ne pas polluer les logs
SQLALCHEMY_TRACK_MODIFICATIONS = False

# (Optionnel) Si vous voulez que Flask-SocketIO utilise Eventlet ou Gevent,
# vous pouvez ajouter ici une config spécifique, mais ce n'est pas requis.
