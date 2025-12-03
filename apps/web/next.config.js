const nextConfig = {
  typescript: {
    tsconfigPath: './tsconfig.json',
  },
<<<<<<< HEAD:apps/web/next.config.ts
  experimental: {
    turbopackUseSystemTlsCerts: true,
  },
  turbopack: {
    root: __dirname,
  },
  // eslint-disable-next-line @typescript-eslint/require-await
=======
>>>>>>> origin/main:apps/web/next.config.js
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
        {
          key: 'Referrer-Policy',
          value: 'strict-origin-when-cross-origin',
        },
      ],
    },
  ],
<<<<<<< HEAD:apps/web/next.config.ts
  // eslint-disable-next-line @typescript-eslint/require-await
  redirects: async () => [],
  // eslint-disable-next-line @typescript-eslint/require-await
=======
  redirects: async () => [],
>>>>>>> origin/main:apps/web/next.config.js
  rewrites: async () => ({
    beforeFiles: [],
    afterFiles: [],
    fallback: [],
  }),
}

module.exports = nextConfig
