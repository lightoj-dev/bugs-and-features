import os
from github_client import GitHubClient
from lightoj_api import LightOJAPIClient
from typing import Optional, Dict, Any

# These are used by the ADK Agent in agent.py
def get_issue_content(issue_number: int) -> str:
    gh = GitHubClient(os.getenv("GITHUB_TOKEN"))
    issue = gh.get_issue(issue_number)
    content = f"ISSUE_BODY:\n{issue.body}\n\nCOMMENTS:\n"
    for comment in issue.get_comments():
        content += f"USER {comment.user.login}: {comment.body}\n"
    return content

def post_comment_to_issue(issue_number: int, message: str):
    gh = GitHubClient(os.getenv("GITHUB_TOKEN"))
    gh.comment_on_issue(issue_number, message)

def close_issue(issue_number: int):
    gh = GitHubClient(os.getenv("GITHUB_TOKEN"))
    gh.close_issue(issue_number)

def search_lightoj_institution(name: str) -> Optional[Dict[str, Any]]:
    loj = LightOJAPIClient(
        "https://lightoj.com/api", 
        os.getenv("LIGHTOJ_HANDLE"), 
        os.getenv("LIGHTOJ_PASSWORD")
    )
    if loj.login():
        return loj.search_institution(name)
    return None

def create_lightoj_institution(name: str, website: str, logo_url: str, country_code: str) -> Dict[str, Any]:
    loj = LightOJAPIClient(
        "https://lightoj.com/api", 
        os.getenv("LIGHTOJ_HANDLE"), 
        os.getenv("LIGHTOJ_PASSWORD")
    )
    if loj.login():
        return loj.create_institution(name, website, logo_url, country_code)
    return {"status": "error", "message": "Login failed"}
