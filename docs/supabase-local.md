# Supabase local development

Use these steps to run Supabase locally for the Abaco Loans Analytics stack. Docker Desktop must be running before you start.

## Environment file
- Copy `.env.example` to `.env` and add the Supabase project values. Keep this file local-only and out of Git history.
  ```bash
  cp .env.example .env
  export NEXT_PUBLIC_SUPABASE_URL=... # from the Supabase project settings
  export NEXT_PUBLIC_SUPABASE_ANON_KEY=... # from the Supabase project settings
  ```

## Prerequisites
- Docker Desktop running with at least 8 GB RAM allocated (verify with `docker info`).
- Supabase CLI installed ([docs](https://supabase.com/docs/guides/cli)).
- Access to the project `pljjgdtczxmrxydfuaep`.
- Environment variables set in a `.env` file at the repo root:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## One-time authentication
```bash
# Sign in (opens browser for device login)
supabase login

# Link this repo to the hosted project
supabase link --project-ref pljjgdtczxmrxydfuaep
```

## Start the local stack
```bash
# From the repository root
supabase start

# Verify containers and services are healthy and ports are bound
supabase status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

If Docker is not running, `supabase start` will fail. Start Docker Desktop and retry.

## Stop and clean up
```bash
# Gracefully stop services
supabase stop

# Remove local volumes (optional)
supabase db reset --force
```

Keep `.env.local` and `.vercel` out of version control; they should never be committed.
