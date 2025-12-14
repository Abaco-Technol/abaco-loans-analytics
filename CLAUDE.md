# Agent Guide

This repository contains a Next.js application in a monorepo-like structure.

## Project Structure
- `apps/web`: The main Next.js web application.
- `.github/workflows`: CI/CD pipelines.

## Commands
All commands should be run from the `apps/web` directory unless specified otherwise.

- **Install**: `npm install` (or `npm ci` for clean install)
- **Dev Server**: `npm run dev`
- **Lint**: `npm run lint` (Uses `next lint`, compatible with ESLint 9)
- **Type Check**: `npm run type-check`
- **Build**: `npm run build`

## Guidelines for Agents
1. **ESLint 9**: Do not use the `--ext` flag when running eslint manually. Use `npm run lint`.
2. **Paths**: Always verify the working directory. Most app logic resides in `apps/web`.
3. **Partial Edits**: When refactoring, ensure `package.json` scripts remain valid before running builds.
4. **Deployment**: Deployment is handled via CI/CD. Do not append deployment commands to documentation files.

## Production Environment Variables

No environment variables are currently required for production.

## Deployment Steps

1. Ensure the following secrets are configured in GitHub:
   - `VERCEL_TOKEN`: Personal access token for Vercel.
   - `VERCEL_ORG_ID`: Organization ID in Vercel.
   - `VERCEL_PROJECT_ID`: Project ID in Vercel.

2. The CI/CD pipeline will automatically deploy to Vercel after a successful build.

## Local Development

1. Install dependencies:
   ```bash
   npm ci
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Checks

1. Run linting:
   ```bash
   npm run lint
   ```

2. Run type-checking:
   ```bash
   npm run type-check
   ```

3. Build the application:
   ```bash
   npm run build
   ```

## Rollback Strategy

To rollback a deployment on Vercel:
1. Navigate to the Vercel dashboard.
2. Select the project and go to the "Deployments" tab.
3. Revert to a previous deployment by selecting "Redeploy" on the desired version.