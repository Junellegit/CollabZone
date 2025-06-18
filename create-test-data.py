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
            username="testuser",
            first_name="Test",
            last_name="User",
            password_hash=generate_password_hash("password123", method='pbkdf2:sha256'),
            bio="I'm a test user",
            role="etudiant"
        )
        db.session.add(test_user)
        db.session.commit()
        print("✓ Created test user (username: testuser, password: password123)")
        
        # Create test project
        test_project = Project(
            name="Test Project",
            description="This is a test project to demonstrate the Kanban board",
            owner_id=test_user.id
        )
        db.session.add(test_project)
        db.session.commit()
        print("✓ Created test project")
        
        # Create test tasks
        tasks = [
            Task(title="Design the database schema", status="done", project_id=test_project.id),
            Task(title="Implement user authentication", status="done", project_id=test_project.id),
            Task(title="Create the Kanban board", status="doing", project_id=test_project.id),
            Task(title="Add real-time updates", status="doing", project_id=test_project.id),
            Task(title="Implement file uploads", status="todo", project_id=test_project.id),
            Task(title="Add user profiles", status="todo", project_id=test_project.id),
            Task(title="Create project chat", status="todo", project_id=test_project.id),
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        print("✓ Created test tasks")
        
        print("\n=== Test data created successfully! ===")
        print("You can now login with:")
        print("Username: testuser")
        print("Password: password123")

if __name__ == "__main__":
    create_test_data()