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
