# ABACO — Loan Analytics Platform

ABACO delivers an executive-grade analytics and governance stack for lending teams. The platform pairs a Next.js dashboard with Python risk pipelines, Azure deployment scripts, and traceable KPI governance.

## Stack map
- **apps/web**: Next.js dashboard for portfolio, risk, and growth views.
- **apps/analytics**: Python scoring, stress testing, and KPI pipelines.
- **infra/azure**: Azure infra-as-code and deployment scripts.
- **data_samples**: Anonymized datasets for repeatable development and testing.

## Observability, KPIs, and lineage
- **KPI catalog**: Use `docs/KPI-Operating-Model.md` to define owners, formulas, and lineage links for every metric; keep PR and issue references for auditability.
- **Dashboards**: Ensure every visualization lists source tables, refresh timestamp, and on-call owner. Target vs. actual, sparkline trends, and SLA badges should be present on executive views.
- **Data quality**: Track null/invalid rates, schema drift counts, ingestion success %, and freshness lag; surface alerts into the dashboard and CI comments.

<<<<<<< HEAD
## Governance and compliance guardrails
- Enforce PR reviews, lint/test gates, and SonarQube quality gates before merging to main.
- Store secrets in GitHub or cloud KMS; never commit credentials or sample PII.
- Require audit logs for dashboard publishes/exports and validate access controls for sensitive fields.
- Align contributions to the `docs/Analytics-Vision.md` narrative to keep KPIs, prompts, and dashboards within fintech standards.

## Getting started
- Validate repository structure before running tooling:
  ```
  deno run --allow-all main.ts
  ```
  `--unstable` is unnecessary in Deno 2.0; add specific `--unstable-*` flags only when required.
- Web: see `apps/web` for Next.js dashboard setup.
- Analytics: use `apps/analytics` pipelines for risk and KPI computation; keep formulas versioned and tested.
- Infra: apply `infra/azure` scripts for environment provisioning; confirm `docs/integration-readiness.md` for service readiness and pre-checks.

## Essential knowledge base
- `docs/Analytics-Vision.md`: Vision, Streamlit blueprint, and narrative alignment for KPIs and prompts.
- `docs/KPI-Operating-Model.md`: Ownership, formulas, dashboard standards, lineage, GitHub guardrails, and audit controls.
- `docs/Copilot-Team-Workflow.md`: Inviting teams to GitHub Copilot, validation/security workflows, and Azure/GitHub/KPI checklists during the Enterprise trial.
- `docs/ContosoTeamStats-setup.md`: Setup, secrets, migrations, Docker validation, and Azure deployment for the bundled ContosoTeamStats .NET 6 Web API.
- `docs/Fitten-Code-AI-Manual.md`: Fitten Code AI installation, GitHub integration, FAQs, and local inference testing.
- `docs/MCP_CONFIGURATION.md`: Adding MCP servers via Codex CLI or `config.toml`, including Context7, Figma, Chrome DevTools, and running Codex as an MCP server.
- `docs/Zencoder-Troubleshooting.md`: Remediation checklist for the VS Code Zencoder extension (`zencoder-cli ENOENT`).
=======
- Azure SQL / Cosmos / Storage
- Supabase
- Vercel
- OpenAI / Gemini / Claude
- SonarCloud
- GitHub Actions

Consulta `docs/integration-readiness.md` para verificar el estado de cada integración y las comprobaciones previas que debes ejecutar antes de usarlas.

## ContosoTeamStats

This repository contains ContosoTeamStats, a .NET 6 Web API for managing sports teams that ships with Docker, Azure deployment scripts, SendGrid/Twilio integrations, and SQL Server migrations. Follow docs/ContosoTeamStats-setup.md for local setup, secrets, database provisioning, and container validation.

See docs/Analytics-Vision.md for the analytics vision, Streamlit blueprint, and the agent-ready narrative that keeps every KPI, scenario, and AI prompt aligned with our fintech-grade delivery.

  contains ContosoTeamStats, a .NET 6 Web API for managing sports teams that ships with Docker, Azure deployment scripts, SendGrid/Twilio integrations, and SQL Server migrations. Follow docs/ContosoTeamStats-setup.md for local setup, secrets, database provisioning, and container validation.

## Java and Gradle setup

Use a locally installed JDK (21+ recommended) and let Gradle's toolchain resolver download the appropriate compiler per module. Avoid adding `org.gradle.java.home` to version control so CI and developers can rely on their own `JAVA_HOME` or toolchains without path-specific overrides.

## Copilot Enterprise workflow

Use `docs/Copilot-Team-Workflow.md` when inviting your team to Copilot, documenting the validation and security workflows, and keeping the Azure, GitHub Actions, and KPI checklist aligned with your 30-day Enterprise trial (App Service F1, ACR Basic, and free Azure security tiers). The doc includes prompts you can reuse whenever Copilot is guiding changes.

 contains ContosoTeamStats, a .NET 6 Web API for managing sports teams that ships with Docker, Azure deployment scripts, SendGrid/Twilio integrations, and SQL Server migrations. Follow docs/ContosoTeamStats-setup.md for local setup, secrets, database provisioning, and container validation.

## Fitten Code AI 编程助手

Para integrar Fitten Code AI en este monorepo (local y GitHub), consulta `docs/Fitten-Code-AI-Manual.md`, que cubre la introducción al producto, instalación, integración, preguntas frecuentes y pruebas de inferencia local.

## MCP configuration

Use `docs/MCP_CONFIGURATION.md` to add MCP servers via the Codex CLI or by editing `config.toml`, including examples for Context7, Figma, Chrome DevTools, and how to run Codex itself as an MCP server.

## Deno helper

The repository exposes a tiny Deno helper at `main.ts` that verifies the expected directories before you execute tooling such as Fitten or analytics scripts. Run it with:

```
deno run --allow-all main.ts
```

`--unstable` is no longer needed in Deno 2.0; only include the specific `--unstable-*` flags when you actually depend on unstable APIs.

## Troubleshooting VS Code Zencoder extension

If you see `Failed to spawn Zencoder process: ... zencoder-cli ENOENT` while working in VS Code, follow the remediation checklist in `docs/Zencoder-Troubleshooting.md` to reinstall the extension and restore the missing binary.
- rerun CI
- rerun CI
# Trigger Azure Static Web Apps deployment
# Trigger Azure Static Web Apps deployment again
>>>>>>> origin/main
