#!/usr/bin/env python3
from __future__ import annotations
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([
        "git",
        *args,
    ], cwd=ROOT, capture_output=True, text=True)


def find_conflict_markers() -> list[str]:
    result = run_git(["grep", "-n", "^<<<<<<< "])
    if result.returncode in (0, 1):
        return [] if not result.stdout else result.stdout.strip().splitlines()
    raise RuntimeError(result.stderr.strip() or "git grep failed")


def tracked_paths(paths: list[str]) -> list[str]:
    tracked: list[str] = []
    for path in paths:
        result = run_git(["ls-files", path])
        if result.returncode == 0 and result.stdout.strip():
            tracked.append(path)
    return tracked


def working_tree_changes() -> list[str]:
    result = run_git(["status", "--porcelain"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    return [] if not result.stdout else result.stdout.strip().splitlines()


def main() -> int:
    issues: list[str] = []

    markers = find_conflict_markers()
    if markers:
        issues.append("Conflict markers present:\n" + "\n".join(markers))

    secret_hits = tracked_paths([".env.local", ".vercel"])
    if secret_hits:
        issues.append("Tracked secret-bearing files detected. Please review your git tracked files and update your .gitignore if necessary.")

    changes = working_tree_changes()
    if changes:
        issues.append("Working tree not clean:\n" + "\n".join(changes))

    if issues:
        print("Conflicts detected. Fix before merging:\n")
        for item in issues:
            print(f"- {item}\n")
        return 1

    print("No conflict markers, tracked secrets, or pending changes detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
