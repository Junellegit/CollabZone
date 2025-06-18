from flask import (
    render_template, redirect, url_for,
    request, flash
)
from flask_login import login_required, current_user
from models import db, Task, Membership
from . import tasks_bp

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    # Liste des projets de l'utilisateur
    memberships = Membership.query.filter_by(user_id=current_user.id).all()
    projects = [m.project for m in memberships]

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        project_id  = int(request.form.get('project_id', 0))

        if not title:
            flash('Le titre est requis.', 'danger')
            return render_template('tasks/create.html', projects=projects)

        # Vérifie que l'utilisateur est bien membre du projet
        if not Membership.query.filter_by(
            user_id=current_user.id, project_id=project_id
        ).first():
            flash("Vous n'êtes pas membre du projet sélectionné.", 'danger')
            return redirect(url_for('tasks.create_task'))

        task = Task(
            title=title,
            description=description,
            user_id=current_user.id,
            project_id=project_id
        )
        db.session.add(task)
        db.session.commit()
        flash('Tâche créée avec succès.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('tasks/create.html', projects=projects)

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    # Vérifie que l'utilisateur est membre du projet
    if not Membership.query.filter_by(
        user_id=current_user.id, project_id=task.project_id
    ).first():
        flash("Vous n'avez pas la permission d'éditer cette tâche.", 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        task.title       = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        task.status      = request.form.get('status', task.status)
        db.session.commit()
        flash('Tâche mise à jour.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('tasks/edit.html', task=task)

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not Membership.query.filter_by(
        user_id=current_user.id, project_id=task.project_id
    ).first():
        flash("Vous n'avez pas la permission de supprimer cette tâche.", 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Tâche supprimée.', 'success')
    return redirect(url_for('dashboard'))
