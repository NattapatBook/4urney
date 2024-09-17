import { defineConfig } from "@vue/cli-service";

export default defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8000,
    allowedHosts: ["frontend"],
  },
});
