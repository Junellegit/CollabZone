#!/usr/bin/env python
"""
Script de débogage pour tester l'application CollabZone
"""
import sys
import traceback

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        from flask import Flask
        print("✓ Flask imported")
        
        from flask_login import LoginManager
        print("✓ Flask-Login imported")
        
        from flask_socketio import SocketIO
        print("✓ Flask-SocketIO imported")
        
        from config import Config
        print("✓ Config imported")
        
        from models import db, User, Project, Task, Message, File
        print("✓ Models imported")
        
        from auth import auth_bp
        print("✓ Auth blueprint imported")
        
        from projects import proj_bp
        print("✓ Projects blueprint imported")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """Test app creation"""
    print("\nTesting app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✓ App created successfully")
        
        with app.app_context():
            from models import db
            db.create_all()
            print("✓ Database tables created")
        
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        traceback.print_exc()
        return False

def test_routes():
    """Test basic routes"""
    print("\nTesting routes...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test index
            response = client.get('/')
            print(f"✓ Index route: {response.status_code}")
            
            # Test login page
            response = client.get('/login')
            print(f"✓ Login route: {response.status_code}")
            
            # Test signup page
            response = client.get('/signup')
            print(f"✓ Signup route: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== CollabZone Debug Script ===\n")
    
    # Run tests
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_app_creation()
    all_passed &= test_routes()
    
    print("\n=== Summary ===")
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check the errors above.")
        sys.exit(1)