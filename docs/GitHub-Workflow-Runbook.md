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
