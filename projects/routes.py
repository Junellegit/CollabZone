from flask import (
    render_template, redirect, url_for,
    request, flash
)
from flask_login import login_required, current_user
from models import db, Project, Membership, User
from . import projects_bp

@projects_bp.route('/', methods=['GET'])
@login_required
def list_projects():
    memberships = Membership.query.filter_by(user_id=current_user.id).all()
    projects = [m.project for m in memberships]
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('Le nom du projet est requis.', 'danger')
            return render_template('projects/create.html')
        project = Project(
            name=name,
            description=description,
            created_by=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        # Le créateur devient propriétaire
        membership = Membership(
            user_id=current_user.id,
            project_id=project.id,
            role='owner'
        )
        db.session.add(membership)
        db.session.commit()
        flash('Projet créé.', 'success')
        return redirect(url_for('projects.manage_project', project_id=project.id))
    return render_template('projects/create.html')

@projects_bp.route('/<int:project_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_project(project_id):
    project = Project.query.get_or_404(project_id)
    membership = Membership.query.filter_by(
        project_id=project_id,
        user_id=current_user.id
    ).first()
    if not membership:
        flash("Vous n'êtes pas membre de ce projet.", 'danger')
        return redirect(url_for('dashboard'))

    # Invitation de nouveaux membres
    if request.method == 'POST' and 'invite' in request.form:
        email = request.form.get('email', '').strip()
        role  = request.form.get('role', 'member')
        user  = User.query.filter_by(email=email).first()
        if not user:
            flash("Utilisateur introuvable.", "danger")
        elif Membership.query.filter_by(
            project_id=project_id,
            user_id=user.id
        ).first():
            flash("Utilisateur déjà membre.", "warning")
        else:
            new_member = Membership(
                user_id=user.id,
                project_id=project_id,
                role=role
            )
            db.session.add(new_member)
            db.session.commit()
            flash("Membre invité.", "success")
        return redirect(url_for('projects.manage_project', project_id=project_id))

    members = Membership.query.filter_by(project_id=project_id).all()
    return render_template(
        'projects/manage.html',
        project=project,
        members=members,
        membership=membership
    )

@projects_bp.route('/<int:project_id>/remove_member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(project_id, user_id):
    owner_membership = Membership.query.filter_by(
        project_id=project_id,
        user_id=current_user.id
    ).first()
    if not owner_membership or owner_membership.role != 'owner':
        flash("Seul le propriétaire peut retirer des membres.", "danger")
        return redirect(url_for('projects.manage_project', project_id=project_id))

    member = Membership.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first_or_404()
    if member.user_id == current_user.id:
        flash("Vous ne pouvez pas vous retirer.", "warning")
    else:
        db.session.delete(member)
        db.session.commit()
        flash("Membre retiré.", "success")
    return redirect(url_for('projects.manage_project', project_id=project_id))
