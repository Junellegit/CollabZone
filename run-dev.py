#!/usr/bin/env python
"""
Development runner for CollabZone
Creates necessary directories and runs the app
"""
import os
import sys
from pathlib import Path

def setup_environment():
    """Setup the development environment"""
    
    # Create necessary directories
    dirs_to_create = [
        'static/uploads',
        'instance'  # For SQLite database
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")
    
    # Check if database exists
    db_path = Path('school_pm.sqlite')
    if not db_path.exists():
        print("✓ Database will be created on first run")
    else:
        print(f"✓ Database exists: {db_path}")

def run_app():
    """Run the application"""
    try:
        from app import main
        print("\n=== Starting CollabZone ===")
        print("Access the application at: http://localhost:5000")
        print("Press CTRL+C to quit\n")
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError running app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("=== CollabZone Development Setup ===\n")
    setup_environment()
    run_app()