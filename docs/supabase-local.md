# Supabase local workflow

Prerequisites
- Docker Desktop (running) with enough resources for Supabase containers.
- Supabase CLI installed and authenticated (`supabase --version` to verify).
- Project ref: `pljjgdtczxmrxydfuaep`.

Steps
1) Ensure Docker Desktop is running.
2) `supabase login` (interactive) with an account that can access the project.
3) `supabase link --project-ref pljjgdtczxmrxydfuaep` to bind the local folder.
4) `supabase start` to launch local services.
5) `supabase status` to confirm containers are healthy.
6) Export `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` into your `.env` (keep `.env.local` untracked).
7) Run web checks from repo root: `./scripts/check-web.sh`.
8) Stop services when finished: `supabase stop`.

Notes
- Keep `.env.local` and `.vercel` out of version control (already gitignored).
- If Docker is not running, `supabase start` will fail; start Docker Desktop first.
