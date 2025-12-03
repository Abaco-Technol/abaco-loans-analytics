# ABACO — Loan Analytics Platform

Arquitectura:

- **apps/web**: Next.js dashboard corporativo.
- **apps/analytics**: pipelines de Python para riesgo, scoring y KPIs.
- **infra/azure**: scripts de despliegue Azure.
- **data_samples**: datasets anonimizados para desarrollo.

Integraciones disponibles:

- Azure SQL / Cosmos / Storage
- Supabase
- Vercel
- OpenAI / Gemini / Claude
- SonarCloud
- GitHub Actions

## Fitten Code AI 编程助手

Para integrar Fitten Code AI en este monorepo (local y GitHub), consulta `docs/Fitten-Code-AI-Manual.md`, que cubre la introducción al producto, instalación, integración, preguntas frecuentes y pruebas de inferencia local.

## Deno helper

The repository exposes a tiny Deno helper at `main.ts` that verifies the expected directories before you execute tooling such as Fitten or analytics scripts. Run it with:

```
deno run --allow-all main.ts
```

`--unstable` is no longer needed in Deno 2.0; only include the specific `--unstable-*` flags when you actually depend on unstable APIs.

## Quality gates

Run the web experience checks (type safety, linting, and formatting) with a single command from the repository root:

```
./scripts/check-web.sh
```

The helper script enforces consistent paths and exits on the first failure to keep audit trails predictable for CI, SonarQube, and code review agents.

## PR sync and merge workflow

Use the reproducible workflow below to keep branches aligned with `origin/main`, surface conflicts early, and provide a copy-paste path for CI agents such as SonarQube, Sourcery, CodeRabbit, and Codex:

```
./scripts/git-pr-sync.sh
./scripts/check-web.sh
git commit -am "Describe the change"
git push
# Merge via the GitHub UI or: gh pr merge --merge --delete-branch
```

For branches that need the full cycle (checkout → merge `origin/main` → checks → commit → push) in a single, auditable command, use:

```
./scripts/pr-merge.sh <branch> "Commit message"
# The script stops on conflicts and prints status so you can resolve safely before rerunning.
```
