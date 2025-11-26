import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Abaco Loans Analytics',
  description: 'Customer-centric lending intelligence with governed growth for Abaco clients.',
  keywords: ['lending', 'risk management', 'fintech analytics', 'governance', 'customer growth'],
  openGraph: {
    title: 'Abaco Loans Analytics',
    description:
      'Customer-centric lending intelligence with governed growth for Abaco clients and partners.',
    url: 'https://abaco-loans-analytics.example.com',
    siteName: 'Abaco Loans Analytics',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Abaco Loans Analytics',
    description:
      'Audit-ready underwriting, portfolio visibility, and growth acceleration for lenders.',
  },
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
