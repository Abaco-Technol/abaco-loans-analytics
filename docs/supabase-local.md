# Supabase local development

Run Supabase locally with Docker Desktop and the Supabase CLI so the web app can exercise real storage and authentication flows.

## Prerequisites
- Docker Desktop running and logged in (`docker info` returns without errors)
- Supabase CLI installed (`npm install -g supabase` or `brew install supabase/tap/supabase`)
- Project reference: `pljjgdtczxmrxydfuaep`
- Environment variables `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env`

## First-time setup
1. Authenticate: `supabase login`
2. Link the project: `supabase link --project-ref pljjgdtczxmrxydfuaep`

## Start and verify services
1. Ensure Docker is running: `docker ps`
2. Start local services: `supabase start`
3. Check health: `supabase status`
4. Use the printed Studio credentials from `supabase start` to access the dashboard.

If Docker or the Supabase CLI are unavailable locally, install them before retrying these commands.
