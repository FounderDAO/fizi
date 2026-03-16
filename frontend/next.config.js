/** @type {import('next').NextConfig} */
const createNextIntlPlugin = require('next-intl/plugin');
const withNextIntl = createNextIntlPlugin();

const nextConfig = {
  images: {
    domains: ['localhost', 'fizi.uz'],
  },
};

module.exports = withNextIntl(nextConfig);
