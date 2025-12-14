# Abaco Loans Analytics — Production Deployment Guide

## Quick Start Commands

### Local Development
```bash
cd apps/web
npm install
npm run dev
# Open http://localhost:3000
```

### Run All Quality Checks
```bash
cd apps/web
npm ci --legacy-peer-deps
npm run lint
npm run type-check
npm run build
```

**Note**: `--legacy-peer-deps` is required due to Sentry's peer dependency constraints with Next.js 16.

### Production Build & Verification
```bash
cd apps/web
npm ci --legacy-peer-deps
npm run build
npm run start
```

---

## Environment Variables

All environment variables must be configured in GitHub Secrets. Required variables differ between production and staging environments.

### Production Environment Variables

| Name | Purpose | Required | Notes |
|------|---------|----------|-------|
| **NEXT_PUBLIC_SUPABASE_URL** | Supabase project URL for backend data fetching | ✅ Yes | Public URL exposed to client-side code |
| **NEXT_PUBLIC_SUPABASE_ANON_KEY** | Supabase anonymous key for client authentication | ✅ Yes | Public key with limited RLS permissions |
| **NEXT_PUBLIC_SENTRY_DSN** | Sentry project DSN for error tracking and monitoring | ❌ Optional | If not set, error tracking is disabled |
| **SENTRY_ORG** | Sentry organization slug (for source map uploads) | ❌ Optional | Required only if uploading source maps to Sentry |
| **SENTRY_PROJECT** | Sentry project slug (for source map uploads) | ❌ Optional | Required only if uploading source maps to Sentry |
| **SENTRY_AUTH_TOKEN** | Sentry authentication token for build integration | ❌ Optional | Required only for source map uploads |
| **VERCEL_TOKEN** | Vercel API token for deployments | ✅ Yes | Used by GitHub Actions to deploy |
| **VERCEL_ORG_ID** | Vercel organization ID | ✅ Yes | Found in Vercel dashboard settings |
| **VERCEL_PROJECT_ID** | Vercel project ID | ✅ Yes | Found in Vercel project settings |

### Staging Environment Variables

Use the same variables as production, but with `-STAGING` suffix for Supabase configuration if using a separate staging database:

| Name | Purpose |
|------|---------|
| **NEXT_PUBLIC_SUPABASE_URL_STAGING** | Staging Supabase project URL |
| **NEXT_PUBLIC_SUPABASE_ANON_KEY_STAGING** | Staging Supabase anonymous key |
| **NEXT_PUBLIC_SENTRY_DSN** | Same Sentry DSN or separate staging DSN |

### Vercel Deployment Variables

Obtain these values from Vercel:

1. **VERCEL_TOKEN**: Generate in Vercel dashboard → Settings → Tokens → Create
2. **VERCEL_ORG_ID**: Found in Team Settings → General
3. **VERCEL_PROJECT_ID**: Found in project Settings → General

---

## GitHub Secrets Configuration

### Step 1: Navigate to GitHub Repository
1. Go to: `github.com/your-org/abaco-loans-analytics`
2. Click **Settings** → **Secrets and variables** → **Actions**

### Step 2: Add Production Secrets
Click **New repository secret** and add each required variable:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_SENTRY_DSN=https://your-key@your-org.ingest.sentry.io/project-id
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-org-id
VERCEL_PROJECT_ID=your-project-id
```

### Step 3: (Optional) Add Staging Secrets
If using separate staging infrastructure:

```
NEXT_PUBLIC_SUPABASE_URL_STAGING=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY_STAGING=staging-anon-key
```

---

## CI/CD Workflow

The `.github/workflows/ci-main.yml` defines a multi-stage pipeline:

### Pipeline Stages

1. **Lint** (parallel)
   - Runs ESLint to validate code quality
   - Fails on any linting errors

2. **Type-Check** (parallel)
   - Runs TypeScript compiler in `--noEmit` mode
   - Validates type safety across the codebase

3. **Build** (depends on lint + type-check)
   - Builds Next.js application
   - Loads production environment variables
   - Generates `.next/` directory with optimized production bundle

4. **Deploy to Production** (depends on build)
   - **Trigger**: Commits to `main` branch
   - **URL**: https://abaco-loans-analytics.vercel.app
   - Uses `production: true` to deploy to production environment
   - Passes production secrets to Vercel

5. **Deploy to Staging** (depends on build)
   - **Trigger**: Commits to `staging` branch
   - **URL**: https://abaco-loans-analytics-staging.vercel.app
   - Uses `production: false` for staging environment
   - Passes staging secrets to Vercel

### Viewing Workflow Status
- Go to **Actions** tab in GitHub repository
- Click on any workflow run to see detailed logs
- Deployment logs are available in Vercel dashboard

---

## Staging Workflow

### Creating a Staging Environment

1. **Create `staging` branch from `main`**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b staging
   git push -u origin staging
   ```

2. **Push changes to staging for testing**:
   ```bash
   git checkout staging
   git cherry-pick <commit-hash>  # or merge a feature branch
   git push origin staging
   ```

3. **Access staging deployment**:
   - URL: https://abaco-loans-analytics-staging.vercel.app
   - Verify changes before merging to `main`

4. **Promote staging to production**:
   ```bash
   git checkout main
   git merge staging
   git push origin main
   ```

### GitHub Environments

GitHub Environments are configured for approval workflows:

- **production**: Requires approval before deployment (optional to enable)
- **staging**: Auto-deploys on `staging` branch pushes

