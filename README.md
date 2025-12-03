# ABACO — Loan Analytics Platform

ABACO delivers an executive-grade analytics and governance stack for lending teams. The platform pairs a Next.js dashboard with Python risk pipelines, Azure deployment scripts, and traceable KPI governance.

## Stack map
- **apps/web**: Next.js dashboard for portfolio, risk, and growth views.
- **apps/analytics**: Python scoring, stress testing, and KPI pipelines.
- **infra/azure**: Azure infra-as-code and deployment scripts.
- **data_samples**: Anonymized datasets for repeatable development and testing.

<<<<<<< HEAD
- Azure SQL / Cosmos / Storage
- Supabase
- Vercel
- OpenAI / Gemini / Claude
- SonarCloud
- GitHub Actions
<<<<<<< HEAD
- Figma / Notion / Slack (ver [guía de integraciones](docs/integrations.md))
=======
Consulta `docs/integration-readiness.md` para verificar el estado de cada integración y las comprobaciones previas que
debes ejecutar antes de usarlas.
=======
## Observability, KPIs, and lineage
- **KPI catalog**: Use `docs/KPI-Operating-Model.md` to define owners, formulas, and lineage links for every metric; keep PR and issue references for auditability.
- **Dashboards**: Ensure every visualization lists source tables, refresh timestamp, and on-call owner. Target vs. actual, sparkline trends, and SLA badges should be present on executive views.
- **Data quality**: Track null/invalid rates, schema drift counts, ingestion success %, and freshness lag; surface alerts into the dashboard and CI comments.
>>>>>>> upstream/main

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

<<<<<<< HEAD
## ContosoTeamStats

Este repositorio contiene ContosoTeamStats, una API Web de .NET 6 para gestionar equipos deportivos que incluye Docker,
scripts de despliegue en Azure, integraciones con SendGrid/Twilio y migraciones de SQL Server. Sigue
`docs/ContosoTeamStats-setup.md` para la configuración local, secretos, aprovisionamiento de base de datos y validación
de contenedores.

Consulta `docs/Analytics-Vision.md` para la visión analítica, el plano de Streamlit y la narrativa preparada para
agentes que mantiene cada KPI, escenario y prompt de IA alineados con nuestra entrega de nivel fintech.

Para gobernanza, trazabilidad y flujos de revisión GitHub-first en KPIs y dashboards, sigue
`docs/analytics/governance.md`.

## Catálogo de KPIs y runbooks

Consulta `docs/analytics/KPIs.md` para la taxonomía de KPIs, propietarios, orígenes de datos, umbrales y enlaces a
dashboards, tablas de drill-down y runbooks (`docs/analytics/runbooks`). Usa `docs/analytics/dashboards.md` como guía de
visualizaciones y alertas.

### Variables de entorno (alertas y drill-down)

- `NEXT_PUBLIC_ALERT_SLACK_WEBHOOK`: webhook de Slack para alertas (red/amber).
- `NEXT_PUBLIC_ALERT_EMAIL`: correo de alertas si Slack no está disponible.
- `NEXT_PUBLIC_DRILLDOWN_BASE_URL`: base URL para tablas de drill-down (cola de cobranzas, cohortes de mora, errores de ingesta).
Configura estas variables en tu despliegue (Vercel/Azure) y en `.env.local` durante desarrollo.

## Copilot Enterprise workflow

Usa `docs/Copilot-Team-Workflow.md` cuando invites a tu equipo a Copilot, documentes los flujos de validación y
seguridad, y mantengas alineada la checklist de Azure, GitHub Actions y KPIs durante tu prueba de 30 días de Enterprise
(App Service F1, ACR Basic y tiers de seguridad gratuitos de Azure). El documento incluye prompts reutilizables cuando
Copilot guíe los cambios.

Validation signal: refreshed on the validation/contoso-team-stats branch to trigger CI verification for the current release cycle.

## Fitten Code AI 编程助手

Para integrar Fitten Code AI en este monorepo (local y GitHub), consulta `docs/Fitten-Code-AI-Manual.md`, que cubre la
introducción al producto, instalación, integración, preguntas frecuentes y pruebas de inferencia local.

## MCP configuration

Usa `docs/MCP_CONFIGURATION.md` para agregar servidores MCP mediante la CLI de Codex o editando `config.toml`, con
ejemplos para Context7, Figma, Chrome DevTools y cómo ejecutar Codex como servidor MCP.

## Deno helper

The repository exposes a tiny Deno helper at `main.ts` that verifies the expected directories before you execute
tooling such as Fitten or analytics scripts. Run it with:

```sh
deno run --allow-all main.ts
```

`--unstable` ya no es necesario en Deno 2.0; solo incluye los flags `--unstable-*` cuando dependas de APIs inestables.

## VS Code Python terminals

If you rely on `.env` files while running the Python analytics scripts, enable the VS Code setting
`python.terminal.useEnvFile` so integrated terminals automatically load those variables. Add this to your user
`settings.json` via the Command Palette to avoid missing secrets during local runs.

## Troubleshooting VS Code Zencoder extension

Si observas `Failed to spawn Zencoder process: ... zencoder-cli ENOENT` en VS Code, sigue la checklist de remediación en
`docs/Zencoder-Troubleshooting.md` para reinstalar la extensión y restaurar el binario faltante.

## Java & Gradle

The Gradle build is configured for JDK **21** via the toolchain in `build.gradle`. Running Gradle with newer
early-access JDKs (e.g., JDK 25) is not supported by the current Gradle wrapper (8.10) and will fail during project
sync. If your IDE selects a newer JDK by default, switch the Gradle JVM to JDK 21 (or another supported LTS version)
and ensure your `JAVA_HOME` points to that installation. In IntelliJ IDEA, go to **Settings > Build, Execution,
Deployment > Build Tools > Gradle** and set **Gradle JVM** to JDK 21 to avoid the sync error. You can verify the
wrapper is using JDK 21 by running `./gradlew --version` and checking the `JVM` line.
>>>>>>> origin/main
=======
## Essential knowledge base
- `docs/Analytics-Vision.md`: Vision, Streamlit blueprint, and narrative alignment for KPIs and prompts.
- `docs/KPI-Operating-Model.md`: Ownership, formulas, dashboard standards, lineage, GitHub guardrails, and audit controls.
- `docs/Copilot-Team-Workflow.md`: Inviting teams to GitHub Copilot, validation/security workflows, and Azure/GitHub/KPI checklists during the Enterprise trial.
- `docs/ContosoTeamStats-setup.md`: Setup, secrets, migrations, Docker validation, and Azure deployment for the bundled ContosoTeamStats .NET 6 Web API.
- `docs/Fitten-Code-AI-Manual.md`: Fitten Code AI installation, GitHub integration, FAQs, and local inference testing.
- `docs/MCP_CONFIGURATION.md`: Adding MCP servers via Codex CLI or `config.toml`, including Context7, Figma, Chrome DevTools, and running Codex as an MCP server.
- `docs/Zencoder-Troubleshooting.md`: Remediation checklist for the VS Code Zencoder extension (`zencoder-cli ENOENT`).
>>>>>>> upstream/main
