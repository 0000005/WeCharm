import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 只转发 /api 开头的请求到后端服务器
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
