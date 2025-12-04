import { createClient, type SupabaseClient } from '@supabase/supabase-js'

export interface LandingPageData {
  metrics: { value: string; label: string }[]
  products: { title: string; detail: string }[]
  controls: string[]
  steps: { label: string; title: string; copy: string }[]
}

type Database = {
  public: {
    Tables: {
      landing_page_data: {
        Row: LandingPageData
      }
    }
    Views: Record<string, never>
    Functions: Record<string, never>
    Enums: Record<string, never>
    CompositeTypes: Record<string, never>
  }
}

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

export const isSupabaseConfigured =
  typeof supabaseUrl === 'string' &&
  typeof supabaseAnonKey === 'string' &&
  supabaseUrl.trim() !== '' &&
  supabaseAnonKey.trim() !== '' &&
  !supabaseUrl.includes('placeholder')

let supabaseClient: SupabaseClient<Database> | null = null

if (isSupabaseConfigured && supabaseUrl && supabaseAnonKey) {
  supabaseClient = createClient<Database>(supabaseUrl, supabaseAnonKey)
}

export const supabase = supabaseClient
