from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from . import auth_bp
from models import db, User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("projects.dashboard"))
        flash("Identifiants incorrects", "error")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        bio = request.form.get('bio', '')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            bio=bio,
            role='etudiant'  # Default role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')