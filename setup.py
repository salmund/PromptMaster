"""
Script de configuration et d'installation pour PromptMaster.
Lance l'installation des dépendances et initialise la base de données.
"""

import subprocess
import sys
import os


def check_python_version():
    """Vérifie que la version de Python est compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou supérieur est requis")
        print(f"   Votre version : Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} détecté")
    return True


def install_dependencies():
    """Installe les dépendances depuis requirements.txt."""
    print("\n📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation des dépendances")
        return False


def initialize_database():
    """Initialise la base de données avec des exemples."""
    print("\n🗄️ Initialisation de la base de données...")
    try:
        from database import DatabaseManager, populate_sample_data
        
        db = DatabaseManager()
        
        # Vérifier si la base est vide
        all_prompts = db.get_all_prompts()
        if len(all_prompts) == 0:
            print("   Ajout de prompts d'exemple...")
            populate_sample_data()
        else:
            print(f"   Base de données déjà initialisée ({len(all_prompts)} prompts)")
        
        print("✓ Base de données prête")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base : {e}")
        return False


def test_imports():
    """Teste que tous les modules peuvent être importés."""
    print("\n🧪 Vérification des imports...")
    
    modules = [
        ("PySide6.QtWidgets", "PySide6"),
        ("pynput.keyboard", "pynput"),
        ("sqlite3", "sqlite3 (intégré)")
    ]
    
    all_ok = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"   ✓ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} - Installation requise")
            all_ok = False
    
    return all_ok


def create_startup_script():
    """Crée un script batch pour démarrer facilement l'application."""
    print("\n📝 Création du script de démarrage...")
    
    batch_content = f"""@echo off
echo Demarrage de PromptMaster...
cd /d "{os.getcwd()}"

REM Activer l'environnement virtuel si présent
if exist venv\\Scripts\\activate.bat (
    call venv\\Scripts\\activate.bat
)

REM Lancer l'application
python main.py

pause
"""
    
    try:
        with open("start_promptmaster.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        print("✓ Script 'start_promptmaster.bat' créé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du script : {e}")
        return False


def main():
    """Point d'entrée du script de setup."""
    print("="*60)
    print("🎯 Configuration de PromptMaster")
    print("="*60)
    
    # Étape 1 : Vérifier Python
    if not check_python_version():
        sys.exit(1)
    
    # Étape 2 : Installer les dépendances
    if not install_dependencies():
        sys.exit(1)
    
    # Étape 3 : Tester les imports
    if not test_imports():
        print("\n⚠️ Certains modules ne sont pas disponibles.")
        print("   Exécutez : pip install -r requirements.txt")
        sys.exit(1)
    
    # Étape 4 : Initialiser la base
    initialize_database()
    
    # Étape 5 : Créer le script de démarrage
    create_startup_script()
    
    # Résumé
    print("\n" + "="*60)
    print("✅ Configuration terminée avec succès !")
    print("="*60)
    print("\n📚 Prochaines étapes :")
    print("   1. Lancez l'application : python main.py")
    print("   2. Ou utilisez : start_promptmaster.bat")
    print("   3. Appuyez sur Ctrl + Space pour afficher l'interface")
    print("\n📖 Documentation complète dans README.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
