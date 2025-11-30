# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please email security@abaco.dev instead of using the issue tracker.

**Do NOT** open public GitHub issues for security vulnerabilities.

## Security Best Practices

### Environment Variables

All sensitive credentials must be stored in `.env.local` (never committed):

- Never commit `.env`, `.env.local`, or any files containing credentials
- Use `.env.example` as a template
- All CI/CD secrets must be configured in GitHub Settings → Secrets

### Credential Rotation Schedule

- **API Keys**: Rotate every 90 days
- **Database Passwords**: Rotate every 180 days
- **OAuth Tokens**: Rotate immediately if compromised
- **Service Account Keys**: Rotate every 365 days

### Required Security Checks

All PRs must pass:

1. **TypeScript strict mode** (`npm run type-check`)
2. **ESLint rules** (`npm run lint`)
3. **Prettier formatting** (`npm run format:check`)
4. **Secret scanning** (Gitleaks + TruffleHog)
5. **Dependency audit** (`npm audit`)
6. **Build verification** (`npm run build`)

### Dependency Management

- Keep dependencies up-to-date
- Review dependency updates for security advisories
- Run `npm audit` before releases
- Remove unused dependencies

### Production Deployment

Only merge to `main` branch when:

1. All tests pass
2. Security scanning passes
3. Build is successful
4. Code review approved
5. No blocking issues

## Incident Response

1. Immediately rotate compromised credentials
2. Investigate scope of exposure
3. Patch affected systems
4. Update dependent systems
5. Document lessons learned

## Contact

Security inquiries: security@abaco.dev
