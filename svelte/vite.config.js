import { sveltekit } from '@sveltejs/kit/vite';
import path from 'path';

/** @type {import('vite').UserConfig} */
const config = {
  plugins: [sveltekit()],
  server: {
    port: 5173,
    strictPort: true
  },
  resolve: {
    alias: {
      '@tools': path.resolve('./src/tools'),
      '@components': path.resolve('./src/components'),
      '@store': path.resolve('./src/store')
    }
  }
};

export default config;
