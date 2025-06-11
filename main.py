from code_correction import verifier_et_corriger
from git_operations import GitManager
from dotenv import load_dotenv
from fastapi import FastAPI
import os
import platform

# Chargement des variables d'environnement
load_dotenv()

# Configuration
REPO_URL = "https://github.com/Seiffaress/Agent"
# Détection de l'environnement
if platform.system() == "Windows":
    LOCAL_PATH = "C:\\Users\\timos\\Desktop\\Clone"
else:
    LOCAL_PATH = "/app/Clone"  # Pour Render

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

app = FastAPI()

@app.get("/run-agent")
def run_agent():
    try:
        # Initialisation du gestionnaire Git
        git_manager = GitManager(REPO_URL, LOCAL_PATH, GITHUB_TOKEN)

        # Clone et pull du repository
        git_manager.clone_repository()
        git_manager.pull_changes()

        # Vérification existence fichier test
        test_file_path = os.path.join(LOCAL_PATH, "test_sample.py")
        if not os.path.exists(test_file_path):
            return {"status": "error", "message": "❌ Le fichier test_sample.py n'existe pas dans le dépôt Git"}

        print("Lancement de la vérification du code...")
        verifier_et_corriger()

        # Commit et push des modifications avec chemin relatif au LOCAL_PATH
        git_manager.commit_and_push(
            os.path.join(LOCAL_PATH, "exemple_corrige.py"),
            "fix: Correction automatique du code"
        )

        return {"status": "success", "message": "Vérification terminée et changements poussés."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Pour le développement local
if __name__ == "__main__":
    # Initialisation du gestionnaire Git
    git_manager = GitManager(REPO_URL, LOCAL_PATH, GITHUB_TOKEN)
    
    # Clone et pull du repository
    git_manager.clone_repository()
    git_manager.pull_changes()
    
    # Vérifier si le fichier test_sample.py existe dans le dépôt
    if not os.path.exists(os.path.join(LOCAL_PATH, "test_sample.py")):
        print("❌ Le fichier test_sample.py n'existe pas dans le dépôt Git")
    else:
        print("Lancement de la vérification du code...")
        verifier_et_corriger()
        
        # Commit et push des modifications
        git_manager.commit_and_push(
            os.path.join(LOCAL_PATH, "exemple_corrige.py"),
            "fix: Correction automatique du code"
        )
        print("Vérification terminée et changements poussés.")