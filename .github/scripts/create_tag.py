"""
Example call:
python create_branch.py \
--repo Flooorent/tests-workflow \
--gh-token TOKEN \
--sha ed776f17e289cbec69b2a41defad35816dd70608 \
--tag v0.0.13
"""
import argparse
import requests
from requests.exceptions import HTTPError


def get_owner_and_repo(full_repo_name: str) -> (str, str):
    owner, repo = full_repo_name.split("/")
    owner = owner.strip("/")
    repo = repo.strip("/")
    return owner, repo


def check_if_is_release_branch(branch_name: str) -> bool:
    return branch_name.startswith("release/v")


def check_if_is_hotfix_branch(branch_name: str) -> bool:
    return branch_name.startswith("hotfix/v")


def get_tag_from_release(release: str) -> str:
    prefix = "release/"
    assert release.startswith(f"{prefix}v"), f"A release should be of the form '{prefix}vx.y.z'."
    return release.strip(prefix)


def get_tag_from_hotfix(hotfix: str) -> str:
    prefix = "hotfix/"
    assert hotfix.startswith(f"{prefix}v"), f"A hotfix should be of the form '{prefix}vx.y.z'."
    return hotfix.strip(prefix)


def get_tag_version(branch_name: str) -> str:
    is_release_branch = check_if_is_release_branch(branch_name)
    is_hotfix_branch = check_if_is_hotfix_branch(branch_name)

    assert is_release_branch or is_hotfix_branch, f"branch_name {branch_name} should be a release or a hotfix branch."

    tag_version = ""

    if is_release_branch:
        tag_version = get_tag_from_release(branch_name)

    if is_hotfix_branch:
        tag_version = get_tag_from_hotfix(branch_name)

    return tag_version


parser = argparse.ArgumentParser(description="test")

parser.add_argument("--repo", help="GitHub full repository name (including the owner)", type=str)
parser.add_argument("--gh-token", help="GitHub token to call the REST API", type=str)
parser.add_argument("--sha", help="Commit sha used to create the branch", type=str)
parser.add_argument(
    "--head-branch",
    help="Name of the head branch to use, must be of the form 'release/v*' or 'hotfix/v*'.",
    type=str,
)

args = parser.parse_args()

is_release_branch = check_if_is_release_branch(args.head_branch)
is_hotfix_branch = check_if_is_hotfix_branch(args.head_branch)

if not (is_release_branch or is_hotfix_branch):
    raise ValueError(f"Head branch {args.head_branch} must be a release or a hotfix branch.")


owner, repo = get_owner_and_repo(args.repo)
url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"

tag_version = get_tag_version(args.head_branch)
target_branch_name = f"test-dev/{tag_version}"


headers = {
  "Accept": "application/vnd.github+json",
  "Authorization": f"Bearer {args.gh_token}",
  "X-GitHub-Api-Version": "2022-11-28",
}

req = requests.post(
  url,
  headers=headers,
  json={
    "ref": f"refs/tags/{target_branch_name}",
    "sha": args.sha,
  }
)

try:
  req.raise_for_status()
except HTTPError as e:
  print(e.response.text)
  raise e

print(req.json())
