// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  css: ['vuetify/lib/styles/main.sass'],
  build: {
    transpile: ['vuetify'],
  },
  vite: {
    define: {
      'process.env.DEBUG': false,
    },
  },
  publicRuntimeConfig: {
    serverUrl: process.env.SERVER_URL || 'http://127.0.0.1:8888',
  }
})
