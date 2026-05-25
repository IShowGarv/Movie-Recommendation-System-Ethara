/** @type {import('next').NextConfig} */
const nextConfig = {
  // OneDrive/synced folders can break webpack file watching and chunk writes
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
        ignored: ["**/node_modules", "**/.git"],
      };
    }
    return config;
  },
};

export default nextConfig;
