from code_correction import verifier_et_corriger
from git_operations import GitManager
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Configuration
REPO_URL = "https://github.com/Seiffaress/Agent"
LOCAL_PATH = "C:\\Users\\timos\\Desktop\\Clone"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def main():
   # Initialisation du gestionnaire Git avec le token
    git_manager = GitManager(REPO_URL, LOCAL_PATH, GITHUB_TOKEN)
    
    # Clone et pull du repository
    git_manager.clone_repository()
    git_manager.pull_changes()
    
    # Vérifier si le fichier test_sample.py existe dans le dépôt
    if not os.path.exists(os.path.join(LOCAL_PATH, "test_sample.py")):
        print("❌ Le fichier test_sample.py n'existe pas dans le dépôt Git")
        return
    
    print("Lancement de la vérification du code...")
    verifier_et_corriger()
    
    # Commit et push des modifications
    git_manager.commit_and_push(
        "exemple_corrige.py",
        "fix: Correction automatique du code"
    )
    
    print("Vérification terminée et changements poussés.")

if __name__ == "__main__":
    main()