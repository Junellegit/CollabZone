from flask import render_template
from flask_login import login_required
from . import projects_bp
from models import Project, Task

@projects_bp.route("/")
@login_required
def dashboard():
    projects = Project.query.all()
    return render_template("projects/dashboard.html", projects=projects)


@projects_bp.route("/<string:project_id>/kanban")
@login_required
def kanban(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template("projects/kanban.html", project=project, tasks=tasks)