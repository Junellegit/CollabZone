import os
from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import projects_bp
from models import db, Project, Task, User

# Routes configuration
projects_bp.url_prefix = '/projects'

@projects_bp.route("/")
@login_required
def dashboard():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    return render_template("dashboard.html", projects=projects)

@projects_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@projects_bp.route('/profile/avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Crée un nom de fichier unique pour éviter les conflits
        unique_filename = f"{current_user.id}_{filename}"
        
        # Créer le dossier uploads s'il n'existe pas
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        # Met à jour l'URL de l'avatar dans la base de données
        current_user.avatar_url = f'/static/uploads/avatars/{unique_filename}'
        db.session.commit()

        return jsonify({'success': True, 'avatar_url': current_user.avatar_url})

    return jsonify({'success': False, 'error': 'File type not allowed'}), 400


@projects_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    data = request.get_json()
    
    try:
        # Update user information
        if 'bio' in data:
            current_user.bio = data['bio']
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        if 'last_name' in data:
            current_user.last_name = data['last_name']
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profil mis à jour avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@projects_bp.route("/create", methods=["POST"])
@login_required
def create_project():
    """Create a new project via AJAX"""
    name = request.form.get("name")
    description = request.form.get("description", "")
    
    if not name:
        return jsonify({"success": False, "error": "Le nom du projet est requis"}), 400
    
    try:
        project = Project(
            name=name,
            description=description,
            owner_id=current_user.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Projet '{name}' créé avec succès!",
            "redirect": url_for("projects.kanban", project_id=project.id)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@projects_bp.route("/<string:project_id>/kanban")
@login_required
def kanban(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template("kanban.html", project=project, tasks=tasks)


@projects_bp.route("/<string:project_id>/tasks", methods=["POST"])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    priority = data.get("priority", "normal")
    
    if not title:
        return jsonify({"success": False, "error": "Le titre est requis"}), 400
    
    task = Task(
        title=title,
        status="todo",
        project_id=project_id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
    })