#!/usr/bin/env python
"""
Reset the database by dropping all tables and recreating them
"""
import os
from pathlib import Path
from app import create_app
from models import db

def reset_database():
    """Drop all tables and recreate them"""
    
    # Option 1: Delete the SQLite file
    db_path = Path('school_pm.sqlite')
    if db_path.exists():
        print(f"Suppression de l'ancienne base de données: {db_path}")
        os.remove(db_path)
        print("✓ Ancienne base de données supprimée")
    
    # Option 2: Drop and recreate tables
    app = create_app()
    with app.app_context():
        print("Création du nouveau schéma de base de données...")
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables with new schema
        print("✓ Schéma de base de données créé avec succès")
        
        # Verify the schema
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        print("\nTables de la base de données:")
        for table_name in inspector.get_table_names():
            print(f"  - {table_name}")
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(f"    • {column['name']} ({column['type']})")

if __name__ == "__main__":
    print("=== Outil de réinitialisation de base de données ===\n")
    
    response = input("Ceci va SUPPRIMER toutes les données existantes. Continuer? (oui/non): ")
    if response.lower() in ['oui', 'yes', 'o', 'y']:
        reset_database()
        print("\n✓ Réinitialisation de la base de données terminée!")
        print("Vous pouvez maintenant exécuter 'python create-test-data.py' pour ajouter des données de test.")
    else:
        print("Opération annulée.")