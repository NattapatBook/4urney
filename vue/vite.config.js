import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
      '/ws': {
        target: 'http://localhost:8000',
        ws: true,
      },
    },
  },
  base: process.env.NODE_ENV == "production" ? "/static/" : "/",
  plugins: [vue()],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@import "@/styles/variables.scss";', // Optional: adjust if you use SCSS
      },
    },
  },
  resolve: {
    extensions: [".ts", ".js", ".json", ".vue"],
    alias: {
      "@": "/src",
    },
  },
});
