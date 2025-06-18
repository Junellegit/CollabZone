#!/usr/bin/env python
"""
Reset the database by dropping all tables and recreating them
"""
import os
import sys
import time
from pathlib import Path
from app import create_app
from models import db

def reset_database():
    """Drop all tables and recreate them"""
    
    # # Option 1: Try to delete the SQLite file
    # db_path = Path('school_pm.sqlite')
    # if db_path.exists():
    #     print(f"Tentative de suppression de l'ancienne base de données: {db_path}")
        
    #     # Try multiple times with a delay
    #     for attempt in range(3):
    #         try:
    #             os.remove(db_path)
    #             print("Ancienne base de données supprimée")
    #             break
    #         except PermissionError:
    #             if attempt < 2:
    #                 print(f"La base de données est utilisée. Tentative {attempt + 1}/3...")
    #                 print("   Assurez-vous d'avoir arrêté l'application Flask (Ctrl+C)")
    #                 time.sleep(2)
    #             else:
    #                 print("\nImpossible de supprimer la base de données.")
    #                 print("   Solutions possibles:")
    #                 print("   1. Arrêtez l'application Flask si elle tourne encore (Ctrl+C)")
    #                 print("   2. Fermez tous les terminaux/IDE qui pourraient accéder au fichier")
    #                 print("   3. Redémarrez votre IDE ou terminal")
    #                 print("\n   Alternative: renommer le fichier manuellement")
                    
    #                 # Try to rename instead
    #                 try:
    #                     backup_name = f'school_pm_backup_{int(time.time())}.sqlite'
    #                     os.rename(db_path, backup_name)
    #                     print(f"\nBase de données renommée en: {backup_name}")
    #                 except:
    #                     print("\nImpossible de renommer la base de données non plus.")
    #                     print("   Veuillez fermer tous les programmes et réessayer.")
    #                     return False
    
    # Create new database
    print("\nCréation du nouveau schéma de base de données...")
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables first (if database exists)
            db.drop_all()
            # Create all tables with new schema
            db.create_all()
            print("Schéma de base de données créé avec succès")
            
            # Verify the schema
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            print("\nTables de la base de données:")
            for table_name in inspector.get_table_names():
                print(f"  - {table_name}")
                columns = inspector.get_columns(table_name)
                for column in columns:
                    print(f"    • {column['name']} ({column['type']})")
            
            return True
            
        except Exception as e:
            print(f"\nErreur lors de la création de la base de données: {e}")
            return False

def check_processes():
    """Check if Flask app is running"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'app.py' in cmdline or 'run-dev.py' in cmdline:
                    print(f"Processus Flask détecté (PID: {proc.info['pid']})")
                    return True
    except:
        # psutil not installed, skip check
        pass
    return False

if __name__ == "__main__":
    print("=== Outil de réinitialisation de base de données ===\n")
    
    # Check if Flask is running
    if check_processes():
        print("Il semble que l'application Flask soit encore en cours d'exécution.")
        print("   Veuillez l'arrêter avec Ctrl+C avant de continuer.\n")
    
    # Check for non-interactive flag
    force_run = '-y' in sys.argv or '--yes' in sys.argv

    if force_run:
        response = 'oui'
    else:
        response = input("Ceci va SUPPRIMER toutes les données existantes. Continuer? (oui/non): ")

    if response.lower() in ['oui', 'yes', 'o', 'y']:
        if reset_database():
            print("\nRéinitialisation de la base de données terminée!")
            print("Vous pouvez maintenant exécuter 'python create-test-data.py' pour ajouter des données de test.")
        else:
            print("\nLa réinitialisation a échoué. Veuillez suivre les instructions ci-dessus.")
            sys.exit(1)
    else:
        print("Opération annulée.")