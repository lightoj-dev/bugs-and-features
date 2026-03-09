from github import Github
import os

class GitHubClient:
    def __init__(self, token: str):
        self.gh = Github(token)
        self.repo = self.gh.get_repo(os.getenv("GITHUB_REPOSITORY"))

    def get_issue(self, issue_number: int):
        return self.repo.get_issue(number=issue_number)

    def comment_on_issue(self, issue_number: int, body: str):
        issue = self.get_issue(issue_number)
        return issue.create_comment(body)

    def close_issue(self, issue_number: int):
        issue = self.get_issue(issue_number)
        issue.edit(state="closed")

    def label_issue(self, issue_number: int, label: str):
        issue = self.get_issue(issue_number)
        issue.add_to_labels(label)