To enable approvals, go to **Settings** → **Environments** → **production** → **Required reviewers**

---

## Monitoring & Error Tracking

### Sentry Integration

Error tracking is configured via Sentry. The application automatically sends errors to Sentry if `NEXT_PUBLIC_SENTRY_DSN` is set.

#### Features Enabled

- **Client-side error tracking**: Captures JavaScript errors, exceptions, and unhandled promise rejections
- **Turbopack compatibility**: Simplified client-only implementation for compatibility with Next.js 16 Turbopack

**Note**: Sentry support for Turbopack is still in development. For the most current information, see [Sentry + Turbopack issue](https://github.com/getsentry/sentry-javascript/issues/8105).

#### Accessing Sentry Dashboard

1. Go to https://sentry.io
2. Sign in to your organization
3. Select the "abaco-loans-analytics" project
4. Review errors and metrics

#### Sentry Configuration

Modify sampling rates in `src/sentry.client.config.ts`:

```typescript
tracesSampleRate: 0.1,  // 10% of transactions in production
```

For more advanced Sentry features (server-side tracking, session replays, performance monitoring), consider upgrading Sentry when Turbopack support is complete.

---

## Deployment & Rollback

### Automatic Deployments

Deployments happen automatically via GitHub Actions:

- **Production**: Triggered by `git push origin main`
- **Staging**: Triggered by `git push origin staging`

### Manual Deployments via Vercel

If needed, deploy directly from Vercel without GitHub:

1. Go to https://vercel.com
2. Select the **abaco-loans-analytics** project
3. Click **Deployments** tab
4. Click the deployment to promote/rollback

### How to Rollback a Bad Deployment

#### Option 1: Revert Last Commit (Recommended)

```bash
# On main branch
git log --oneline -5
# Find the commit to revert
git revert <commit-hash>
git push origin main
```

This creates a new commit that undoes the problematic changes. The new commit will trigger a fresh deployment.

#### Option 2: Deploy Previous Version in Vercel

1. Go to https://vercel.com → **abaco-loans-analytics** → **Deployments**
2. Find the last known-good deployment
3. Click **...** → **Promote to Production**

This immediately serves the previous version without code changes.

#### Option 3: Manual Rollback via GitHub

```bash
# If multiple commits need to be reverted
git revert <bad-commit-hash>..HEAD
git push origin main
```

#### Option 4: Revert via Git Reset (Destructive)

⚠️ **Use only if no one else has pulled the bad commit**:

```bash
git reset --hard <last-known-good-commit>
git push --force origin main
```

---

## Performance Optimization

### Build Performance

The application uses Next.js with Turbopack for fast builds:

- **Dev mode**: Hot module reloading with instant updates
- **Production build**: Full optimizations including code splitting
- **Typical build time**: ~6 seconds on GitHub Actions (ubuntu-latest)

### Bundle Analysis

To analyze bundle size:

```bash
npm install -D @next/bundle-analyzer
```

Then add to `next.config.js`:

```javascript
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer(nextConfig)
```

Run with:

```bash
ANALYZE=true npm run build
```

### Caching Strategy

- **NPM dependencies**: Cached via `cache-dependency-path` in GitHub Actions
- **Next.js build cache**: Stored between workflow runs
- **Vercel edge caching**: HTTP caching headers set in `next.config.js`

---

## Security Best Practices

### Environment Variable Security

- **Never commit `.env.local`** (included in `.gitignore`)
- **Use GitHub Secrets** for all sensitive values
- **Rotate tokens** regularly (especially VERCEL_TOKEN)
- **Limit secret scope**: Use environment-specific secrets

### Deployment Security

- **Sentry source map hiding**: Enabled (`hideSourceMaps: true`)
- **Security headers**: Configured in `next.config.js`:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`

- **HTTPS only**: Vercel automatically enforces HTTPS
- **API rate limiting**: Configure in Supabase dashboard

### Code Quality

- **Type safety**: TypeScript `--noEmit` check in CI
- **Linting**: ESLint with Next.js rules enforced
- **No secrets in code**: Scan with `git-secrets` or `detect-secrets`

---

## Troubleshooting

### Build Fails with Type Errors

```bash
cd apps/web
npm run type-check
# Fix errors reported by TypeScript
npm run build
```

### Lint Errors Block Deployment

```bash
npm run lint -- --fix
# or manually fix the errors shown
git add .
git commit -m "fix: resolve linting errors"
git push origin main
```

### Vercel Deployment Token Expired

1. Go to https://vercel.com → Settings → Tokens
2. Generate a new token
3. Update `VERCEL_TOKEN` in GitHub Secrets

### Sentry Configuration Issues

If Sentry error tracking isn't working:
1. Verify `NEXT_PUBLIC_SENTRY_DSN` is set in GitHub Secrets
2. Check Sentry dashboard for incoming events: https://sentry.io
3. Ensure DSN is for the correct Sentry project
4. If not receiving errors, verify browser console for any Sentry initialization errors
5. Check that `NEXT_PUBLIC_SENTRY_DSN` environment variable is loaded at build time

### Environment Variables Not Loading

1. Verify secrets are added to GitHub Settings → Secrets
2. Check workflow file environment variable names match exactly
3. Rebuild to pick up latest secrets

---

## References

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/app/building-your-application/deploying)
- [Sentry Integration](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Supabase Client](https://supabase.com/docs/reference/javascript/client)
