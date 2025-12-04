# GitHub Workflow Runbook (Fintech Commercial Intelligence)

**Purpose:** Deliver predictable, auditable releases that keep the ABACO analytics platform stable while accelerating growth. This runbook aligns day-to-day engineering with the governance, KPI, and compliance expectations in this repo.

## Roles and accountability
- **Delivery lead:** Owns branch hygiene, PR quality, and release notes; ensures every change references a ticket/PR ID.
- **Data/KPI steward:** Validates metric definitions, lineage links, and dashboard refresh expectations before merge.
- **Security and compliance:** Confirms secrets handling, access controls, and SonarQube quality gates; flags any data-handling risk.
- **Automation/agents:** Coordinate @codex for MCP/workflow automation, @sonarqube for code health, @coderabbit for PR reviews, and @sourcery for refactor suggestions; keep their feedback in PR comments for auditability.

## Golden path: fix → verify → commit → ship
Use these command blocks as-is to keep traceability and reproducibility high.

### 1) Sync with origin and create a clean feature branch
```bash
# refresh local refs
git fetch origin

# stay aligned with the integration branch
git checkout work
git pull --rebase origin work

# start focused work
git checkout -b feature/<summary>
```

### 2) Install and hydrate toolchains
```bash
# JS/TS toolchain for the Next.js dashboard
npm install
npm --prefix apps/web install

# (Optional) Python analytics env; keep a fresh venv per feature
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Quality gates before commit
```bash
# Type safety and linting (required)
npm --prefix apps/web run type-check
npm run lint

# Format check to keep diffs clean
npm --prefix apps/web run format:check

# (Optional) Python quality — run if touching analytics code
python -m pytest tests
```

### 4) Codify the change
```bash
# stage intentionally
git status
git add <files>

# atomic, audit-friendly commit messages
git commit -m "feat: <concise change>"
```

### 5) Push, scan, and request review
```bash
# publish branch with upstream tracking
git push -u origin feature/<summary>

# SonarQube scan when available (keeps results in PR checks)
sonar-scanner -Dsonar.projectKey=abaco-loans-analytics

# notify review agents
# @coderabbit and @sourcery post suggestions automatically when enabled
```

### 6) Merge standard
```bash
# keep branch current before merge
git fetch origin && git rebase origin/work

# fast-forward via GitHub after approvals and green checks
# merge strategy: squash for crisp history unless release notes require otherwise
```

## Dashboards, KPIs, and traceability guardrails
- Update `docs/KPI-Operating-Model.md` when formulas, owners, or lineage shift.
- Ensure dashboards expose source tables, refresh timestamps, and SLA/alert owners.
- For any data export or new surface, log access expectations and on-call rotation in the PR body.

## Documentation standard
- Keep runbook links in PR descriptions for visibility.
- Prefer tables and bullet lists for executive readability; avoid long prose without structure.
- Capture verification evidence (command outputs, screenshots) in PR comments to reinforce auditability.
# GitHub Workflow Runbook

This runbook defines the golden path for contributing to the ABACO Loan Analytics Platform. It covers branch hygiene, quality gates, AI agent coordination, and merge standards to maintain traceable releases.

## Roles and responsibilities
- **Authors**: Open issues, create branches, write code, and keep documentation (including KPIs and dashboards) current.
- **Reviewers**: Enforce branching rules, verify quality gates, and request traces/links for analytics changes.
- **Release managers**: Ensure merge commits stay auditable, tags/releases capture artifacts, and rollback/forward-fix plans exist.

## Branching strategy
1. Start from `main` and create a topic branch named `feature/<ticket>` (or `fix/<ticket>`, `chore/<ticket>` for maintenance).
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/<ticket>
   ```
2. Keep branches small and focused; avoid piling unrelated changes.
3. Rebase frequently to minimize merge conflicts and keep quality signals current.
   ```bash
   git fetch origin
   git rebase origin/main
   ```
4. If the branch diverges or carries merge markers, clean them before pushing.

## Commit standards
- Write conventional commits (e.g., `feat: add risk alert thresholds`, `docs: add workflow runbook`).
- Reference the ticket/issue in the description when applicable.
- Avoid committing generated artifacts, secrets, or unresolved merge markers.

## Quality gates (required unless noted)
Run these commands locally before opening or updating a pull request:
- **Lint (JS/TS)**: `npm run lint`
- **Type-check (if TS changes)**: `npm run type-check` or `npm run lint -- --max-warnings=0`
- **Formatting**: `npm run format:check`
- **Tests**: `npm test` (or package-specific test commands)
- **Python**: `pytest` or the package’s documented test command when touching Python modules
- **SonarQube**: Ensure no new critical/major issues; review PR Sonar results and address blockers.

Optional but recommended:
- **Playwright/End-to-end**: Run targeted suites when modifying UI flows.
- **Vercel preview**: Validate preview builds for UI/UX changes and screenshot updates.

Record results in the PR description when gates cannot run (e.g., environment limits) and explain mitigations.

## AI agent and automation coordination
- Note in the PR when Codex, Sourcery, or other agents assisted; include acceptance of suggested changes.
- Keep MCP/server configs under version control where documented (see `docs/MCP_CONFIGURATION.md`).
- Treat agent output like human contributions: review for security, compliance, and KPI accuracy.

## Pull request expectations
1. Keep PRs scoped to a single concern; link to the tracking issue/ticket.
2. Include:
   - Summary of changes and intended outcomes.
   - Tests and quality gates run (with commands).
   - KPI/dashboard impact and links to updated runbooks if analytics changed.
3. Require at least one approving review with write access before merging.
4. Resolve all comments and failing checks before merge; document exceptions with approvals.

## Merge standards
- Prefer **squash and merge** for traceability; ensure the squash message references the ticket and key impacts.
- Tag releases with semantic versioning when shipping to production; attach release notes and relevant artifacts.
- After merge:
  - Monitor pipelines and dashboards; revert or forward-fix quickly on regressions.
  - Update runbooks and KPI documentation to reflect any operational changes.

## Traceability checklist for analytics/dashboards
- KPIs updated in `docs/analytics/KPIs.md` with owners, formulas, thresholds, and runbook links.
- Dashboards documented in `docs/analytics/dashboards.md` with drill-down tables, alert routes, and runbook links.
- Post-merge artifacts (charts, screenshots, or sample payloads) attached to the PR when UI/alert surfaces change.

## Golden path: from branch to merge
1. Create and sync your branch (see branching strategy).
2. Implement the change; keep changeset small and focused.
3. Run lint, format, type-check, tests, and any package-specific checks.
4. Confirm SonarQube and CI signals are green; fix blockers before requesting review.
5. Open PR with summary, gates run, KPI/dashboard impact, and agent notes.
6. Address review feedback; re-run gates after major changes.
7. Merge via squash; tag release if shipping to production and update runbooks/KPI docs.
