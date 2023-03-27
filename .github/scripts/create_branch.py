import argparse
import requests
from requests.exceptions import HTTPError


def get_owner_and_repo(full_repo_name: str) -> (str, str):
    owner, repo = full_repo_name.split("/")
    owner = owner.strip("/")
    repo = repo.strip("/")
    return owner, repo


parser = argparse.ArgumentParser(description="test")

parser.add_argument("--repo", help="GitHub full repository name (including the owner)", type=str)
parser.add_argument("--gh-token", help="GitHub token to call the REST API", type=str)
parser.add_argument("--sha", help="Commit sha used to create the branch", type=str)
parser.add_argument("--tag", help="Name of the tag to use, must be of the form 'vx.y.z'", type=str)

args = parser.parse_args()

owner, repo = get_owner_and_repo(args.repo)
url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
target_branch_name = f"test-dev/{args.tag}"

# owner = "Flooorent"
# repo = "tests-workflow"
# gh_token = "TODO"
# commit sha of release/v0.0.10
# sha = "ed776f17e289cbec69b2a41defad35816dd70608"

headers = {
  "Accept": "application/vnd.github+json",
  "Authorization": f"Bearer {args.gh_token}",
  "X-GitHub-Api-Version": "2022-11-28",
}

req = requests.post(
    url,
    headers=headers,
    json={
        "ref": f"refs/heads/{target_branch_name}",
        "sha": args.sha
    }
)

try:
  req.raise_for_status()
except HTTPError as e:
  print(e.response.text)
  raise e

print(req.json())
