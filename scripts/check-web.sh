#!/usr/bin/env bash
set -euo pipefail

# Run web app static analysis, lint, and formatting checks from repository root.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR%/scripts}"
cd "$PROJECT_ROOT/apps/web"

npm run check-all
