import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,
  typescript: {
    tsconfigPath: './tsconfig.json',
  },
  headers: async () =>
    await Promise.resolve([
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]),
  redirects: async () => [],
  rewrites: async () =>
    await Promise.resolve({
      beforeFiles: [],
      afterFiles: [],
      fallback: [],
    }),
}

export default nextConfig
