import { createClient } from '@supabase/supabase-js'

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

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co'
const supabaseAnonKey =
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.placeholder'

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey)
