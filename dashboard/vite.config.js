import { defineConfig } from 'vite'

export default defineConfig({
  base: '/sp500-by-sector/dashboard/',
  build: {
    outDir: '../docs',
    emptyOutDir: true
  },
  server: {
    port: 3000
  }
})