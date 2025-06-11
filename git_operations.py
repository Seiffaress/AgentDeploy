from git import Repo
import os
from urllib.parse import urlparse, urlunparse

class GitManager:
    def __init__(self, repo_url, local_path, github_token):
        self.repo_url = repo_url
        self.local_path = local_path
        self.github_token = github_token
        self.repo = None

    def get_authenticated_url(self):
        """Create authenticated URL with token"""
        parsed = urlparse(self.repo_url)
        netloc = f'{self.github_token}@{parsed.netloc}'
        return urlunparse(parsed._replace(netloc=netloc))

    def clone_repository(self):
        """Clone le dépôt distant avec authentification"""
        auth_url = self.get_authenticated_url()
        
        if not os.path.exists(self.local_path):
            print(f"Clonage du dépôt {self.repo_url}...")
            self.repo = Repo.clone_from(auth_url, self.local_path)
        else:
            self.repo = Repo(self.local_path)

    def pull_changes(self):
        """Pull les derniers changements"""
        print("Pull des changements...")
        origin = self.repo.remotes.origin
        origin.pull()

    def commit_and_push(self, file_path, commit_message):
        """Commit et push les changements"""
        print("Commit et push des changements...")
        # S'assurer que nous sommes dans le répertoire du dépôt
        os.chdir(self.local_path)
        self.repo.index.add(file_path)
        self.repo.index.commit(commit_message)
        origin = self.repo.remotes.origin
        origin.push()