// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(__dirname, 'web');

// 站点静态化配置：纯静态导出，可托管到 GitHub Pages / Vercel / Netlify / 自建 Nginx
export default defineConfig({
  site: 'https://wiselinpm.github.io',
  base: '/agent-pitfalls-cn',
  srcDir: path.join(WEB, 'src'),
  publicDir: path.join(WEB, 'public'),
  output: 'static',
  integrations: [
    sitemap(),
    mdx(),
  ],
  build: {
    format: 'directory',
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark-dimmed',
      wrap: true,
    },
  },
  vite: {
    css: {
      postcss: path.join(WEB, 'postcss.config.mjs'),
    },
    resolve: {
      alias: {
        '@': path.join(WEB, 'src'),
      },
    },
  },
});