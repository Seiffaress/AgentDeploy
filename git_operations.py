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

from github import Github
import logging
from datetime import datetime

class GithubIssueManager:
    def __init__(self, github_token):
        self.github = Github(github_token)
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging to file and console"""
        log_filename = f"agent_actions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_bug_issues(self, repo_name):
        """Get all open issues labeled as 'bug'"""
        try:
            repo = self.github.get_repo(repo_name)
            return repo.get_issues(state='open', labels=['bug'])
        except Exception as e:
            self.logger.error(f"Error fetching bug issues: {str(e)}")
            return []

    def mark_issue_as_resolved(self, issue):
        """Change issue label from 'bug' to 'resolved'"""
        try:
            issue.remove_from_labels('bug')
            issue.add_to_labels('resolved')
            self.logger.info(f"Issue #{issue.number} marked as resolved")
        except Exception as e:
            self.logger.error(f"Error updating issue labels: {str(e)}")