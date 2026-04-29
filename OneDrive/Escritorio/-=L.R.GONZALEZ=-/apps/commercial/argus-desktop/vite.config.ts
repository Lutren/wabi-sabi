import path from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['claudio-mark.svg'],
      manifest: {
        name: 'Argus',
        short_name: 'Argus',
        description: 'Companion operativo para MEDIOEVO con voz, escritura y soporte.',
        theme_color: '#0A0A0F',
        background_color: '#0A0A0F',
        display: 'standalone',
        orientation: 'portrait-primary',
        start_url: './',
        scope: './',
        icons: [
          {
            src: 'pwa-192x192.svg',
            sizes: '192x192',
            type: 'image/svg+xml',
            purpose: 'any'
          },
          {
            src: 'pwa-512x512.svg',
            sizes: '512x512',
            type: 'image/svg+xml',
            purpose: 'any maskable'
          }
        ]
      },
      devOptions: {
        enabled: false
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '127.0.0.1',
    port: 47847
  },
  preview: {
    host: '127.0.0.1',
    port: 47847
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    chunkSizeWarningLimit: 900,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react-markdown') || id.includes('remark-') || id.includes('micromark') || id.includes('mdast') || id.includes('unified') || id.includes('hast-') || id.includes('bail') || id.includes('trough')) {
              return 'markdown'
            }
            if (id.includes('react-dom') || id.includes('scheduler')) {
              return 'react-dom'
            }
            if (id.includes('/react/') || id.endsWith('/react/index.js')) {
              return 'react-core'
            }
            return 'vendor'
          }
          return undefined
        }
      }
    }
  }
})
