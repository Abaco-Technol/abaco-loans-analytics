# ABACO Fintech Platform - Build & Deployment Reference

## Quick Setup

```bash
# Root installation
npm install

# Build web app
npm run build

# Type check
npm run type-check

# Lint & format
npm run lint
npm run format

# Full validation
npm run check-all
```

## Key Commands

**Development:**
```bash
npm run dev                    # Start dev server
```

**Production:**
```bash
npm run build                  # Build for production
npm run start                  # Start production server
```

**Code Quality:**
```bash
npm run lint                   # Check linting
npm run lint:fix               # Auto-fix lint issues
npm run format                 # Auto-format code
npm run format:check           # Check formatting
npm run type-check             # TypeScript type check
npm run check-all              # Run all checks
```

## Project Structure

```
/apps/web/                     # Next.js frontend application
├── src/
│   ├── app/                   # Next.js App Router pages
│   ├── components/            # React components
│   ├── lib/                   # Business logic, utilities
│   │   ├── supabaseClient.ts  # DB client
│   │   ├── ml/                # ML services
│   │   ├── integrations/      # External APIs
│   │   └── data/              # Data utilities
│   ├── types/                 # TypeScript types
│   └── styles/                # Global styles
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── next.config.ts             # Next.js config
├── tailwind.config.ts         # Tailwind CSS config
└── .env.example               # Environment template

/notebooks/                    # Python analysis notebooks
├── financial_utils.py         # Financial calculations
└── ml_dashboard.py            # Streamlit dashboard

.github/workflows/             # CI/CD automation
├── ci.yml                     # Lint, type-check, build
├── deploy.yml                 # Production deployment
└── secret-scanning.yml        # Credential scanning
```

## Environment Setup

1. **Create `.env.local` in `/apps/web`:**
   ```bash
   cp apps/web/.env.example apps/web/.env.local
   ```

2. **Add your credentials:**
   - Supabase URL and key
   - OpenAI API key
   - xAI Grok key
   - Any other service credentials

3. **Never commit `.env.local`** - it's in `.gitignore`

## CI/CD Pipeline

**On Every Push to `main` or `develop`:**
1. Install dependencies
2. Type checking (TypeScript)
3. Linting (ESLint)
4. Format checking (Prettier)
5. Build (Next.js)
6. Security audit (npm audit)
7. Secret scanning (Gitleaks + TruffleHog)
8. Vulnerability scanning (Trivy)

**On Merge to `main`:**
- Deploy to Vercel (if `VERCEL_TOKEN` configured)

## Troubleshooting

**Build fails:**
```bash
rm -rf node_modules package-lock.json apps/web/node_modules apps/web/package-lock.json
npm install
cd apps/web && npm install
npm run build
```

**Lint errors:**
```bash
npm run lint:fix              # Auto-fix fixable issues
npm run format                # Re-format code
```

**Type errors:**
```bash
npm run type-check            # See detailed errors
```

## GitHub Actions Secrets Required

For production deployment, configure these in GitHub Settings → Secrets:

```
VERCEL_TOKEN=               # Vercel deployment token
VERCEL_ORG_ID=             # Vercel organization ID
VERCEL_PROJECT_ID=         # Vercel project ID
NEXT_PUBLIC_SUPABASE_URL=  # Supabase URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=  # Supabase anon key
```

## Production Deployment

1. **Merge PR to `main`** (triggers deploy workflow)
2. **Verify in Vercel dashboard** (vercel.com)
3. **Monitor logs** for errors

## Security

- **Never commit secrets** - use `.env.local`
- **Rotate credentials** every 90 days
- **Review dependencies** for security updates
- **Run `npm audit`** before releases
- See `SECURITY.md` for full policy

## Performance Optimization

- Next.js caching configured
- Turbopack for fast builds
- TypeScript strict mode enabled
- ESLint enforces best practices
- Prettier ensures consistency

## Next Steps

1. ✅ **Phase 1 Complete**: Config, tooling, CI/CD
2. 🔄 **Phase 2**: Implement Python financial analysis engine
3. 🔄 **Phase 3**: Create Streamlit ML dashboard
4. 🔄 **Phase 4**: Deploy to production
