import os
import time
import subprocess
from github import Github, GithubException, Auth

# ✅ Load GitHub credentials from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

if not GITHUB_TOKEN:
    raise Exception("❌ GITHUB_TOKEN not set in environment")
if not GITHUB_USERNAME:
    raise Exception("❌ GITHUB_USERNAME not set in environment")

# ✅ Authenticate using modern method
g = Github(auth=Auth.Token(GITHUB_TOKEN))


def create_unique_repo_name(base_name: str) -> str:
    """
    Generate a unique repo name by appending a timestamp if it already exists.
    """
    user = g.get_user()
    existing_repo_names = [repo.name for repo in user.get_repos()]

    if base_name not in existing_repo_names:
        return base_name

    timestamp = int(time.time())
    return f"{base_name}-{timestamp}"


def create_repo(repo_name: str, description: str = "", private: bool = False) -> str:
    """
    Create a new GitHub repository and return its HTTPS URL.
    """
    user = g.get_user()
    final_name = create_unique_repo_name(repo_name)

    try:
        repo = user.create_repo(
            name=final_name,
            description=description,
            private=private,
            auto_init=False
        )
        print(f"✅ Created repo: {final_name}")
        return repo.clone_url
    except GithubException as e:
        msg = e.data.get('message', str(e))
        raise Exception(f"❌ Failed to create repo: {msg}")


def push_files_to_repo(repo_name: str, folder_path: str) -> str:
    """
    Push all files from folder_path to the GitHub repo.
    Returns the last commit SHA.
    """
    user = g.get_user()
    repo = user.get_repo(repo_name)
    last_commit_sha = None

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder_path).replace("\\", "/")

            with open(file_path, "rb") as f:
                content = f.read()

            try:
                # Try creating new file
                commit = repo.create_file(
                    path=rel_path,
                    message=f"Add {rel_path}",
                    content=content
                )
                last_commit_sha = commit["commit"].sha
                print(f"📄 Added: {rel_path}")

            except GithubException:
                # If file exists, update it
                contents = repo.get_contents(rel_path)
                commit = repo.update_file(
                    path=rel_path,
                    message=f"Update {rel_path}",
                    content=content,
                    sha=contents.sha
                )
                last_commit_sha = commit["commit"].sha
                print(f"✏️ Updated: {rel_path}")

    if last_commit_sha is None:
        raise Exception("❌ No files were pushed to the repository.")

    return last_commit_sha


def push_updated_files_to_repo(repo_name: str, folder_path: str) -> str:
    """
    Push updated files for Round 2 to an existing repo.
    Returns the last commit SHA.
    """
    print(f"🔁 Pushing updated files for Round 2 to repo: {repo_name}")
    return push_files_to_repo(repo_name, folder_path)


def get_pages_url(repo_name: str) -> str:
    """
    Returns the GitHub Pages URL for a repo (username.github.io/repo).
    """
    return f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"
