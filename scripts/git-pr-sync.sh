#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/git-pr-sync.sh [branch]
# Ensures a branch is up to date with origin/main, ready for conflict resolution.

branch="${1:-$(git symbolic-ref --quiet --short HEAD)}"
if [[ -z "${branch}" ]]; then
  echo "Unable to determine branch. Pass a branch name as the first argument." >&2
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

main_branch="main"

echo "==> Fetching from origin"
git fetch origin

echo "==> Checking out ${branch}"
git checkout "$branch"

echo "==> Merging ${main_branch} into ${branch}"
git merge "origin/${main_branch}"

echo "==> Status summary"
git status -sb
