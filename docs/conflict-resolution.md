# Pull Request Conflict Resolution Playbook

This playbook standardizes how to clear merge conflicts in Abaco Loans Analytics so PRs merge cleanly and auditably.

## Prerequisites
- Local Docker Desktop running if Supabase services are involved.
- GitHub CLI (`gh`) authenticated with rights to fetch, push, and merge.
- Working tree clean before starting.

## Step-by-step workflow
1. **Sync main**
   ```bash
   git fetch origin main
   ```
2. **Checkout the target PR branch**
   ```bash
   gh pr checkout <pr_number>
   ```
3. **Merge latest main into the branch**
   ```bash
   git merge origin/main
   ```
4. **Resolve conflicts**
   - Fix files manually.
   - Run `npm run lint` at repo root for JS/TS areas; run package-specific checks where applicable.
   - Re-run builds or tests for touched packages (e.g., `npm run build` in `apps/web`).
5. **Commit the resolution**
   ```bash
   git add .
   git commit -m "chore: resolve merge conflicts"
   ```
6. **Preflight before pushing**
   ```bash
   python scripts/conflict_guard.py
   ```
   - Confirms no conflict markers, tracked secrets (`.env.local`, `.vercel`), or uncommitted changes remain.
7. **Push and merge**
   ```bash
   git push
   gh pr merge <pr_number> --merge --delete-branch
   ```

## Verification checklist
- No `<<<<<<<`/`>>>>>>>` markers remain.
- `git status` shows a clean tree after commit.
- Secret-bearing files (`.env.local`, `.vercel`) stay untracked.
- CI/quality gates (lint, type checks, sonar) are re-run where relevant.
