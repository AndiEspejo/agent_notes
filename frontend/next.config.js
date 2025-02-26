/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // No need for rewrites in static export
  // The basePath helps when hosting in a subdirectory
  basePath: '',
  // Turn off image optimization for static export
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
