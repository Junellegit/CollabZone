#!/usr/bin/env python
"""
Migrate existing database to add new columns
"""
from app import create_app
from models import db
from sqlalchemy import text

def migrate_database():
    """Add missing columns to existing database"""
    app = create_app()
    
    with app.app_context():
        # Get database connection
        with db.engine.connect() as conn:
            # Check if columns already exist
            result = conn.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result]
            
            print("Current columns in user table:", columns)
            
            # Add missing columns if they don't exist
            if 'first_name' not in columns:
                print("Adding first_name column...")
                conn.execute(text("ALTER TABLE user ADD COLUMN first_name VARCHAR(80)"))
                conn.commit()
                print("✓ Added first_name column")
            
            if 'last_name' not in columns:
                print("Adding last_name column...")
                conn.execute(text("ALTER TABLE user ADD COLUMN last_name VARCHAR(80)"))
                conn.commit()
                print("✓ Added last_name column")
            
            if 'bio' not in columns:
                print("Adding bio column...")
                conn.execute(text("ALTER TABLE user ADD COLUMN bio TEXT"))
                conn.commit()
                print("✓ Added bio column")
            
            # Check if role column has default value
            if 'role' in columns:
                # Update existing rows that might have NULL role
                conn.execute(text("UPDATE user SET role = 'etudiant' WHERE role IS NULL"))
                conn.commit()
                print("✓ Updated NULL roles to 'etudiant'")
            
            print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    print("=== Database Migration Tool ===\n")
    try:
        migrate_database()
    except Exception as e:
        print(f"Error during migration: {e}")
        print("\nIf migration fails, you can reset the database with 'python reset-db.py'")