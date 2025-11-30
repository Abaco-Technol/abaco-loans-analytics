import './globals.css'

export const metadata = {
  title: 'Abaco Loans Analytics',
  description: 'AI-powered image generation for loan analytics.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}