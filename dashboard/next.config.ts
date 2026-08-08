/** @type {import('next').NextConfig} */
const nextConfig = {
  // Suppress leaflet SSR issues
  experimental: {},
  // Ensure static files in public/ are served correctly
  outputFileTracingIncludes: {
    '/data/*': ['public/data/**/*'],
  },
  // Disable static generation for API routes that need to be dynamic
  // (not needed but good practice)
}

export default nextConfig
