from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash
)
from flask_login import (
    login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    url_prefix='/auth'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # … votre code existant pour la connexion …
    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # … votre code existant pour l’inscription …
    return render_template('signup.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnecté avec succès.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile/avatar', methods=['POST'])
@login_required
def upload_avatar():
    file = request.files.get('avatar')
    if not file:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('profile'))
    # … logique de sauvegarde de l’avatar (ex. file.save(…) ) …
    flash('Avatar mis à jour.', 'success')
    return redirect(url_for('profile'))
