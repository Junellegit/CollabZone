# CollabZone – Mini Skeleton (100 % Python)

CollabZone est une application de gestion de projets pensée pour un usage académique
(écoles, universités, bootcamps).  
Cette version « mini » se concentre sur la simplicité : **aucun Node.js, aucun
build front**, tout se pilote avec Python et un CDN Tailwind.

---

## Fonctionnalités principales

| Domaine            | Détails                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| Authentification   | Inscription (pseudo, prénom, nom, bio), connexion/déconnexion, protection Flask-Login             |
| Rôles              | *étudiant* (par défaut), extensible (*professeur*, *admin*, etc.)                                  |
| Projets            | CRUD projets, tableau **Kanban** (todo / in-progress / done)                                       |
| Temps réel         | Mise à jour Kanban + chat de projet via **Flask-SocketIO**                                         |
| Partage de fichiers| Uploads locaux (dossier *static/uploads*)                                                          |
| Stockage           | SQLite (zéro config)                                                                               |
| UI                 | Tailwind JIT CDN + quelques composants Alpine/HTMX (facultatif)                                    |

---

## Arborescence

.
├── app.py # Point d’entrée, crée l’application
├── config.py # Configuration (SECRET_KEY, DB, SocketIO mode)
├── models.py # SQLAlchemy : User, Project, Task, Message, File
├── requirements.txt
│
├── auth/ # Inscription / connexion
│ ├── init.py
│ ├── routes.py
│ └── templates/
│ ├── signup.html
│ └── login.html
│
├── projects/ # Tableau Kanban & vues projet
│ ├── init.py
│ ├── routes.py
│ └── sockets.py
│
├── chat/ # Namespace Socket.IO dédié au chat
│ ├── init.py
│ └── sockets.py
│
├── templates/ # Layout global, navbar, etc.
│ ├── base.html
│ └── navbar.html
│
└── static/
└── js/ # kanban.js, chat.js, app.js (libres à remplir)

yaml
Copier
Modifier

---

## Prérequis

* **Python ≥ 3.9**  
* *pip* & *virtualenv* (fortement recommandé)

---

## Installation rapide

```bash
# 1) Cloner le dépôt et se placer dedans
git clone https://github.com/votrecompte/CollabZone.git
cd CollabZone

# 2) Environnement virtuel
python -m venv venv
source venv/bin/activate    # Windows : venv\Scripts\activate

# 3) Dépendances Python
pip install -r requirements.txt
