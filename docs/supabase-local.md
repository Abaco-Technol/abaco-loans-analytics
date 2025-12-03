# Supabase local development

Local Supabase emulation requires Docker Desktop and the Supabase CLI. Start Docker Desktop before running any Supabase commands.

## Prerequisites
- Docker Desktop running and logged in
- Supabase CLI installed (`npm install -g supabase` or `brew install supabase/tap/supabase`)
- Project reference: `pljjgdtczxmrxydfuaep`

## Startup workflow
1. Authenticate: `supabase login`
2. Link the project: `supabase link --project-ref pljjgdtczxmrxydfuaep`
3. Start local services: `supabase start`
4. Check health: `supabase status`

Use the Supabase dashboard credentials printed after `supabase start` to access local Studio. Environment variables `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` should be available in your `.env` file for the web app to connect.
