<template lang="pug">
v-toolbar(app='')
  v-toolbar-title.hidden-xs-only
    nuxtlink.link(to='/') {{ appTitle }}
  v-spacer
  v-toolbar-items(v-if='isAuthenticated')
    v-btn(flat='' v-for='item in menuItems' :key='item.title' :to='item.path' nuxt='') {{ item.title }}
    v-btn(to='/profile' nuxt='') {{ user?.name }}
  v-toolbar-items(v-else='')
    v-btn(flat='' v-for='item in authItems' :key='item.title' :to='item.path' nuxt='') {{ item.title }}
</template>

<script>
import {LocalStorage} from "../services/LocalStorage";

export default {
  setup() {
    const localStorageService = new LocalStorage()
    return {
      localStorageService
    }
  },
  name: "Navigation",
  mounted() {
    this.isAuthenticated = this.localStorageService.getIsAuthenticated()
    this.user = this.localStorageService.getUser()

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