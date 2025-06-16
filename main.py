from code_correction import verifier_et_corriger
from git_operations import GitManager
from dotenv import load_dotenv
from fastapi import FastAPI
import os
import platform
from git_operations import GithubIssueManager

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
        #Gestion des issues Github
        issue_manager = GithubIssueManager(GITHUB_TOKEN)
        bug_issues = list(issue_manager.get_bug_issues("Seiffaress/Agent"))
        if not bug_issues:
         return {"status": "no_issues", "message": "🚫 Aucun bug trouvé dans les issues."}
         exit(0) 
        else:

            # Prendre la première issue par exemple
            selected_issue = bug_issues[0]
            bug_description = selected_issue.body  # Le texte du bug
            verifier_et_corriger(bug_description)

            # Commit et push des modifications avec chemin relatif au LOCAL_PATH
            git_manager.commit_and_push(
                 os.path.join(LOCAL_PATH, "exemple_corrige.py"),
                "fix: Correction automatique du code"
                )
            issue_manager.mark_issue_as_resolved(selected_issue)

            return {
    "status": "success",
    "operation": "Code Review & Push",
    "details": {
        "message": "✅ Vérification terminée",
        "action": "📤 Changements poussés sur GitHub"
             }
                    }

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
        #Gestion des issues Github
        issue_manager = GithubIssueManager(GITHUB_TOKEN)
        bug_issues = list(issue_manager.get_bug_issues("Seiffaress/Agent"))

        if not bug_issues:
            print("🚫 Aucun bug trouvé dans les issues.")
            exit(0) 
        else:
         # Prendre la première issue par exemple
            selected_issue = bug_issues[0]
            bug_description = selected_issue.body  # Le texte du bug
            verifier_et_corriger(bug_description)

            # Commit et push des modifications
            git_manager.commit_and_push(
            os.path.join(LOCAL_PATH, "exemple_corrige.py"),
            "fix: Correction automatique du code"
                )
            print("✅ Vérification terminée et changements poussés.")
            issue_manager.mark_issue_as_resolved(selected_issue)

        
        
      