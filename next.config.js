/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    console.log('Setting up rewrites to proxy API requests to FastAPI server');
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig 