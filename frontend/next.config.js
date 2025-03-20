/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  images: {
    domains: ['localhost'],
  },
  pageExtensions: ['tsx', 'ts', 'jsx', 'js']
}

module.exports = nextConfig
