import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Dev proxy: forward API calls to backend running on port 8000
    proxy: {
      '/process-text': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/test-text': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
