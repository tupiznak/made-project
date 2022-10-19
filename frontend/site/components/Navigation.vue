<template>

  <v-toolbar app>
    <v-toolbar-title class="hidden-xs-only">
      <NuxtLink to="/" class="link">
        {{ appTitle }}
      </NuxtLink>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items v-if="isAuthenticated">
      <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          nuxt>
        {{ item.title }}
      </v-btn>
      <v-btn to="/profile" nuxt>{{ user?.name }}</v-btn>
    </v-toolbar-items>
    <v-toolbar-items v-else>
      <v-btn
          flat
          v-for="item in authItems"
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
  mounted() {
    if (process.client) {
      this.isAuthenticated = localStorage.getItem('isAuthenticated')
      this.user = JSON.parse(localStorage.getItem('user'))
    }
    window.addEventListener('user-localstorage-changed', (event) => {
      this.isAuthenticated = event.detail.isAuth;
      this.user = JSON.parse(event.detail.user);
    });
  },
  data () {
    return {
      appTitle: 'Application',
      isAuthenticated: false,
      user: null,
      menuItems: [
        { title: 'Home', path: '/' },
        { title: 'Dashboard', path: '/dashboard' },
      ],
      authItems: [
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