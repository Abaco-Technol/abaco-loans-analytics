import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ABACO — Loan Intelligence',
  description: 'Growth-ready analytics for credit, collections, finance, and funding teams.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
