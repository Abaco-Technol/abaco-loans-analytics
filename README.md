# ABACO — Loan Analytics Platform

ABACO delivers an executive-grade analytics and governance stack for lending teams. It pairs a Next.js dashboard with Python risk/KPI pipelines, Azure deployment scripts, and anonymized datasets, with end-to-end observability and audit-ready workflows.

## Stack map
- **apps/web**: Next.js dashboard for portfolio, risk, and growth views.
- **apps/analytics**: Python scoring, stress testing, and KPI pipelines.
- **infra/azure**: Azure infra-as-code and deployment scripts.
- **data_samples**: Anonymized datasets for repeatable development and testing.
- **Integrations**: Figma / Notion / Slack guide at `docs/integration-readiness.md` (service preflight checks included).

## Integrations
- Azure SQL / Cosmos / Storage
- Supabase
- Vercel
- OpenAI / Gemini / Claude
- SonarCloud
- GitHub Actions
- Run preflight checks in `docs/integration-readiness.md` before enabling each service.

## Observability, KPIs, and lineage
- Use `docs/Analytics-Vision.md` to keep dashboards, prompts, and KPIs aligned with the fintech narrative.
- Track sources, refresh timestamps, SLA badges, and on-call owners on every executive view.
- Surface data quality signals (null/invalid rates, schema drift counts, ingestion success %, freshness lag) and alert through CI and dashboard comments.
- Keep KPI ownership, formulas, and lineage links in `docs/KPI-Operating-Model.md` for auditability.

## Governance and workflows
- Enforce PR reviews, lint/test gates, and SonarQube quality gates before merging to main.
- Store secrets in GitHub or cloud KMS; never commit credentials or sample PII.
- Require audit logs for dashboard publishes/exports and validate access controls for sensitive fields.
- `docs/Copilot-Team-Workflow.md`: GitHub Copilot onboarding, validation/security workflows, and Azure/GitHub/KPI checklists.
- `docs/MCP_CONFIGURATION.md`: Add MCP servers via Codex CLI or config files (Context7, Figma, Chrome DevTools, Codex-as-MCP).
- `docs/GitHub-Workflow-Runbook.md`: Branching strategy, quality gates, agent coordination, and merge standards for traceable releases.
- `docs/Zencoder-Troubleshooting.md`: Remediation checklist for the VS Code Zencoder extension (`zencoder-cli ENOENT`).
- `docs/presentation-exports.md`: Guidance for traceable presentation exports and executive reporting.

## ContosoTeamStats companion API
ContosoTeamStats is a .NET 6 Web API for managing sports teams, with Docker, Azure deployment scripts, SendGrid/Twilio integrations, and SQL Server migrations. See `docs/ContosoTeamStats-setup.md` for local setup, secrets, migrations, and container validation.

## Fitten Code AI
Integrate Fitten Code AI locally and on GitHub with `docs/Fitten-Code-AI-Manual.md` (installation, integration, FAQs, and local inference tests).

## Deno helper
Validate the repository structure before running tooling:

```
deno run --allow-all main.ts
```

`--unstable` is unnecessary in Deno 2.0; add specific `--unstable-*` flags only when required.
