import type { ReactNode } from 'react'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Inter } from 'next/font/google'
<<<<<<< HEAD
=======
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
>>>>>>> origin/main
import './globals.css'
import { siteMetadata } from './seo'

const inter = Inter({ subsets: ['latin'] })

<<<<<<< HEAD
export const metadata: Metadata = {
  title: 'Abaco Loans Analytics',
  description: 'Customer-centric lending intelligence with governed growth for Abaco clients.',
}
=======
export const metadata = siteMetadata
>>>>>>> origin/main

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode
}>) {
  return (
<<<<<<< HEAD
<<<<<<< HEAD
    <html lang="en">
      <body className={inter.className}>{children}</body>
=======
    <html lang="en" className={inter.className}>
      <body>
=======
    <html lang="en" className={inter.className}>
      <body>
        <a className="skipLink" href="#main-content">
          Skip to main content
        </a>
>>>>>>> origin/main
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
<<<<<<< HEAD
>>>>>>> origin/main
=======
>>>>>>> origin/main
    </html>
  )
}
