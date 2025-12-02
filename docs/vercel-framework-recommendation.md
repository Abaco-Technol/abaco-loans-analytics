# Vercel Framework Recommendation

## Best Preset
- **Framework:** Next.js 14+ (App Router)
- **Why:**
  - Hybrid rendering (ISR/SSR/SSG) for mixed static + dynamic data.
  - Built-in image optimization, edge middleware, and server actions align with low-latency fintech dashboards.
  - Strong SEO defaults and streaming SSR to keep FCP/LCP low for marketing and analytics pages.
  - Mature TypeScript support with strict mode to preserve safety and auditability.

## Stack Blueprint
- **Language:** TypeScript with strict mode enabled.
- **Styling:** Tailwind CSS or CSS Modules for predictable theming.
- **Data Layer:** Server Components for secure, direct data reads; client components only for interactive widgets.
- **APIs:** Route Handlers (`app/api`) with edge functions for auth/routing and regional latency optimization.
- **Observability:** `@vercel/analytics` and `@vercel/speed-insights` for user journey KPIs; pair with GitHub Actions status checks.
- **Security:** Content Security Policy headers, `Strict-Transport-Security`, and `Referrer-Policy` via middleware or Vercel config.

## Comparison vs. Vite SPA (React)
| Dimension | Next.js (App Router) | Vite SPA (React) |
| --- | --- | --- |
| Initial Load (FCP/LCP) | Faster via SSR/ISR + granular code splitting; supports partial prerendering | Slower cold start; full client hydration required |
| SEO | Native SSR/SSG provides crawlable HTML | CSR by default; requires additional prerender tooling |
| Vercel Optimization | First-class: Image Optimization, Edge Middleware, ISR, Route Handlers | Limited; manual CDN/image setup, edge requires custom adapters |
| Dynamic Data | Server Components stream data; reduces client fetch overhead | Client-only fetching; higher latency and bundle size |
| Complexity | Moderate; requires SSR and RSC patterns | Lower; pure client patterns |

## Deployment on Vercel
- **Framework Preset:** Next.js (auto-detected).
- **Build Command:** `npm run build`
- **Install Command:** `npm install` (or `npm ci` in CI)
- **Output Directory:** `.next`
- **Env Vars:** `NODE_ENV=production`, database URL(s), `NEXT_PUBLIC_API_URL` for client endpoints.
- **Commands to copy:**
  ```bash
  npm i -g vercel
  vercel link
  vercel
  vercel --prod
  ```

## Governance & Workflow
- Enforce PR checks (lint, type-check, build) in GitHub Actions before Vercel deploys.
- Track performance KPIs (FCP, LCP, TTFB) via Vercel Speed Insights dashboards per environment.
- Require code owners for critical surfaces (auth, payments, analytics) to maintain auditability.
