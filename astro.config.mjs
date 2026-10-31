import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://pranast.com',
  output: 'static',
  // Matches pranast.com, which uses trailing slashes (e.g. /faq/)
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        if (item.url === 'https://pranast.com/') {
          item.changefreq = 'weekly';
          item.priority = 1.0;
        } else if (
          item.url.includes('/cyber-security/') ||
          item.url.includes('/cloud-infrastructure/') ||
          item.url.includes('/digital-transformation/') ||
          item.url.includes('/it-support-managed-services/') ||
          item.url.includes('/bridgead/') ||
          item.url.includes('/who-we-are/') ||
          item.url.includes('/contact/')
        ) {
          item.changefreq = 'monthly';
          item.priority = 0.9;
        } else if (item.url.includes('/blog/') || item.url.includes('/case-studies/')) {
          item.changefreq = 'monthly';
          item.priority = 0.8;
        } else if (item.url.includes('/privacy-policy/') || item.url.includes('/terms-of-service/')) {
          item.changefreq = 'yearly';
          item.priority = 0.3;
        } else {
          item.changefreq = 'monthly';
          item.priority = 0.7;
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
