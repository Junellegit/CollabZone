#!/usr/bin/env python
"""
Create test data for CollabZone
"""
from app import create_app
from models import db, User, Project, Task
from werkzeug.security import generate_password_hash

def create_test_data():
    app = create_app()
    
    with app.app_context():
        # Check if we already have data
        if User.query.first():
            print("Data already exists. Skipping...")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password_hash=generate_password_hash("password123", method='pbkdf2:sha256'),
            bio="Je suis un utilisateur de test",
            role="etudiant"
        )
        db.session.add(test_user)
        db.session.commit()
        print("✓ Created test user (email: test@example.com, password: password123)")
        
        # Create test project
        test_project = Project(
            name="Projet de Test",
            description="Ceci est un projet de test pour démontrer le tableau Kanban",
            owner_id=test_user.id
        )
        db.session.add(test_project)
        db.session.commit()
        print("✓ Created test project")
        
        # Create another project
        demo_project = Project(
            name="Projet Demo CollabZone",
            description="Un projet de démonstration avec plusieurs tâches et fonctionnalités",
            owner_id=test_user.id
        )
        db.session.add(demo_project)
        db.session.commit()
        print("✓ Created demo project")
        
        # Create test tasks for first project
        tasks = [
            Task(title="Concevoir le schéma de base de données", status="done", project_id=test_project.id),
            Task(title="Implémenter l'authentification", status="done", project_id=test_project.id),
            Task(title="Créer le tableau Kanban", status="doing", project_id=test_project.id),
            Task(title="Ajouter les mises à jour en temps réel", status="doing", project_id=test_project.id),
            Task(title="Implémenter l'upload de fichiers", status="todo", project_id=test_project.id),
            Task(title="Ajouter les profils utilisateurs", status="todo", project_id=test_project.id),
            Task(title="Créer le chat de projet", status="todo", project_id=test_project.id),
        ]
        
        # Create tasks for demo project
        demo_tasks = [
            Task(title="Analyse des besoins", status="done", project_id=demo_project.id),
            Task(title="Design de l'interface", status="done", project_id=demo_project.id),
            Task(title="Développement du backend", status="doing", project_id=demo_project.id),
            Task(title="Tests unitaires", status="todo", project_id=demo_project.id),
            Task(title="Documentation", status="todo", project_id=demo_project.id),
        ]
        
        for task in tasks + demo_tasks:
            db.session.add(task)
        
        db.session.commit()
        print("✓ Created test tasks")
        
        print("\n=== Données de test créées avec succès! ===")
        print("Vous pouvez maintenant vous connecter avec:")
        print("Email: test@example.com")
        print("Mot de passe: password123")

if __name__ == "__main__":
    create_test_data()