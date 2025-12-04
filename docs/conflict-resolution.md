# Conflict resolution playbook

Use this playbook when a feature branch diverges from `origin/main` and requires manual conflict resolution.

## Prerequisites
- Local repository cloned with access to `origin/main`.
- Working tree clean before merging (`git status` shows no pending changes).

## Steps
1. Fetch the latest references and ensure `origin/main` is up to date:
   ```bash
   git fetch origin main
   ```
2. Check out the feature branch and merge `origin/main`:
   ```bash
   git checkout <feature-branch>
   git merge origin/main
   ```
3. Resolve conflicts shown by Git in your editor; remove all `<<<<<<<`, `=======`, and `>>>>>>>` markers.
4. Verify the merge with quality checks:
   ```bash
   npm run lint
   npm run build
   npm test
   ```
   (Replace with service-specific commands where applicable.)
5. Commit the resolved merge:
   ```bash
   git add .
   git commit -m "chore: resolve merge conflicts"
   ```
6. Push the branch and complete the PR with a merge and branch deletion:
   ```bash
   git push origin <feature-branch>
   gh pr merge --merge --delete-branch
   ```

Keep the branch history clean by avoiding force pushes unless a secret was committed and needs a rewrite.
