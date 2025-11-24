import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,
  typescript: {
    tsconfigPath: './tsconfig.json',
  },
  turbopack: {
    root: './apps/web',
  },
  headers: async () => [
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
      ],
    },
  ],
  redirects: async () => [],
  rewrites: async () => ({
    beforeFiles: [],
    afterFiles: [],
    fallback: [],
  }),
}

export default nextConfig
