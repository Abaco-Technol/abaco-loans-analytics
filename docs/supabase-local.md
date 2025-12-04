# Supabase local environment

This project expects Supabase services to be available locally. Use the Supabase CLI with Docker Desktop running to mirror the hosted project `pljjgdtczxmrxydfuaep`.

## Prerequisites
- Docker Desktop running with adequate resources (validate with `docker info`)
- Supabase CLI installed and authenticated
- Environment variables available in a local `.env` file (not committed):
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Bootstrap steps
1) Sign in to Supabase (interactive browser/device flow):
   ```bash
   supabase login
   ```
2) Link to the remote project for migrations and auth:
   ```bash
   supabase link --project-ref pljjgdtczxmrxydfuaep
   ```
3) Start the local stack (requires Docker Desktop):
   ```bash
   supabase start
   ```
4) Verify services are healthy:
   ```bash
   supabase status
   ```

Keep `.env.local` and `.vercel` out of version control. If Docker is not running, `supabase start` and dependent tests will fail.
