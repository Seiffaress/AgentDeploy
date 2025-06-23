import time
from code_correction import verifier_et_corriger
from git_operations import GitManager, GithubIssueManager
from dotenv import load_dotenv
import os
import platform

load_dotenv()

REPO_URL = "https://github.com/Seiffaress/Agent"
LOCAL_PATH = "/app/Clone"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

git_manager = GitManager(REPO_URL, LOCAL_PATH, GITHUB_TOKEN)
issue_manager = GithubIssueManager(GITHUB_TOKEN)

def run_agent():
    try:
        git_manager.clone_repository()
        git_manager.pull_changes()

        test_file_path = os.path.join(LOCAL_PATH, "test_sample.py")
        if not os.path.exists(test_file_path):
            print("❌ Le fichier test_sample.py n'existe pas")
            return

        bug_issues = list(issue_manager.get_bug_issues("Seiffaress/Agent"))
        if not bug_issues:
            print("🚫 Aucun bug à traiter")
            return

        selected_issue = bug_issues[0]
        bug_description = selected_issue.body
        verifier_et_corriger(bug_description)

        git_manager.commit_and_push(
            os.path.join(LOCAL_PATH, "exemple_corrige.py"),
            "fix: Correction automatique"
        )
        issue_manager.mark_issue_as_resolved(selected_issue)

        print("✅ Correction terminée")

    except Exception as e:
        print(f"Erreur : {e}")

# boucle infinie
while True:
    run_agent()
    time.sleep(300)  # 5 minutes d’attente
