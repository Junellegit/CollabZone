#!/usr/bin/env python
"""
Force close all database connections and processes
"""
import os
import sys
import subprocess
from pathlib import Path

def force_close_db():
    """Force close database and Python processes"""
    
    print("=== Fermeture forcée des connexions à la base de données ===\n")
    
    # On Windows, use taskkill to find and kill Python processes
    if sys.platform == "win32":
        print("Recherche des processus Python...")
        
        # Get list of Python processes
        try:
            # Find all python processes
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            python_pids = []
            
            for line in lines:
                if line and 'python.exe' in line:
                    parts = line.split(',')
                    if len(parts) > 1:
                        pid = parts[1].strip('"')
                        python_pids.append(pid)
            
            if python_pids:
                print(f"Trouvé {len(python_pids)} processus Python")
                
                # Don't kill the current process
                current_pid = str(os.getpid())
                python_pids = [pid for pid in python_pids if pid != current_pid]
                
                if python_pids:
                    response = input(f"Voulez-vous fermer {len(python_pids)} processus Python? (oui/non): ")
                    if response.lower() in ['oui', 'yes', 'o', 'y']:
                        for pid in python_pids:
                            try:
                                subprocess.run(['taskkill', '/PID', pid, '/F'], check=True)
                                print(f"✓ Processus {pid} fermé")
                            except:
                                print(f"❌ Impossible de fermer le processus {pid}")
            else:
                print("Aucun autre processus Python trouvé")
                
        except Exception as e:
            print(f"Erreur lors de la recherche des processus: {e}")
    
    # Check if database file is still locked
    db_path = Path('school_pm.sqlite')
    if db_path.exists():
        print(f"\nVérification de l'accès au fichier {db_path}...")
        try:
            # Try to open the file exclusively
            with open(db_path, 'rb+') as f:
                f.seek(0)
            print("✓ Le fichier de base de données est accessible")
        except:
            print("❌ Le fichier est toujours verrouillé")
            print("\nSolutions:")
            print("1. Fermez tous les terminaux/CMD ouverts")
            print("2. Fermez votre IDE (VSCode, PyCharm, etc.)")
            print("3. Redémarrez votre ordinateur si nécessaire")

if __name__ == "__main__":
    force_close_db()