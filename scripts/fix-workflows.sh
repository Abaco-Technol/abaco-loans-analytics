#!/usr/bin/env bash
set -euo pipefail

# Install a pinned version of actionlint for consistent validation
ACTIONLINT_VER="1.6.23"

echo "Installing actionlint@$ACTIONLINT_VER..."
sudo npm install -g "actionlint@${ACTIONLINT_VER}"

echo "Running actionlint on .github/workflows"
actionlint .github/workflows || exit 1

echo "All workflows pass actionlint checks."