import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    TanStackRouterVite(),
    react(),
    tailwindcss(),
  ],
  server: {
    host: '0.0.0.0', // Tüm ağ arayüzlerini dinle
    port: 5173,
    watch: {
      usePolling: true
    },
  }
})
