# Test GitHub workflows

- test 1: create branch after merging PR against `main`
  - changed Workflow permissions to "read and write"
  - test with already existing branch
- test 2: create tag after merging PR against `main`
  - use correct commit sha
  - specifying commit sha doesn't work, update main branch protection rule and require linear history
  - try squashing commits
- test 3: check that on_push workflow is not triggered for 'feature/something'
