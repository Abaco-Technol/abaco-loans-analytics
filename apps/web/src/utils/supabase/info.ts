const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''

export const projectId = (() => {
  const match = supabaseUrl.match(/^https?:\/\/([^.]+)\.supabase\.co/)
  return match?.[1] ?? ''
})()

export const publicAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

export const supabaseConfigAvailable = Boolean(projectId && publicAnonKey)
