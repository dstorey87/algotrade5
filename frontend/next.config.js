/**
 * Next.js Configuration for AlgoTradePro5 Frontend
 * 
 * This configuration ensures proper App Router setup and removes any conflicts
 * with the Pages Router. It also includes optimizations for development and production.
 */

const nextConfig = {
  // Enable experimental features for optimized performance
  experimental: {
    optimizeCss: true,
  },

  // Configure path aliases for cleaner imports
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
    };
    return config;
  },

  // Define page extensions to include TypeScript and JavaScript files
  pageExtensions: ['tsx', 'ts', 'jsx', 'js'],

  // Disable image optimization in development for faster builds
  images: {
    unoptimized: process.env.NODE_ENV !== 'production',
  },

  // Enable React Strict Mode for better debugging
  reactStrictMode: true,

  // Configure environment variables for runtime
  env: {
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL,
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  },
};

module.exports = nextConfig;
