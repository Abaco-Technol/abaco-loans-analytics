# Supabase local workflow

Use these steps to run the local Supabase stack and keep the project linked to the hosted project reference `pljjgdtczxmrxydfuaep`.

## Prerequisites
- Docker Desktop running locally with access to the default socket.
- Supabase CLI installed (`npm install -g supabase` or download from https://supabase.com/docs/guides/cli).
- An authenticated Supabase account.

## Startup checklist
1. Sign in to Supabase:
   ```bash
   supabase login
   ```
2. Link the project once per machine:
   ```bash
   supabase link --project-ref pljjgdtczxmrxydfuaep
   ```
3. Start services (requires Docker Desktop):
   ```bash
   supabase start
   ```
4. Verify health:
   ```bash
   supabase status
   ```

Keep `.env.local` and `.vercel` out of version control; local secrets belong in your personal environment files only.
