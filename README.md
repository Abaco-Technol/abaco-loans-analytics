# ABACO — Loan Analytics Platform

ABACO delivers an executive-grade analytics and governance stack for lending teams. It pairs a Next.js dashboard with Python risk/KPI pipelines, Azure deployment scripts, and anonymized datasets, with end-to-end observability and audit-ready workflows.

## Stack map
- **apps/web**: Next.js dashboard for portfolio, risk, and growth views.
- **apps/analytics**: Python scoring, stress testing, and KPI pipelines.
- **infra/azure**: Azure infra-as-code and deployment scripts.
- **data_samples**: Anonymized datasets for repeatable development and testing.

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

## Governance and workflows
- `docs/Copilot-Team-Workflow.md`: GitHub Copilot onboarding, validation/security workflows, and Azure/GitHub/KPI checklists.
- `docs/MCP_CONFIGURATION.md`: Add MCP servers via Codex CLI or config files (Context7, Figma, Chrome DevTools, Codex-as-MCP).
- `docs/Zencoder-Troubleshooting.md`: Restore the VS Code Zencoder extension when CLI binaries are missing.
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
