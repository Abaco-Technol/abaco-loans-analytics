# Abaco Loans Analytics — Web App

This directory holds the Next.js web application that powers the Abaco Loans Analytics product.

## Prerequisites

- Node.js 20 or later
- npm (bundled with Node.js)

## Getting started

1. `cd apps/web`
2. `npm install`
3. `npm run dev`

Open <http://localhost:3000> in your browser to view the app while the dev server is running.

## Production Environment Variables

The following environment variables must be configured for production deployment:

| Variable | Purpose | Required |
|----------|---------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | ✅ Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | ✅ Yes |
| `NEXT_PUBLIC_SENTRY_DSN` | Sentry error tracking DSN | ❌ Optional |
| `VERCEL_TOKEN` | Vercel API token for deployments | ✅ Yes (CI/CD) |
| `VERCEL_ORG_ID` | Vercel organization ID | ✅ Yes (CI/CD) |
| `VERCEL_PROJECT_ID` | Vercel project ID | ✅ Yes (CI/CD) |

For detailed environment setup, deployment procedures, and GitHub Secrets configuration, see **[CLAUDE.md](./CLAUDE.md)** (production deployment guide).

## Available scripts

- `npm run dev` – starts the Next.js development server with hot reloading.
- `npm run build` – compiles the app for production.
- `npm run start` – runs the production build locally (after `npm run build`).
- `npm run lint` – enforces ESLint rules (`--max-warnings=0` to fail on warnings).
- `npm run type-check` – runs `tsc --noEmit` to validate TypeScript types.

## CI/CD Workflow

`.github/workflows/ci-main.yml` defines a multi-stage CI/CD pipeline:

1. **Lint & Type-Check** (parallel jobs) – enforces code quality
2. **Build** (depends on lint & type-check) – compiles Next.js application
3. **Deploy to Production** (main branch) – automatic deployment to Vercel
4. **Deploy to Staging** (staging branch) – automatic deployment to Vercel staging

All jobs use Node.js 20, npm cache for fast dependency installation, and environment variables from GitHub Secrets.

## Project structure

- `app/` – Next.js App Router routes, layouts, and pages.
- `public/` – Static assets served by the Next.js server.
- `package.json` – Dependencies, devDependencies, and workspace-specific scripts.

## Type-check script

If `npm run type-check` fails with “missing script”, add the following entry to `apps/web/package.json` and rerun the command:

```json
"type-check": "tsc --noEmit"
```

## Quick Verification

Run all quality checks locally before pushing:

```bash
cd apps/web
npm ci
npm run lint
npm run type-check
npm run build
```

Run the development server:

```bash
cd apps/web
npm run dev
# then open http://localhost:3000
```

## Production Deployment

See **[CLAUDE.md](./CLAUDE.md)** for:
- Complete deployment guide
- GitHub Secrets configuration
- Monitoring & error tracking setup
- Rollback procedures
- Staging workflow
