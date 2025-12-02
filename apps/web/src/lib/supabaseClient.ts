import { createClient, type SupabaseClient } from '@supabase/supabase-js'
import type { LandingPageData } from '../types/landingPage'

type Database = {
  public: {
    Tables: {
      landing_page_data: {
        Row: LandingPageData
      }
    }
  }
}

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

const hasSupabaseEnv = Boolean(supabaseUrl && supabaseAnonKey)

export const supabase: SupabaseClient<Database> | null = hasSupabaseEnv
  ? createClient<Database>(supabaseUrl as string, supabaseAnonKey as string)
  : null

export const isSupabaseConfigured = hasSupabaseEnv
