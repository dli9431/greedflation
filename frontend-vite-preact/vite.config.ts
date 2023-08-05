import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [preact()],
  resolve: {
    alias: {
      react: 'preact/compat',
    },
  },
  server: {
    host: true,
    port: 8000,
    watch: {
      usePolling: true
    }
  }
})
