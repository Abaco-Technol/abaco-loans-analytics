# Vercel Framework Preset Recommendation

## Context and roles
- **Audience:** Engineering, DevOps, and product stakeholders shipping fintech analytics experiences.
- **Objective:** Deploy performant, SEO-ready, and data-rich experiences with strong observability and compliance on Vercel.

## Recommendation
- **Framework Preset:** **Next.js (App Router, v14+)**
- **Why:**
  - Native SSR/SSG/ISR for best FCP/LCP and crawlable HTML.
  - Edge Middleware and Edge Functions for global low-latency auth/routing.
  - Server Components and streaming for KPI dashboards with progressive rendering.
  - First-class Vercel optimizations (Images, Caching, Analytics, Speed Insights) with minimal config.

## Comparative analysis (Next.js vs Vite/SPA)
| Dimension | Next.js (App Router) | Vite/SPA (React) |
| --- | --- | --- |
| Initial Load (FCP/LCP) | Faster via SSR/SSG/ISR + route-level code splitting; streaming reduces time-to-data. | Slower: full client hydration before meaningful paint; larger initial bundle. |
| SEO | Strong: HTML rendered on the server; metadata API; ISR for freshness. | Weak by default: CSR requires extra pre-rendering; bots see minimal HTML. |
| Vercel Optimization | Built-in Image Optimization, Edge Middleware, Edge/Node runtimes, ISR, cache tags. | Limited: image/CDN tuning must be manual; no native ISR; edge requires custom setup. |
| Data Handling | Server Components fetch securely; incremental revalidation for KPIs; API Routes for server-side joins. | Client-only data fetch; more API roundtrips; harder to protect secrets. |
| Complexity | Moderate: SSR/RSC patterns; clear conventions for layouts/routes. | Lower: familiar SPA patterns but more infra wiring for SEO/perf. |
| Scalability | Horizontal and edge-native by default; good cold-start profile with Vercel functions. | Depends on separate backend; SPA alone does not scale server logic. |

## Deployment strategy (Vercel)
- **Framework Preset:** Next.js
- **Build command:** `npm run build` (or `pnpm run build` / `yarn build`)
- **Install command:** `npm ci` for deterministic builds.
- **Output directory:** `.next`
- **Environment configuration:**
  - `NODE_ENV=production`
  - `NEXT_PUBLIC_API_URL=https://api.example.com`
  - `DATABASE_URL=<postgres_url>` (server-side only)
  - `NEXT_RUNTIME=edge` per route when low latency matters.
- **Routing and middleware:** Use `middleware.ts` for auth, geo routing, or A/B tests; prefer Edge runtime for latency-sensitive checks.
- **Data freshness:** Prefer ISR with route-specific revalidation or cache tags for KPI pages; fall back to SSR for highly dynamic views.
- **Observability:** Enable `@vercel/analytics` and `@vercel/speed-insights` in `app/layout.tsx`; set up dashboards for FCP, LCP, TTFB, error rate, and cache hit ratio.
- **Security and compliance:** Enforce HTTPS (HSTS), `Strict-Transport-Security`, `Content-Security-Policy` tuned to allowed sources, and `Referrer-Policy: strict-origin-when-cross-origin`.
- **Team workflow:**
  - Branch-based previews for every PR.
  - Protect `main` with required checks: lint, type-check, unit tests.
  - Use GitHub Actions to run `npm ci`, `npm run lint`, `npm run test`, and `npm run build` per push.

## Copy-paste command deck
```bash
# Local verification
npm ci
npm run lint
npm run test
npm run build

# Deploy with Vercel CLI
npm i -g vercel
vercel link
vercel  # preview
vercel --prod

# Manage env vars
vercel env add DATABASE_URL production
vercel env add NEXT_PUBLIC_API_URL production
vercel env pull .env.local
```

## KPIs and dashboards
- **Performance:** FCP, LCP, TTFB, CLS, cache hit ratio, edge vs origin latency.
- **Reliability:** Error rate by route/function, build success rate, ISR revalidate success.
- **Growth/SEO:** Index coverage, crawl errors, organic CTR, structured data validity.
- **Product:** Funnel conversion on marketing pages, dashboard time-to-first-chart, API latency percentiles.

## Continuous improvement
- Review analytics weekly; tune caching and ISR windows per page.
- Add synthetic checks for key journeys (login → dashboard → export KPI report).
- Rotate secrets regularly; enable audit logs on Vercel and connected stores.
