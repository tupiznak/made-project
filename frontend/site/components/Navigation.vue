<template>

  <v-toolbar app>
    <v-toolbar-title class="hidden-xs-only">
      <NuxtLink to="/" class="link">
        {{ appTitle }}
      </NuxtLink>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          nuxt>
        {{ item.title }}
      </v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
export default {
  name: "Navigation",
  data () {
    return {
      appTitle: 'Application',
      sidebar: false,
      menuItems: [
        { title: 'Home', path: '/' },
        { title: 'Dashboard', path: '/dashboard' },
        { title: 'Sign In', path: '/login' },
        { title: 'Sign Up', path: '/register' }
      ]
    }
  }
}
</script>

<style scoped>
.link {
  color: black;
  text-decoration: none;
}
</style>