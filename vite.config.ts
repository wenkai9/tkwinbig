import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "vue-i18n": "vue-i18n/dist/vue-i18n.cjs.js",
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    // host: "127.0.0.1",
    host: "0.0.0.0",
    port: 5016,
    proxy: {
      "/user": {
        // 文杰
        target: "http://192.168.31.240:8833",
        // localhost
        // target: "http://192.168.31.236:8000",
        changeOrigin: true,
        rewrite: (path) =>
          path.replace(
            /^\/user/,
            // 文杰
            "http://192.168.31.240:8833"
            // localhost
            // "http://192.168.31.236:8000"
          ),
      },

      "/api": {
        target: "https://preview.keenthemes.com/metronic8/laravel/api",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  // base: "/metronic8/vue/demo1/",
  base: "/",
  build: {
    chunkSizeWarningLimit: 3000,
    target: "es2015",
    terserOptions: {
      compress: {
        keep_infinity: true,
        pure_funcs: ["console.log"],
      },
    },
  },

});
