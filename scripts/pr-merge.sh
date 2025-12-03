#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/pr-merge.sh <branch> [commit message]
# Automates checkout -> merge origin/main -> quality gates -> commit -> push guidance.
branch="${1:-}" ; commit_message="${2:-}"
if [[ -z "$branch" ]]; then
  echo "Usage: ./scripts/pr-merge.sh <branch> [commit message]" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Run this script inside a Git repository." >&2
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "Remote 'origin' is not configured. Add it before syncing." >&2
  exit 1
fi

main_branch="${MAIN_BRANCH:-main}"

echo "==> Fetching from origin"
git fetch origin

echo "==> Checking out ${branch}"
git checkout "$branch"

echo "==> Merging origin/${main_branch} into ${branch}"
set +e
git merge --no-ff "origin/${main_branch}"
merge_status=$?
set -e
if [[ $merge_status -ne 0 ]]; then
  echo "Merge reported conflicts. Resolve them, rerun ./scripts/check-web.sh, then commit and push." >&2
  git status -sb
  exit $merge_status
fi

echo "==> Running quality gates"
"$(dirname "$0")/check-web.sh"

echo "==> Staging changes"
git add .

if [[ -z "$commit_message" ]]; then
  commit_message="Sync ${branch} with ${main_branch}"
fi

echo "==> Committing: ${commit_message}"
git commit -m "$commit_message"

echo "==> Pushing to origin/${branch}"
git push origin "$branch"

echo "==> Merge when ready"
echo "Run: gh pr merge --merge --delete-branch"
